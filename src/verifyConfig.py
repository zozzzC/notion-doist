import json
import pytz
from jsonschema import validate

config_schema = {
    "type": "object",
    "properties": {
        "last_sync": {"type": ["string", "null"]},
        "notion_token": {"type": "string"},
        "todoist_token": {"type": "string"},
        "notion_db_id": {"type": "string"},
        "notion_db_url": {"type": "string"},
        "timezone": {"type": "string"},
    },
    "additionalProperties": False,
    "minProperties": 6,
}


def verifyConfig():
    with open("config.json", "r") as f:
        config_data = json.load(f)

    try:
        validate(instance=config_data, schema=config_schema)
        # check that timezone is a vlid timezone.

        if config_data["timezone"] in pytz.all_timezones:
            print("Config data is valid!")
        else:
            raise ValueError(
                "Timezone is not a valid tz timezone. Please ensure this is valid. (See: http://en.wikipedia.org/wiki/List_of_tz_database_time_zones for a list of valid timezones.)"
            )
    except:
        raise ValueError(
            "Config file was not filled out properly. Please be sure to fill in all values EXCEPT for last_sync."
        )
