from src.notion.auth import notionAuth
from src.todoist.auth import doIstAuth


def lookupProject(project_id: str):
    api = doIstAuth()
    

    return api.get_project(project_id).name
