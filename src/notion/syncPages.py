from notion_client import Client
from dotenv import load_dotenv
import os
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


def syncPages(client: Client, data: any):
    # first call is to get pages that are complete
    # second call is to get pages that are not complete

    complete_pages: SyncAsync[Any] = client.databases.query(
        **{
            "database_id": os.getenv("NOTION_DB_ID"),
            "filter": {
                "and": [
                    {"property": "Done", "checkbox": {"equals": True}},
                    {"property": "ToDoistId", "rich_text": {"is_not_empty": True}},
                ]
            },
        }
    )

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

    reformatCompletePages = ReformatPages()
    reformatCompletePages.reformatPages(complete_pages)

    reformatNewPages = ReformatPages()
    reformatNewPages.reformatPages(new_pages)

    # notion cache contains potentially completed and potentially updated pages.
    with open(os.getcwd() + "/test/notionPage.json", "r") as f:
        cache_pages: dict[str : dict[PagesType]] = json.load(f)

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

    pprint(reformatUpdatePages)
    # get all the pages that already have a doist ID and check with the cache if they were updated.
    for page in reformatUpdatePages.reformatted:
        # determine if there are any changes.
        # first we look up the corresponding page in our cache.

        cache_page = cache_pages[page]

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

    with open(os.getcwd() + "/test/notionPage.json", "w") as f:
        cache_pages.update(reformatUpdatePages.reformatted)
        json.dump(cache_pages, f)
        f.close()
        print("Cache Pages found. Adding updated pages to the updated pages cache.")
