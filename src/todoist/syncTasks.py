from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task
from notion_client import Client
from queue import Queue
import os
import json
from src.todoist.helpers.ReformatTasks import ReformatTasks, tasksType, taskType
from src.todoist.helpers.deleteNotionPage import deleteNotionPage
from src.todoist.helpers.checkForRelation import checkForRelation
from src.todoist.helpers.convertPriority import convertPriority
from src.todoist.helpers.createNotionPage import createNotionPage
from src.todoist.helpers.lookupProject import lookupProject
from src.todoist.helpers.lookupSection import lookupSection
from src.todoist.helpers.calculateEndDate import calculateEndDate
from .helpers.getProperties import getProperties, getResults
from pprint import pprint
from dotenv import load_dotenv
from todoist.helpers.formatToDoIstDateTime import formatToDoIstDateTime
from src.notion.helpers.lookupPageByTodoistId import lookupPageByTodoistId
from todoist.helpers.updateNotionPage import updateNotionPage
from datetime import date, datetime, timedelta
from src.todoist.helpers.completeNotionPage import completeNotionPage
from src.todoist.helpers.changeTimezone import changeTimezone
from src.todoist.helpers.formatTaskForCreateUpdate import formatTaskForCreateUpdate


def syncTasks(client: Client, api: TodoistAPI, data: any):
    tasks = api.get_tasks()
    completed_t = api.get_completed_tasks_by_completion_date(
        since=(datetime.now() - timedelta(days=1)), until=(datetime.now())
    )
    completed_tasks = ReformatTasks()
    completed_tasks.reformatTasks(completed_t)
    new_tasks = ReformatTasks()
    new_tasks.reformatTasks(tasks)

    global reformatted_relation_tasks, require_relations
    reformatted_relation_tasks = ReformatTasks()
    # this queue takes in the tasks that require relations but do not have a parent id in notion to refer to yet
    require_relations = Queue()

    with open(os.getcwd() + "/test/doIstTask.json", "r") as f:
        cache_tasks: dict[str : dict[tasksType]] = json.load(f)

    if len(data) == 0:
        with open(os.getcwd() + "/test/doIstTask.json", "w") as f:
            print("Saving doIst tasks...")
            json.dump(new_tasks.reformatted, f)
            f.close()

    # check for added and updated projects
    for t in new_tasks.reformatted:
        # t is the key, so if t is in cache_tasks that means the task is already in the cache.
        if t in cache_tasks:
            for label in cache_tasks[t]:
                # o is the name of the title EG: name, url, is_favourite
                # cache_projects[p].get(o) is the name of the value EG: coding, http..., true
                # print(o)
                # print(cache_projects[p].get(o))

                if cache_tasks[t].get(label) != new_tasks.reformatted[t].get(label):
                    print(label)
                    print(cache_tasks[t].get(label))
                    print(new_tasks.reformatted[t].get(label))
                    updateTaskInNotion(t, new_tasks.reformatted)
                    break
        else:
            addTaskInNotion(t, new_tasks.reformatted)

    # this queue takes in the tasks that require relations but do not have a parent id in notion to refer to yet
    while not require_relations.empty():
        # determine if the task already exits in cache
        taskWithRelation: dict[
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
        ] = require_relations.get()

        if taskWithRelation in cache_tasks:
            updateTaskInNotion(taskWithRelation, new_tasks.reformatted)
        else:
            addTaskInNotion(taskWithRelation, new_tasks.reformatted)

    # check for deleted tasks
    for ct in cache_tasks:
        if ct in completed_tasks.reformatted:
            print("Task " + cache_tasks[ct].get("content") + " was completed.")
            completeTaskInNotion(ct)
        elif ct not in new_tasks.reformatted:
            print("Task " + cache_tasks[ct].get("content") + " was deleted.")
            deleteTaskInNotion(ct)
    checkForRelation(reformatted_relation_tasks.reformatted)

    with open(os.getcwd() + "/test/doIstTask.json", "w") as f:
        print("Saving doIst tasks...")
        json.dump(new_tasks.reformatted, f)
        f.close()


def updateTaskInNotion(
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
    print("Updating doIst task into Notion...")

    formatTaskForCreateUpdate(t, reformatted_tasks, require_relations, False)


def addTaskInNotion(
    t: dict[taskType],
    reformatted_tasks: dict[str : dict[tasksType]],
):
    print("Adding doIst task into Notion...")

    formatTaskForCreateUpdate(t, reformatted_tasks, require_relations, True)


def deleteTaskInNotion(t: dict[taskType]):
    deleteNotionPage(lookupPageByTodoistId(t))


def completeTaskInNotion(t: dict[taskType]):
    completeNotionPage(lookupPageByTodoistId(t))
