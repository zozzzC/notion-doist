from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task
from notion_client import Client
from queue import Queue
import os
import json
from src.todoist.helpers.ReformatTasks import ReformatTasks, tasksType, taskType
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
from src.notion.helpers.lookupPage import lookupPageByTodoistId
from todoist.helpers.updateNotionPage import updateNotionPage


def syncTasks(client: Client, api: TodoistAPI, data: any):
    tasks: list[Task] = api.get_tasks()
    new_tasks = ReformatTasks()
    new_tasks.reformatTasks(tasks)
    global reformatted_relation_tasks, require_relations
    reformatted_relation_tasks = ReformatTasks()
    # this queue takes in the tasks that require relations but do not have a parent id in notion to refer to yet
    require_relations = Queue()

    # TODO: remove this length, since you will need to save the new sync into the cache
    # And you already got the previous tasks in the method above

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
                    # print(label)
                    # print(cache_tasks[t].get(label))
                    # print(new_tasks.reformatted[t].get(label))
                    updateTaskInNotion(t, new_tasks.reformatted)
                    break
        else:
            addTaskInNotion(t, new_tasks.reformatted)

    # # this queue takes in the tasks that require relations but do not have a parent id in notion to refer to yet
    # while not require_relations.empty():
    #     #determine if the task already exits in cache
    #     taskWithRelation : dict[
    #     "content":str,
    #     "duration" : str | None,
    #     "duration_unit" : str | None,
    #     "datetime" : str | None,
    #     "description":str,
    #     "parent_id" : str | None,
    #     "is_completed":bool,
    #     "labels" : list[str | None],
    #     "timezone" : str | None,
    #     "priority":int,
    #     "project_id" : str | None,
    #     "section_id" : str | None,
    #     "due" : str | None,
    #     "recurring":bool,
    #     "parent_id" : str | None,
    # ] = require_relations.get();

    #     addTaskInNotion(require_relations.get(), new_tasks.reformatted)

    # # check for deleted tasks
    # for ct in cache_tasks:
    #     if ct not in new_tasks.reformatted:
    #         deleteTaskInNotion(t)

    # checkForRelation(reformatted_relation_tasks.reformatted)


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

    task_properties = reformatted_tasks[t]
    # task properties contains content, labels, description, project_id, etc

    print(task_properties.get("parent_id"))
    if task_properties.get("parent_id") != None:
        # TODO: test if working.
        notionParentPageId = lookupPageByTodoistId(task_properties.get("parent_id"))
        if notionParentPageId == None:
            # we can try to see if the parent id is in notion.
            # but if it is not in notion, then in that case we don't have the associated notion ID yet.
            # thus we have to put this into our required relations queue.
            print(
                "doIst task ID:"
                + t
                + " "
                + task_properties.get("content")
                + "pushed onto require relations queue."
            )
            require_relations.put(t)
            return

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

    notionParentPageId = None

    notionPageId = lookupPageByTodoistId(t)

    updateNotionPage(
        t,
        task_properties.get("content"),
        start_date,
        end_date,
        None,
        priority,
        project,
        section,
        task_properties.get("labels"),
        notionParentPageId,
        notionPageId,
    )

    # cache_task_properties : dict[tasksType] = cache_tasks[t]
    # task_properties : dict[tasksType] = reformatted_tasks[t]
    # # task properties contains content, labels, description, project_id, etc

    # #for each of the task properties, check which ones were changed
    # for property in task_properties:
    #     if task_properties[property] != cache_task_properties[property]:


def addTaskInNotion(
    t: dict[taskType],
    reformatted_tasks: dict[str : dict[tasksType]],
):
    print("Adding doIst task into Notion...")

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

    parent_id = None

    if task_properties.get("parent_id") != None:
        if lookupPageByTodoistId(task_properties.get("parent_id")) == None:
            require_relations.put(t)
            print("pushing into require_relations")
            return
        else:
            parent_id = lookupPageByTodoistId(task_properties.get("parent_id"))

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
        parent_id,
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
