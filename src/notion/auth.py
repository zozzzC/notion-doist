import os
from notion_client import Client


def notionAuth() -> Client:
    try:
        notion = Client(auth=os.environ["NOTION_TOKEN"])
        return notion
    except:
        print("Notion Token is not initialized.")
