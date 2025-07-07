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
from src.notion.helpers.removeCompletedPages import removeCompletedPages
from src.notion.helpers.getCompletedPages import getCompletedPages
from src.todoist.helpers.changeTimezone import changeTimezone
from pprint import pprint


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

    reformatNewPages = ReformatPages()
    reformatNewPages.reformatPages(new_pages)

    with open("config.json", "r") as f:
        config_data = json.load(f)

    if config_data["last_sync"] != None:

        update_pages: SyncAsync[Any] = client.databases.query(
            **{
                "database_id": os.getenv("NOTION_DB_ID"),
                "filter": {
                    "and": [
                        {
                            "timestamp": "last_edited_time",
                            "last_edited_time": {"after": config_data["last_sync"]},
                        },
                        {"property": "ToDoistId", "rich_text": {"is_not_empty": True}},
                    ]
                },
            }
        )
        reformatUpdatePages = ReformatPages()
        reformatUpdatePages.reformatPages(update_pages)

        complete_pages = getCompletedPages(reformatUpdatePages.reformatted)
        reformatUpdatePages.reformatted = removeCompletedPages(
            reformatUpdatePages.reformatted, complete_pages
        )

        for page in complete_pages:
            print("Successfully completed task " + complete_pages[page]["Name"])
            completeDoIstTask(complete_pages[page])
            del cache_pages[page]
            del last_sync_pages[page]

    config_sync = {}

    config_sync["last_sync"] = changeTimezone(
        datetime.now().replace(second=0, microsecond=0).isoformat()
    ).isoformat()
    # NOTE: last_sync is in UTC time since this is the time used in notion.

    with open("config.json", "w") as f:
        pprint(config_sync)
        json.dump(config_sync, f, indent=4)
        f.close()

    # get all the new pages and add them into todoist. then we get the todoist id back and store this into the associated notion page.

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

        # there may be a case where the task was synced but was marked as complete then marked as uncomplete, in that case we want to un-complete the task, but by then task does not exist in the notion cache anymore. so we have to add it back into cache.
        if page not in cache_pages:
            markDoIstTaskAsIncomplete(
                reformatUpdatePages.reformatted[page]["ToDoistId"]
            )
            # add back into cache
            cache_pages[page] = reformatUpdatePages.reformatted[page]
            continue

        cache_page = cache_pages[page]

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
    # to do this we compare all the pages currently in notion VS the last sync. delete if we find a match for all items currently in notion. then the remaining items in last sync are now the tasks that are deleted, so we delete it in doist.

    all_pages: SyncAsync[Any] = client.databases.query(
        **{
            "database_id": os.getenv("NOTION_DB_ID"),
            "filter": {"property": "ToDoistId", "rich_text": {"is_not_empty": True}},
        }
    )

    reformatAllPages = ReformatPages()
    reformatAllPages.reformatPages(all_pages)

    last_sync_copy = last_sync_pages.copy()

    for page in reformatAllPages.reformatted:
        if page in last_sync_copy:
            del last_sync_pages[page]

    for page in last_sync_pages:
        print("Successfully deleted task " + last_sync_pages[page]["Name"])
        deleteDoIstTask(last_sync_pages[page])
        del cache_pages[page]

    with open(os.getcwd() + "/test/notionPage.json", "w") as f:
        cache_pages.update(reformatUpdatePages.reformatted)
        json.dump(cache_pages, f)
        f.close()
        print("Cache Pages found. Adding updated pages to the updated pages cache.")
