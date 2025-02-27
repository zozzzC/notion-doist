from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Project
from notion_client import Client
import os
import json
from pprint import pprint

type projectsType = dict[str, dict[str | None, str, bool, str]]


def syncTasks(client: Client, api: TodoistAPI, data: any):
    tasks = api.get_tasks()
    reformatted_tasks: dict[str : dict[tasks]] = {}

    for t in tasks:
        if t.due:
            reformatted_due = {
                "due": t.due.date,
                "recurring": t.due.is_recurring,
                "datetime": t.due.datetime,
            }

        reformatted_tasks.update(
            {
                t.id: {
                    "is_completed": t.is_completed,
                    "content": t.content,
                    "description": t.description,
                    "parent_id": t.parent_id,
                    "project_id": t.project_id,
                    "labels": t.labels,
                    "priority": t.priority,
                    "duration": t.duration,
                }
            }
        )

        reformatted_tasks.get(t.id).update(reformatted_due)

        pprint(reformatted_tasks)


#     if len(data) == 0:
#         with open(os.getcwd() + "/src/sample/doIstProject.json", "w") as f:
#             print("Saving doIst projects...")
#             json.dump(reformatted_projects, f)
#             f.close()
#     else:
#         with open(os.getcwd() + "/src/sample/doIstProject.json", "r") as f:
#             cache_projects: dict[str : dict[projectsType]] = json.load(f)

#             # check for added and updated projects
#             for p in reformatted_projects:
#                 if p in cache_projects:
#                     for label in cache_projects[p]:
#                         # o is the name of the title EG: name, url, is_favourite
#                         # cache_projects[p].get(o) is the name of the value EG: coding, http..., true
#                         # print(o)
#                         # print(cache_projects[p].get(o))

#                         if cache_projects[p].get(label) != reformatted_projects[p].get(
#                             label
#                         ):
#                             updateProjectInNotion(client, p, reformatted_projects)
#                             break
#                 else:
#                     addProjectInNotion(p)

#             # check for deleted projects
#             for cp in cache_projects:
#                 if cp not in reformatted_projects:
#                     deleteProjectInNotion(p)


# def updateProjectInNotion(client, p, reformatted_projects):
#     print("update")


# def addProjectInNotion(client, p, reformatted_projectsp):
#     print("add")


# def deleteProjectInNotion(client: Client, p):
#     print("delete")
