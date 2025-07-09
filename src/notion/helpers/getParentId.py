from src.notion.types.NotionTypes import NotionPropsType
from src.notion.types.PagesTypes import PagesType
from queue import Queue
from pprint import pprint
from src.notion.auth import notionAuth
import os
from src.notion.helpers.ReformatPage import ReformatPages
import json


def getParentId(
    parent_page_id: str,
    child_page: dict[PagesType],
    needs_parent_id: Queue[dict[PagesType]],
):
    # given a notion page with a relation, we want to get the TODOIST parent id.
    # we can check this by going through our pages dict and seeing if the given parent id has a corresponding doIst id.

    client = notionAuth()
    with open(("config.json"), "r") as file:
        config_data = json.load(file)
        file.close()

    pagesWithDoistId = client.databases.query(
        **{
            "database_id": config_data["notion_db_id"],
            "filter": {
                "and": [
                    {"property": "ToDoistId", "rich_text": {"is_not_empty": True}},
                ]
            },
        }
    )

    reformatPages = ReformatPages()
    reformatPages.reformatPages(pagesWithDoistId)

    # TODO: still not working i think.
    # still some errors with the queue.

    if parent_page_id in reformatPages.reformatted:
        print("Parent Page doIst ID was found.")
        return reformatPages.reformatted[parent_page_id]["ToDoistId"]

    # if it DOESNT, then that means we add this to the queue to be processed later.
    print("Parent Page doIst ID was not found. Adding child page to queue.")
    needs_parent_id.put(child_page)
    return None
