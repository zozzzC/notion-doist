from pprint import pprint
import notion_client
import todoist_api_python
from notion.auth import notionAuth
from src.todoist.helpers.createNotionPage import createNotionPage
from src.todoist.helpers.getProperties import getProperties, getResults
from todoist.auth import doIstAuth
from __init__ import __init__

from todoist.syncTasks import syncTasks
import json
import os


def main():
    client = notionAuth()
    api = doIstAuth()
    # res = getProperties(
    #     getResults(
    #         client.databases.query(
    #             **{
    #                 "database_id": os.getenv("NOTION_DB_ID"),
    #                 "filter": {"property": "Done", "checkbox": {"equals": True}},
    #             }
    #         )
    #     )
    # )

    # pprint(res)

    # createNotionPage("me", client, api)

    # try:
    with open((os.getcwd() + "/test/doIstTask.json"), "r") as file:
        data = json.load(file)
        syncTasks(client, api, data)
    # except:
    #     print("Error reading JSON.")


main()
