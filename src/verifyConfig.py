import json
from typing import TypedDict


class ConfigType(TypedDict):
    last_sync: str | None
    notion_token: str
    todoist_token: str
    notion_db_id: str
    notion_db_url: str
    timezone: str


def verifyConfig():
    with open("config.json", "r") as f:
        config_data = json.load(f)

    try:
        ConfigType(config_data)

    except:
        raise ValueError(
            "Config file was not filled out properly. Please be sure to fill in all values EXCEPT for last_sync."
        )
