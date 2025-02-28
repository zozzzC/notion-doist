from dotenv import load_dotenv
import os
from notion_client import Client
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task
import datetime

from src.notion.auth import notionAuth
from src.todoist.auth import doIstAuth


def createNotionPage(
    name: str,
    date: datetime.datetime | None,
    end_date: datetime.datetime | None,
    due: datetime.datetime | None,
    priority: str | None,
    project: str | None,
    section: str | None,
    tag: list[str] | None,
):

    client = notionAuth()
    api = doIstAuth()

    create = {
        "Name": {"title": [{"text": {"content": name}}]},
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

    if date:
        if end_date:
            create.update({"Date": {"date": {"start": str(date), "time_zone": None}}})
        else:
            create.update(
                {
                    "Date": {
                        "date": {
                            "end": str(end_date),
                            "start": str(date),
                            "time_zone": None,
                        }
                    }
                }
            )

    client.pages.create(
        parent={"database_id": os.getenv("NOTION_DB_ID")}, properties=create
    )
