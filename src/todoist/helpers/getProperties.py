from notion_client import Client
from dotenv import load_dotenv
import os


def getProperties(page):
    res = page.get("results")[1].get("properties")
    return res
