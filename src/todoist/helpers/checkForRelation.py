from src.todoist.syncTasks import tasksType

def checkForRelation (
    t: dict[
        "content":str,
        "duration" : str | None,
        "duration_unit" : str | None,
        "datetime" : str | None,
        "description":str,
        "parent_id" : str | None,
        "is_completed":bool,
        "labels" : list[str | None],
        "timezone" : str | None,
        "priority":int,
        "project_id" : str | None,
        "section_id" : str | None,
        "due" : str | None,
        "recurring":bool,
        "parent_id" : str | None
    ],
    reformatted_tasks: dict[str : dict[tasksType]],):
    print("this must check for a relation for some task, and if so, then we must then add this relation into notion")
    
    syncRelations()