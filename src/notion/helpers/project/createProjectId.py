from src.todoist.auth import doIstAuth


def createProjectId(project_name: str):
    api = doIstAuth()
    project = api.add_project(name=project_name)
    return project.id
