from notion.auth import notionAuth
from todoist.auth import doIstAuth
from todoist_api_python.api import TodoistAPI
from notion_client import Client

def __init__():
    client = notionAuth()
    api = doIstAuth()
    return client, api;



