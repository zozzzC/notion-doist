from pprint import pprint
import notion_client
import todoist_api_python
from notion.auth import notionAuth
from src.todoist.helpers.createNotionPage import createNotionPage
from src.todoist.helpers.getProperties import getProperties, getResults
from todoist.auth import doIstAuth
from __init__ import __init__
from src.notion.syncPages import syncPages
from todoist.syncTasks import syncTasks
import json
import os
from verifyConfig import verifyConfig
from getDefaultPath import getDefaultPath


def main():
    verifyConfig()
    client = notionAuth()
    api = doIstAuth()
    default_path = getDefaultPath()
    try:
        with open((default_path + "doIstTask.json"), "r") as file:
            data = json.load(file)
            file.close()
    except:
        print("Error reading Todoist Cache.")

    syncTasks(api, data)

    try:
        with open((default_path + "notionPage.json"), "r") as file:
            data = json.load(file)
            file.close()
    except:
        print("Error reading Notion cache.")

    syncPages(client, cache_pages=data)


main()
