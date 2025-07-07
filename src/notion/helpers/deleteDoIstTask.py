from src.todoist.auth import doIstAuth
from src.notion.types.PagesTypes import PagesType


def deleteDoIstTask(page: PagesType):
    api = doIstAuth()

    api.delete_task(page["ToDoistId"])
