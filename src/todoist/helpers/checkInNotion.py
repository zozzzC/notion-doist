from src.todoist.helpers.ReformatTasks import TaskPropsType
from src.notion.auth import notionAuth
import os
import json


def checkInNotion(todoistId: str):
    client = notionAuth()
    with open(("config.json"), "r") as file:
        config_data = json.load(file)

    page = client.databases.query(
        **{
            "database_id": config_data["notion_db_id"],
            "filter": {"property": "ToDoistId", "rich_text": {"equals": todoistId}},
        }
    )

    if len(page["results"]) != 0:
        return page["results"][0]["id"]

    return None
