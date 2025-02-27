from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task
from notion_client import Client
import os
import json
from pprint import pprint

type tasksType = dict[
    str,
    dict[
        str,
        str | None,
        str,
        str,
        str | None,
        bool,
        list[str | None],
        str | None,
        int,
        str,
        bool,
    ],
]


def reformatTasks(tasks: list[Task]) -> dict[str : dict[tasksType]]:
    reformatted_tasks: dict[str : dict[tasksType]] = {}

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

    return reformatted_tasks


def syncTasks(client: Client, api: TodoistAPI, data: any):
    tasks: list[Task] = api.get_tasks()
    reformatted_tasks: dict[str : dict[tasksType]] = reformatTasks(tasks)

    if len(data) == 0:
        with open(os.getcwd() + "/src/sample/doIstTask.json", "w") as f:
            print("Saving doIst tasks...")
            json.dump(reformatted_tasks, f)
            f.close()
    else:
        with open(os.getcwd() + "/src/sample/doIstProject.json", "r") as f:
            cache_tasks: dict[str : dict[tasksType]] = json.load(f)

            # check for added and updated projects
            for t in reformatted_tasks:
                if t in cache_tasks:
                    for label in cache_tasks[t]:
                        # o is the name of the title EG: name, url, is_favourite
                        # cache_projects[p].get(o) is the name of the value EG: coding, http..., true
                        # print(o)
                        # print(cache_projects[p].get(o))

                        if cache_tasks[t].get(label) != reformatted_tasks[t].get(label):
                            updateTaskInNotion(client, t, reformatted_tasks)
                            break
                else:
                    addProjectInNotion(t)

            # check for deleted projects
            for ct in cache_tasks:
                if ct not in reformatted_tasks:
                    deleteProjectInNotion(t)


def updateTaskInNotion(client, t, reformatted_tasks):
    print("Updating doIst task into Notion...")
     


def addProjectInNotion(client, p, reformatted_projectsp):
    print("add")


def deleteProjectInNotion(client: Client, p):
    print("delete")
