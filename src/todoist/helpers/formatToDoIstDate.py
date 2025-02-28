import datetime
import pytz


def formatToDoIstDate(due: str):
    dueReformat = datetime.datetime.strptime(due, "YYYY-MM-DD").isoformat()

    return dueReformat
