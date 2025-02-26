import notion_client
import todoist_api_python
from notion.auth import notionAuth
from todoist.auth import doIstAuth
from __init__ import __init__
from todoist.syncProjects import syncProjects
import json
import os


def main():
    client = notionAuth()
    api = doIstAuth()
    
    # try:
    with open((os.getcwd() + "/src/sample/doIstProject.json"), "r") as file:
        data = json.load(file)
        syncProjects(api, data)
    # except:
    #     print("Error reading JSON.")


main()
