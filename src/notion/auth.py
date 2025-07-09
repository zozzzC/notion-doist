import os
from notion_client import Client
from dotenv import load_dotenv
import json


def notionAuth() -> Client:
    try:
        with open(("config.json"), "r") as file:
            config_data = json.load(file)
            notion = Client(auth=config_data["notion_token"])
            file.close()
            return notion
    except:
        print("Notion Token was not initialized.")
