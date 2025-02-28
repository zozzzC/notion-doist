import datetime
import pytz


def formatToDoIstDate(due: str, dt: str | None, timezone: str):
    utcTimezone = pytz.timezone("UTC")
    myTimezone = pytz.timezone(timezone)

    dueReformat = utcTimezone.localize(
        datetime.datetime.strptime(due, "YYYY-MM-DD").isoformat()
    ).astimezone(myTimezone)

    if dt:
        dtReformat = utcTimezone.localize(
            datetime.datetime.strptime(dt, "yyyy-mm-ddThh:mm:ss.msZ").isoformat()
        ).astimezone(myTimezone)

        return dueReformat, dtReformat

    return dueReformat
