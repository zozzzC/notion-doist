from src.todoist.auth import doIstAuth
from pprint import pprint


def getProjectId(project_name: str) -> str | None:
    api = doIstAuth()

    projects_list = api.get_projects(100)

    for project in next(projects_list):
        if project.name == project_name:
            return project.id

    return None
