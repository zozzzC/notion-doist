from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task
from notion_client import Client
import os
import json
from src.todoist.helpers.ReformatTasks import ReformatTasks
from src.todoist.helpers.checkForRelation import checkForRelation
from src.todoist.helpers.convertPriority import convertPriority
from src.todoist.helpers.createNotionPage import createNotionPage
from src.todoist.helpers.lookupProject import lookupProject
from src.todoist.helpers.lookupSection import lookupSection
from src.todoist.helpers.calculateEndDate import calculateEndDate
from .helpers.getProperties import getProperties, getResults
from pprint import pprint
from dotenv import load_dotenv
from todoist.helpers.formatToDoIstDate import formatToDoIstDate
from todoist.helpers.formatToDoIstDateTime import formatToDoIstDateTime

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


def syncTasks(client: Client, api: TodoistAPI, data: any):
    tasks: list[Task] = api.get_tasks()
    reformatted_tasks = ReformatTasks()
    reformatted_tasks.reformatTasks(tasks)
    global reformatted_relation_tasks
    reformatted_relation_tasks = ReformatTasks()

    with open(os.getcwd() + "/test/doIstTask.json", "r") as f:
        cache_tasks: dict[str : dict[tasksType]] = json.load(f)

    if len(data) == 0:
        with open(os.getcwd() + "/test/doIstTask.json", "w") as f:
            print("Saving doIst tasks...")
            json.dump(reformatted_tasks.reformatted_tasks, f)
            f.close()

    # check for added and updated projects
    for t in reformatted_tasks.reformatted_tasks:
        if t in cache_tasks:
            for label in cache_tasks[t]:
                # o is the name of the title EG: name, url, is_favourite
                # cache_projects[p].get(o) is the name of the value EG: coding, http..., true
                # print(o)
                # print(cache_projects[p].get(o))

                if cache_tasks[t].get(label) != reformatted_tasks.reformatted_tasks[
                    t
                ].get(label):
                    updateTaskInNotion(client, t, reformatted_tasks.reformatted_tasks)
                    break
        else:
            addTaskInNotion(client, t, reformatted_tasks.reformatted_tasks)

    # check for deleted tasks
    for ct in cache_tasks:
        if ct not in reformatted_tasks.reformatted_tasks:
            deleteTaskInNotion(t)

    checkForRelation(reformatted_relation_tasks.reformatted_tasks)


def updateTaskInNotion(client, t, reformatted_tasks):
    print("Updating doIst task into Notion...")


def addTaskInNotion(
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
        "section_id" : str | None,
        "due" : str | None,
        "recurring":bool,
        "parent_id" : str | None,
    ],
    reformatted_tasks: dict[str : dict[tasksType]],
):
    print("Adding doIst task into Notion...")

    print(reformatted_tasks[t])

    task_properties = reformatted_tasks[t]
    # task properties contains content, labels, description, project_id, etc

    start_date = None
    end_date = None

    if task_properties.get("due"):
        start_date = task_properties.get("due")

    if task_properties.get("datetime"):
        start_date = formatToDoIstDateTime(task_properties.get("datetime"))

    if task_properties.get("duration"):
        end_date = calculateEndDate(
            start_date,
            task_properties.get("duration"),
            task_properties.get("duration_unit"),
        )

    priority = convertPriority(task_properties.get("priority"))
    project = None
    section = None

    if task_properties.get("project_id") != None:
        project = lookupProject(task_properties.get("project_id"))

    if task_properties.get("section_id") != None:
        section = lookupSection(
            task_properties.get("section_id"),
        )

    if task_properties.get("parent_id") != None:
        reformatted_relation_tasks.addIndividualTask(t)

    createNotionPage(
        t,
        task_properties.get("content"),
        start_date,
        end_date,
        None,
        priority,
        project,
        section,
        task_properties.get("labels"),
    )

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
