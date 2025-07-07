from src.notion.syncRelations import syncRelations
from src.todoist.helpers.ReformatTasks import TasksType


def checkForRelation(reformatted_tasks: TasksType):
    for t in reformatted_tasks:
        syncRelations(reformatted_tasks[t], t.get("parent_id"))
