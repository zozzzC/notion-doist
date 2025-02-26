import os
from notion_client import Client
from dotenv import load_dotenv


def notionAuth() -> Client:
    try:
        notion = Client(auth=os.getenv("NOTION_TOKEN"))
        return notion
    except:
        print("Notion Token was not initialized.")
