from src.notion.syncRelations import syncRelations
from src.todoist.syncTasks import tasksType


def checkForRelation(
    reformatted_tasks: dict[str : dict[tasksType]],
):
    print(
        "this must check for a relation for some task, and if so, then we must then add this relation into notion"
    )
    for t in reformatted_tasks:
        print("reformatted task todoist id: " + reformatted_tasks[t])
        syncRelations(reformatted_tasks[t], t.get("parent_id"))
