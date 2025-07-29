#!/usr/bin/env python3.12
import json
import os
from pprint import pprint

import notion_client
import todoist_api_python

from __init__ import __init__
from getDefaultPath import getDefaultPath
from notion.auth import notionAuth
from src.notion.syncPages import syncPages
from src.todoist.helpers.createNotionPage import createNotionPage
from src.todoist.helpers.getProperties import getProperties, getResults
from todoist.auth import doIstAuth
from todoist.syncTasks import syncTasks
from verifyConfig import verifyConfig


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
