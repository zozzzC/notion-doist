from src.todoist.helpers.ReformatTasks import TaskPropsType
from src.notion.auth import notionAuth
import os


def checkInNotion(todoistId: str):
    client = notionAuth()

    page = client.databases.query(
        **{
            "database_id": os.getenv("NOTION_DB_ID"),
            "filter": {"property": "ToDoistId", "rich_text": {"equals": todoistId}},
        }
    )

    if len(page["results"]) != 0:
        return page["results"][0]["id"]

    return None
