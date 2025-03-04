import datetime


def formatToDoIstDateTime(due: str):
    dueReformat = datetime.datetime.strptime(due, "%Y-%m-%dT%H:%M:%S").isoformat()

    return dueReformat
