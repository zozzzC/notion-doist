from src.notion.syncRelations import syncRelations
from src.todoist.helpers.ReformatTasks import tasksType


def checkForRelation(
    reformatted_tasks: dict[str : dict[tasksType]],
):
    for t in reformatted_tasks:
        print("t: " + t)
        print("reformatted task todoist id: " + reformatted_tasks[t])
        syncRelations(reformatted_tasks[t], t.get("parent_id"))
