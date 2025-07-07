import pytz
import json
from datetime import datetime, timezone, date


def changeTimezone(doIstDateTime: str, wholeDate: bool):

    with open("config.json", "r") as f:
        config_data = json.load(f)

    if config_data["timezone"] == "" or config_data["timezone"] == None:
        raise ValueError(
            "Timezone was not specified in config. Please specify a timezone."
        )

    local_timezone = pytz.timezone(config_data["timezone"])
    aware_local_time = local_timezone.localize(datetime.fromisoformat(doIstDateTime))

    # Convert to UTC
    utc_time = aware_local_time.astimezone(timezone.utc)

    if wholeDate:
        return utc_time.date()

    return utc_time
