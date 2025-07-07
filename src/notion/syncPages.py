from notion_client import Client
from dotenv import load_dotenv
import os
from datetime import datetime
from pprint import pprint
import json
from notion_client.typing import SyncAsync
from typing import Any
from src.notion.types.PagesTypes import PagesType
from src.notion.helpers.ReformatPage import ReformatPages
from src.notion.helpers.createDoIstTask import createDoIstTask
from queue import Queue
from src.notion.helpers.getParentId import getParentId
from src.notion.helpers.updateDoIstTask import updateDoIstTask
from src.notion.helpers.markDoIstTaskAsIncomplete import markDoIstTaskAsIncomplete
from src.notion.helpers.deleteDoIstTask import deleteDoIstTask
from src.notion.helpers.completeDoIstTask import completeDoIstTask


def syncPages(client: Client, data: any):
    # notion cache contains potentially completed and potentially updated pages.
    with open(os.getcwd() + "/test/notionPage.json", "r") as f:
        cache_pages: dict[str : dict[PagesType]] = json.load(f)
        last_sync_pages = cache_pages.copy()

    new_pages: SyncAsync[Any] = client.databases.query(
        **{
            "database_id": os.getenv("NOTION_DB_ID"),
            "filter": {
                "and": [
                    {"property": "Done", "checkbox": {"equals": False}},
                    {"property": "ToDoistId", "rich_text": {"is_empty": True}},
                ]
            },
        }
    )

    update_pages: SyncAsync[Any] = client.databases.query(
        **{
            "database_id": os.getenv("NOTION_DB_ID"),
            "filter": {
                "and": [
                    {"property": "Done", "checkbox": {"equals": False}},
                    {"property": "ToDoistId", "rich_text": {"is_not_empty": True}},
                ]
            },
        }
    )
    reformatUpdatePages = ReformatPages()
    reformatUpdatePages.reformatPages(update_pages)

    reformatNewPages = ReformatPages()
    reformatNewPages.reformatPages(new_pages)

    # now we want to mark tasks off as completed.

    # TODO: ensure that there is a value for last sync, if not, then dont go through complete pages. if yes, then go through it.

    with open("config.json", "r") as f:
        config_data = json.load(f)

    print(config_data["last_sync"])

    if config_data["last_sync"] != None:
        # TODO: this filter does not appear to work, it returns nothing even though there should be something in there.
        complete_pages: SyncAsync[Any] = client.databases.query(
            **{
                "database_id": os.getenv("NOTION_DB_ID"),
                "filter": {
                    "and": [
                        {"property": "Done", "checkbox": {"equals": True}},
                        {
                            "and": [
                                {
                                    "property": "ToDoistId",
                                    "rich_text": {"is_not_empty": True},
                                },
                                {
                                    "property": "Last edited time",
                                    "last_edited_time": {
                                        "after": config_data["last_sync"]
                                    },
                                },
                            ]
                        },
                    ]
                },
            }
        )

        complete_pages: SyncAsync[Any] = client.databases.query(
            **{
                "database_id": os.getenv("NOTION_DB_ID"),
                "filter": {
                    "and": [
                        {"property": "Done", "checkbox": {"equals": True}},
                        {
                            "and": [
                                {
                                    "property": "ToDoistId",
                                    "rich_text": {"is_not_empty": True},
                                },
                                { #TODO: this doesnt appear to work 
                                    "property": "Last edited time",
                                    "last_edited_time": {
                                        "on_or_after": config_data["last_sync"]
                                    },
                                },
                            ]
                        },
                    ]
                },
            }
        )

        reformatCompletePages = ReformatPages()
        reformatCompletePages.reformatPages(complete_pages)

        print("completed:")
        pprint(complete_pages)
        pprint(reformatCompletePages.reformatted)

        for page in reformatCompletePages.reformatted:
            print(
                "Successfully completed task "
                + reformatCompletePages.reformatted[page]["Name"]
            )
            # TODO: when this is completed, remove it from the cache.
            completeDoIstTask(reformatCompletePages.reformatted[page])
            del cache_pages[page]
            del last_sync_pages[page]

    config_sync = {}

    config_sync["last_sync"] = (
        datetime.now().replace(second=0, microsecond=0).isoformat()
    )

    # TODO: this doesnt seem to work sometimes.
    with open("config.json", "w") as f:
        pprint(config_sync)
        json.dump(config_sync, f, indent=4)
        f.close()

    # first we get all the new pages and add them into todoist. then we get the todoist id back and store this into the associated notion page.

    needs_parent_id: Queue[dict[PagesType]] = Queue()

    for page in reformatNewPages.reformatted:
        if reformatNewPages.reformatted[page]["ParentId"] != None:
            doist_parent_id = getParentId(
                reformatNewPages.reformatted[page]["ParentId"],
                page,
                needs_parent_id,
            )
            if doist_parent_id != None:
                createDoIstTask(
                    page, reformatNewPages.reformatted[page], doist_parent_id
                )
            print(
                "Successfully added task " + reformatNewPages.reformatted[page]["Name"]
            )
        else:
            doist_parent_id = None
            createDoIstTask(page, reformatNewPages.reformatted[page], doist_parent_id)
            print(
                "Successfully added task " + reformatNewPages.reformatted[page]["Name"]
            )

    while needs_parent_id.empty() == False:
        page = needs_parent_id.get()
        doist_parent_id = getParentId(
            reformatNewPages.reformatted[page]["ParentId"],
            page,
            needs_parent_id,
        )

        if doist_parent_id != None:
            createDoIstTask(page, reformatNewPages.reformatted[page], doist_parent_id)
            print(
                "Successfully added task " + reformatNewPages.reformatted[page]["Name"]
            )

    # if there is no notion cache (dict is empty), then we have to add all into ticktick first, otherwise, we add it back again to the existing cache.
    if len(cache_pages) == 0:
        with open(os.getcwd() + "/test/notionPage.json", "w") as f:
            pprint(reformatNewPages.reformatted)
            json.dump(reformatNewPages.reformatted, f)
            f.close()
            print("Saving Notion pages...")
            return
    # if there IS a notion cache, we want to combine the notion cache and reformatNewPages.
    else:
        with open(os.getcwd() + "/test/notionPage.json", "w") as f:
            cache_pages.update(reformatNewPages.reformatted)
            json.dump(cache_pages, f)
            f.close()
            print("Cache Pages found. Adding new pages to the updated pages cache.")

    # get all the pages that already have a doist ID and check with the cache if they were updated.
    for page in reformatUpdatePages.reformatted:
        # determine if there are any changes.
        # first we look up the corresponding page in our cache.

        # TODO this if statement does not work
        # there may be a case where the task was synced but was marked as complete then marked as uncomplete, in that case we want to un-complete the task, but this task does not exist in the cache anymore. so we have to add it back into cache.
        if page not in cache_pages:
            markDoIstTaskAsIncomplete(
                reformatUpdatePages.reformatted[page]["ToDoistId"]
            )
            continue

        cache_page = cache_pages[page]
        # remove the task from the last sync means the task still exists and wasn't deleted.
        del last_sync_pages[page]

        # TODO if the task has a parent id, and the parent id is marked as complete, then we simply SKIP the task, since the child task would be marked as complete by todoist.

        # now loop through the properties.

        for prop in reformatUpdatePages.reformatted[page]:
            if (
                reformatUpdatePages.reformatted[page][prop] != cache_page[prop]
            ):  # in case of a property mismatch, we update.
                print(
                    "Task "
                    + reformatUpdatePages.reformatted[page]["Name"]
                    + " change was found. Attempting to update..."
                )

                # there's a mismatch, so the given page must be updated.
                if reformatUpdatePages.reformatted[page]["ParentId"] != None:
                    doist_parent_id = getParentId(
                        reformatUpdatePages.reformatted[page]["ParentId"],
                        page,
                        needs_parent_id,
                    )
                    if doist_parent_id != None:
                        updateDoIstTask(
                            page, reformatUpdatePages.reformatted[page], doist_parent_id
                        )
                    print(
                        "Successfully updated added task "
                        + reformatUpdatePages.reformatted[page]["Name"]
                    )
                else:
                    doist_parent_id = None
                    updateDoIstTask(
                        page, reformatUpdatePages.reformatted[page], doist_parent_id
                    )
                    print(
                        "Successfully updated task "
                        + reformatUpdatePages.reformatted[page]["Name"]
                    )

    # now we want to see if we have any pages that were deleted, and delete them.
    # TODO: not working.
    for page in last_sync_pages:
        print("Successfully deleted task " + last_sync_pages[page]["Name"])
        deleteDoIstTask(last_sync_pages[page])
        del cache_pages[page]

    with open(os.getcwd() + "/test/notionPage.json", "w") as f:
        cache_pages.update(reformatUpdatePages.reformatted)
        json.dump(cache_pages, f)
        f.close()
        print("Cache Pages found. Adding updated pages to the updated pages cache.")
