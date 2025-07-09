import os
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI
import json


def doIstAuth() -> TodoistAPI:
    try:
        with open(("config.json"), "r") as file:
            config_data = json.load(file)
            file.close()
        api = TodoistAPI(config_data["todoist_token"])
        return api
    except:
        print("Todoist Token was not initialized.")
