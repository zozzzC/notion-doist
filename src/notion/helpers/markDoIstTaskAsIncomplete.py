from src.todoist.auth import doIstAuth
from src.todoist.helpers.ReformatTasks import TasksType, TaskPropsType
from src.notion.types.PagesTypes import PagesType
from src.notion.helpers.lookupPageByTodoistId import lookupPageByTodoistId
from src.todoist.helpers.markNotionPageAsIncomplete import markNotionPageAsIncomplete


def markDoIstTaskAsIncomplete(
    notionId: str, doIstId: str, add_to_doist_cache: TasksType
):
    api = doIstAuth()
    api.uncomplete_task(task_id=doIstId)
    task = api.get_task(task_id=doIstId)

    duration_amount = None
    duration_unit = None
    due_timezone = None
    due_datetime = None
    due = None
    recurring = False
    if task.duration != None:
        duration_amount = task.duration.amount
        duration_unit = task.duration.unit

    if task.due != None:
        due_datetime = task.due.date.isoformat()
        due_timezone = task.due.timezone
        due = task.due.date.isoformat()
        recurring = task.due.is_recurring

    add_to_doist_cache[notionId] = {
        "content": task.content,
        "duration": duration_amount,
        "duration_unit": duration_unit,
        "datetime": due_datetime,
        "description": task.description,
        "parent_id": task.parent_id,
        "is_completed": False,
        "labels": task.labels,
        "timezone": due_timezone,
        "priority": task.priority,
        "project_id": task.project_id,
        "section_id": task.section_id,
        "due": due,
        "recurring": recurring,
    }

    # if we are a child task, then the parent tasks will also be marked as incomplete. in that case, we must:
    # add the parent task into the add_to_doist_cache dict
    # change this accordingly in notion

    parent_id = task.parent_id

    if parent_id != None:
        markDoIstTaskAsIncomplete(
            lookupPageByTodoistId(parent_id), parent_id, add_to_doist_cache
        )
        markNotionPageAsIncomplete(
            lookupPageByTodoistId(parent_id)
        )  # mark the parent as incomplete in notion
