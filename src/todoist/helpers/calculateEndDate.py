import datetime


def calculateEndDate(start_date: datetime.datetime, duration: int, duration_unit: str):
    endDate = start_date + datetime.timedelta(duration_unit + "=" + duration)
    return endDate
