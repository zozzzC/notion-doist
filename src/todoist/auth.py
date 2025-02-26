import os
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI


def doIstAuth() -> TodoistAPI:
    try:
        api = TodoistAPI(os.getenv("TODOIST_TOKEN"))
        return api
    except:
        print("Todoist Token was not initialized.")
