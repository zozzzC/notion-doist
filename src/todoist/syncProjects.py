from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Project
from notion_client import Client
import os
import json

type projectsType = dict[str, dict[str | None, str, bool, str]]


def syncProjects(client: Client, api: TodoistAPI, data: any):
    projects = api.get_projects()
    reformatted_projects: dict[str : dict[projectsType]] = {}

    for p in projects:
        reformatted_projects.update(
            {
                p.id: {
                    "parent_id": p.parent_id,
                    "name": p.name,
                    "is_favourite": p.is_favorite,
                    "url": p.url,
                }
            }
        )

    if len(data) == 0:
        with open(os.getcwd() + "/src/sample/doIstProject.json", "w") as f:
            print("Saving doIst projects...")
            json.dump(reformatted_projects, f)
            f.close()
    else:
        with open(os.getcwd() + "/src/sample/doIstProject.json", "r") as f:
            cache_projects: dict[str : dict[projectsType]] = json.load(f)

            # check for added and updated projects
            for p in reformatted_projects:
                if p in cache_projects:
                    for label in cache_projects[p]:
                        # o is the name of the title EG: name, url, is_favourite
                        # cache_projects[p].get(o) is the name of the value EG: coding, http..., true
                        # print(o)
                        # print(cache_projects[p].get(o))

                        if cache_projects[p].get(label) != reformatted_projects[p].get(
                            label
                        ):
                            updateProjectInNotion(client, p, reformatted_projects)
                            break
                else:
                    addProjectInNotion(p)

            # check for deleted projects
            for cp in cache_projects:
                if cp not in reformatted_projects:
                    deleteProjectInNotion(p)


def updateProjectInNotion(client, p, reformatted_projects):
    print("update")


def addProjectInNotion(client, p, reformatted_projectsp):
    print("add")


def deleteProjectInNotion(client: Client, p):
    print("delete")
