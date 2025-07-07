from src.todoist.auth import doIstAuth
from src.notion.types.PagesTypes import PagesType


def completeDoIstTask(page: PagesType):
    api = doIstAuth()

    api.complete_task(page["ToDoistId"])
