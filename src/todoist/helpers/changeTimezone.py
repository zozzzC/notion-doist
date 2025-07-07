import pytz
import json
from datetime import datetime, timezone


def changeTimezone(doIstDateTime: str):
   
    with open("config.json", "r") as f: 
        config_data = json.load(f)
    
    if (config_data["timezone"] == "" or config_data["timezone"] == None): 
        raise ValueError("Timezone was not specified in config. Please specify a timezone.")
    
    
    local_timezone = pytz.timezone("Pacific/Auckland")
    aware_local_time = local_timezone.localize(datetime.fromisoformat(doIstDateTime))

    # Convert to UTC
    utc_time = aware_local_time.astimezone(timezone.utc)
    return utc_time
