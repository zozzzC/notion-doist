from dotenv import load_dotenv
import os
from notion_client import Client
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task


def createNotionPage(name: str, client: Client, api: TodoistAPI):

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

    client.pages.create(
        parent={"database_id": os.getenv("NOTION_DB_ID")}, properties=create
    )
