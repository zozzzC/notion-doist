from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task
from notion_client import Client
import os
import json

from src.todoist.helpers import convertPriority, createNotionPage
from src.todoist.helpers.calculateEndDate import calculateEndDate
from .helpers.getProperties import getProperties, getResults
from pprint import pprint
from dotenv import load_dotenv
from todoist.helpers import formatToDoIstDate

type tasksType = dict[
    str,
    dict[
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
        "due" : str | None,
        "recurring":bool,
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
                }
            }
        )

        reformatted_tasks.get(t.id).update(reformatted_due)

        if t.duration:
            print(t.duration.amount)
            duration = str(t.duration.amount)
            duration_unit = str(t.duration.unit)
            reformatted_duration = {
                "duration": duration,
                "duration_unit": duration_unit,
            }
            reformatted_tasks.get(t.id).update(reformatted_duration)

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


def updateTaskInNotion(client, t, reformatted_tasks):
    print("Updating doIst task into Notion...")


def addTaskInNotion(
    client: Client,
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
        "due" : str | None,
        "recurring":bool,
    ],
    reformatted_tasks: dict[str : dict[tasksType]],
):
    print("Adding doIst task into Notion...")

    print(reformatted_tasks[t])

    task_properties = reformatted_tasks[t]
    # task properties contains content, labels, description, project_id, etc

    start_date = None
    end_date = None

    if t.get("due"):
        start_date = task_properties.get("due")

    if t.get("datetime"):
        start_date = formatToDoIstDate(task_properties.get("datetime"))
        end_date = calculateEndDate(
            start_date,
            task_properties.get("duration"),
            task_properties.get("duration_unit"),
        )

    priority = convertPriority(t.get("priority"))
    
    createNotionPage(task_properties.get("content"), start_date, end_date, None, priority, lookupProject(task_properties.get("project_id"), lookupSection(task_properties.get("section_id"), task_properties.get("labels"))))

    # res = getProperties(
    #     getResults(
    #         client.databases.query(
    #             **{
    #                 "database_id": os.getenv("NOTION_DB_ID"),
    #                 "filter": {"property": "Done", "checkbox": {"equals": True}},
    #             }
    #         )
    #     )
    # )


def deleteTaskInNotion(client: Client, p):
    print("delete")
