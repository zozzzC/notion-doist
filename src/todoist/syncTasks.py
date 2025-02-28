from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task
from notion_client import Client
import os
import json
from .helpers.getProperties import getProperties, getResults
from pprint import pprint
from dotenv import load_dotenv

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
                "timezone": t.due.timezone,
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

    return reformatted_tasks


def syncTasks(client: Client, api: TodoistAPI, data: any):
    tasks: list[Task] = api.get_tasks()
    reformatted_tasks: dict[str : dict[tasksType]] = reformatTasks(tasks)

    with open(os.getcwd() + "/test/doIstTask.json", "r") as f:
        cache_tasks: dict[str : dict[tasksType]] = json.load(f)

    if len(data) == 0:
        with open(os.getcwd() + "/test/doIstTask.json", "w") as f:
            print("Saving doIst tasks...")
            json.dump(reformatted_tasks, f)
            f.close()

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
            addTaskInNotion(client, t, reformatted_tasks)

    # check for deleted tasks
    for ct in cache_tasks:
        if ct not in reformatted_tasks:
            deleteTaskInNotion(t)

    res = getProperties(
        getResults(
            client.databases.query(
                **{
                    "database_id": os.getenv("NOTION_DB_ID"),
                    "filter": {"property": "Done", "checkbox": {"equals": True}},
                }
            )
        )
    )

    pprint(res)


def updateTaskInNotion(client, t, reformatted_tasks):
    print("Updating doIst task into Notion...")


def addTaskInNotion(client: Client, t, reformatted_tasks):
    print("Adding doIst task into Notion...")

    res = getProperties(
        getResults(
            client.databases.query(
                **{
                    "database_id": os.getenv("NOTION_DB_ID"),
                    "filter": {"property": "Done", "checkbox": {"equals": True}},
                }
            )
        )
    )


def deleteTaskInNotion(client: Client, p):
    print("delete")
