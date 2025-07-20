from src.todoist.auth import doIstAuth
from src.notion.types.PagesTypes import PagesType
from src.todoist.helpers.ReformatTasks import TasksType


def checkIsCompleteDoIstTask(task_id: str):
    api = doIstAuth()
    try:
        doist_task = api.get_task(task_id)
        return doist_task.is_completed
    except:
        print("DoIst task with ID %s was not found", task_id)
