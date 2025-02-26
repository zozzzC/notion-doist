from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Project
import os
import json


def syncProjects(api: TodoistAPI, data: any):

    projects = api.get_projects()
    print(projects)
    reformatted_projects = []

    for p in projects:
        reformatted_projects.append(
            {
                "id": p.id,
                "parent_id": p.parent_id,
                "name": p.name,
                "is_favourite": p.is_favorite,
                "url": p.url,
            }
        )

    print(reformatted_projects)

    if len(data) == 0:
        with open(os.getcwd() + "/src/sample/doIstProject.json", "w") as f:
            json.dump(reformatted_projects, f)
            f.close()
    else:
        with open(os.getcwd() + "/src/sample/doIstProject.json", "w") as f:
            print("files exist")
