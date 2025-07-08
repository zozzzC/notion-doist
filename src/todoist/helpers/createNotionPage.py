from dotenv import load_dotenv
import os
from notion_client import Client
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task
import datetime
import pprint
from src.notion.auth import notionAuth
from src.todoist.auth import doIstAuth
from src.todoist.helpers.formatLabel import formatLabel
import json


def createNotionPage(
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
):

    client = notionAuth()

    create = {
        "Name": {"title": [{"text": {"content": name}}]},
        "ToDoistId": {"rich_text": [{"type": "text", "text": {"content": toDoIstId}}]},
        # "Deadline": {"date": {"end": None, "start": '', "time_zone": None}},
        # "Date": {"date": {"end": None, "start": '', "time_zone": None}},
        # "Priority Level": {"select": {"name": None}},
        # "Project": {"select": [{"name": None}]},
        # "Section": {"select": [{"name": None}]},
        # "Tag": {
        #     "multi-select": [
        #         # this must be multiple if there is more than one tag, so the
        #         # values here must be calculated beforehand in a loop
        #         {"name": None}
        #     ]
        # },
    }

    print("Timezone:")
    print(time_zone)

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
        create.update({"Parent": {"type": "relation", "relation": [{"id": parent_id}]}})

    with open(("config.json"), "r") as file:
        config_data = json.load(file)

    client.pages.create(
        parent={"database_id": config_data["notion_db_id"]}, properties=create
    )

    print("Successfully created Notion page for " + name)
