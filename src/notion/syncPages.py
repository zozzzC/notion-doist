from notion_client import Client
from dotenv import load_dotenv
import os
from pprint import pprint
from notion_client.typing import SyncAsync
from typing import Any
from src.notion.helpers.ReformatPage import ReformatPages


def syncPages(client: Client, data: any):
    # first call is to get pages that are complete
    # second call is to get pages that are not complete

    complete_pages: SyncAsync[Any] = client.databases.query(
        **{
            "database_id": os.getenv("NOTION_DB_ID"),
            "filter": {"property": "Done", "checkbox": {"equals": True}},
        }
    )

    pages: SyncAsync[Any] = client.databases.query(
        **{
            "database_id": os.getenv("NOTION_DB_ID"),
            "filter": {"property": "Done", "checkbox": {"equals": False}},
        }
    )

    # pprint(pages["results"])
    
    
    reformatPages = ReformatPages()
    reformatPages.reformatPages(pages)


    
#NOTE: datetime start and end dates are one entire day behind for some reason. so we need to fix that offset. 

