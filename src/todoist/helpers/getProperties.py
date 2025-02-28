from notion_client import Client
from dotenv import load_dotenv
import os


def getResults(query):
    return query.get("results")


def getProperties(page):
    res = {}
    for i in range(0, len(page)):
        res.update({page[i].get("id"): page[i].get("properties")})

    return res
