from dotenv import load_dotenv
import os
from notion_client import Client
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task
import datetime
from pprint import pprint
from src.notion.auth import notionAuth
from src.todoist.auth import doIstAuth
from src.todoist.helpers.formatLabel import formatLabel


def updateNotionPage(
    toDoIstId: str,
    name: str,
    date: datetime.datetime | None,
    end_date: datetime.datetime | None,
    time_zone: str,
    due: datetime.datetime | None,
    priority: str | None,
    project: str | None,
    section: str | None,
    tag: list[str] | None,
    parent_id: str | None,
    notion_id: str,
):

    client = notionAuth()

    create = {
        "Name": {"title": [{"text": {"content": name}}]},
    }

    if date:
        if end_date:
            create.update(
                {
                    "Date": {
                        "date": {
                            "end": str(end_date),
                            "start": str(date),
                            "time_zone": time_zone,
                        }
                    }
                }
            )
        else:
            create.update({"Date": {"date": {"start": str(date), "time_zone": None}}})

    if due:
        create.update({"Deadline": {"date": {"start": str(date), "time_zone": None}}})

    if priority:
        create.update({"Priority Level": {"select": {"name": priority}}})

    print(project)

    if project:
        create.update({"Project": {"select": {"name": project}}})

    if section:
        create.update({"Section": {"select": {"name": section}}})

    if tag:
        create.update({"Label": {"multi_select": formatLabel(tag)}})

    if parent_id:
        create.update({"Parent": [{"id": parent_id}]})

    pprint({"page_id": notion_id, "properties": create})

    if notion_id == None:
        # then the associated task was alredy deleted in notion, so don't bother updating it.
        print(
            "Notion page with ToDoIst ID:"
            + toDoIstId
            + " Name:"
            + name
            + " was already deleted."
        )
        return

    client.pages.update(
        page_id=notion_id,
        properties=create,
    )

    print("Successfully updated Notion page for " + name)
