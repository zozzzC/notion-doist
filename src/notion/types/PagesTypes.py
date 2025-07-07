from typing import TypedDict, DefaultDict


class DatePagesType(TypedDict):
    end: str | None
    start: str | None


class PagesType(TypedDict):
    Date: DatePagesType | None
    Deadline: DatePagesType | None
    Label: DefaultDict | None
    Name: str
    ParentId: str | None
    Priority_Level: str
    Project: str | None
    Section: str | None
    ToDoistId: str | None
    Status: bool
