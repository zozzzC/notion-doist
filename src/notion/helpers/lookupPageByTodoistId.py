from src.notion.auth import notionAuth
import os
from dotenv import load_dotenv
from src.todoist.helpers.getProperties import getProperties, getResults
from pprint import pprint
import json


def lookupPageByTodoistId(todoistId: str):
    client = notionAuth()
    with open(("config.json"), "r") as file:
        config_data = json.load(file)
        file.close()
    try:
        res = getProperties(
            getResults(
                client.databases.query(
                    **{
                        "database_id": config_data["notion_db_id"],
                        "filter": {
                            "property": "ToDoistId",
                            "rich_text": {"contains": todoistId},
                        },
                    }
                )
            )
        )

        if len(list(res.keys())) == 0:
            return None

        return list(res.keys())[0]
    except IndexError:
        raise Exception("Cannot find page with Todoist ID " + todoistId)
