import pytz
from datetime import datetime, timezone


def changeTimezone(doIstDateTime: str):
    local_timezone = pytz.timezone("Pacific/Auckland")
    aware_local_time = local_timezone.localize(datetime.fromisoformat(doIstDateTime))

    # Convert to UTC
    utc_time = aware_local_time.astimezone(timezone.utc)
    return utc_time
