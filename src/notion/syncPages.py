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

    reformatCompletePages = ReformatPages()
    reformatCompletePages.reformatPages(complete_pages)

    reformatNewPages = ReformatPages()
    reformatNewPages.reformatPages(new_pages)

    reformatUpdatePages = ReformatPages()
    reformatUpdatePages.reformatPages(update_pages)

    # notion cache contains potentially completed and potentially updated pages.
    with open(os.getcwd() + "/test/notionpage.json", "r") as f:
        cache_pages: dict[str : dict[pagesType]] = json.load(f)

    # first we get all the new pages and add them into todoist. then we get the todoist id back and store this into the associated notion page.

    needs_parent_id: Queue[dict[pagesType]] = Queue()

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

    print("Now looping through create queue...")
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

    # for page in reformatUpdatePages.reformatted:

    # # if there is no notion cache (dict is empty), then we have to add all into ticktick first, otherwise, we add it back again to the existing cache.
    # if len(cache_pages) == 0:
    #     with open(os.getcwd() + "/test/notionpage.json", "w") as f:
    #         print("Saving Notion pages...")
    #         json.dump(reformatNewPages.reformatted, f)
    #         f.close()

    # get all the pages that already have a doist ID and check with the cache if they were updated.
