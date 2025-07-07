from datetime import datetime


def getTime(date: str):
    try:
        datetime_object = datetime.fromisoformat(date)
        contains_time = False
        contains_time = (
            datetime_object.hour != 0
            or datetime_object.minute != 0
            or datetime_object.second != 0
            or datetime_object.microsecond != 0
        )
        if contains_time:
            return datetime_object.time()
        return None
    except:
        raise ValueError("Date string is not ISO.")
