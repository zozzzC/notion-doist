from src.notion.auth import notionAuth
import os
from dotenv import load_dotenv
from src.todoist.helpers import getProperties
from pprint import pprint


def lookupPage(id: str, propertyName: str):
    client = notionAuth()

    try:
        res = getProperties(
            getProperties.getResults(
                client.databases.query(
                    **{
                        "database_id": os.getenv("NOTION_DB_ID"),
                        "filter": {
                            "property": propertyName,
                            "title": [{"text": {"content": id}}],
                        },
                    }
                )
            )
        )

        pprint(res)

        return res
    except:
        raise Exception(
            "Cannot find page with ID " + id + " for property " + propertyName
        )
