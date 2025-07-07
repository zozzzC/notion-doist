from src.todoist.auth import doIstAuth
def markDoIstTaskAsIncomplete(doIstId: str): 
    api = doIstAuth()
    api.uncomplete_task(task_id=doIstId)