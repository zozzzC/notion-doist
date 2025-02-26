import os
from todoist_api_python.api import TodoistAPI


def doIstAuth() -> TodoistAPI:
    try:
        api = TodoistAPI(os.environ(["TODOIST_TOKEN"]))
        return api
    except:
        print("Todoist Token is not initialized.")
