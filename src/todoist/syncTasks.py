from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task
from notion_client import Client
from queue import Queue
import os
import json
from src.todoist.helpers.markNotionPageAsIncomplete import markNotionPageAsIncomplete
from src.todoist.helpers.checkInNotion import checkInNotion
from src.todoist.helpers.ReformatTasks import ReformatTasks, TasksType, TaskPropsType
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


def syncTasks(api: TodoistAPI, data: any):
    tasks = api.get_tasks()
    completed_t = api.get_completed_tasks_by_completion_date(
        since=(datetime.now() - timedelta(days=1)), until=(datetime.now())
    )
    completed_tasks = ReformatTasks()
    completed_tasks.reformatTasks(completed_t)
    new_tasks = ReformatTasks()
    new_tasks.reformatTasks(tasks)

    reformatted_relation_tasks = ReformatTasks()
    # this queue takes in the tasks that require relations but do not have a parent id in notion to refer to yet
    require_relations: Queue[TaskPropsType] = Queue()

    with open(os.getcwd() + "/test/doIstTask.json", "r") as f:
        cache_tasks: TasksType = json.load(f)

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
                    # NOTE: we do NOT update if the cache's date is exactly one day behind -- this is expected.
                    updateTaskInNotion(t, require_relations, new_tasks.reformatted)
                    break
        else:
            # check if the task was previously in notion already. there may be a case where we untick a previously completed task.
            notion_id = checkInNotion(t)

            if notion_id != None:
                print(
                    "Previously marked as complete task "
                    + new_tasks.reformatted[t]["content"]
                    + " was marked as incomplete again."
                )
                markNotionPageAsIncomplete(notion_id)
            else:
                addTaskInNotion(t, require_relations, new_tasks.reformatted)

    # this queue takes in the tasks that require relations but do not have a parent id in notion to refer to yet
    while not require_relations.empty():
        # determine if the task already exits in cache
        taskWithRelation: TaskPropsType = require_relations.get()

        if taskWithRelation in cache_tasks:
            updateTaskInNotion(
                taskWithRelation, require_relations, new_tasks.reformatted
            )
        else:
            addTaskInNotion(taskWithRelation, require_relations, new_tasks.reformatted)

    # check for deleted tasks
    for ct in cache_tasks:
        if ct in completed_tasks.reformatted:
            print("Task " + cache_tasks[ct].get("content") + " was completed.")
            completeTaskInNotion(ct)
            # remove this from notion cache
        elif ct not in new_tasks.reformatted:
            print("Task " + cache_tasks[ct].get("content") + " was deleted.")
            deleteTaskInNotion(ct)
            # remove this from notion cache
    checkForRelation(reformatted_relation_tasks.reformatted)

    with open(os.getcwd() + "/test/doIstTask.json", "w") as f:
        print("Saving doIst tasks...")
        json.dump(new_tasks.reformatted, f)
        f.close()


def updateTaskInNotion(
    t: TaskPropsType,
    require_relations: Queue[TaskPropsType],
    reformatted_tasks: TasksType,
):
    print("Updating doIst task into Notion...")
    formatTaskForCreateUpdate(t, reformatted_tasks, require_relations, False)


def addTaskInNotion(
    t: TaskPropsType,
    require_relations: Queue[TaskPropsType],
    reformatted_tasks: TasksType,
):
    print("Adding doIst task into Notion...")
    formatTaskForCreateUpdate(t, reformatted_tasks, require_relations, True)


def deleteTaskInNotion(t: TaskPropsType):
    deleteNotionPage(lookupPageByTodoistId(t))


def completeTaskInNotion(t: TaskPropsType):
    completeNotionPage(lookupPageByTodoistId(t))
