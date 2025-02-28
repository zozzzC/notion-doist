import datetime


def formatToDoIstDate(due: str, dt: str | None):
    dueReformat = datetime.datetime.strptime(due, "YYYY-MM-DD").isoformat()

    if dt:
        dtReformat = datetime.datetime.strptime(
            dt, "yyyy-mm-ddThh:mm:ss.msZ"
        ).isoformat()
        return dueReformat, dtReformat

    return dueReformat
