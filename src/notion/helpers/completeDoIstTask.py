from src.todoist.auth import doIstAuth
from src.notion.types.PagesTypes import PagesType
from src.todoist.helpers.ReformatTasks import TasksType

def completeDoIstTask(page: PagesType, add_to_doist_cache: TasksType):
    api = doIstAuth()

    api.complete_task(page["ToDoistId"])

    try:
        del add_to_doist_cache[page["ToDoistId"]]
    except:
        print("Completing Notion task to Doist was not defined as key was not found.")
