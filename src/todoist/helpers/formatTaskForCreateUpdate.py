from src.todoist.helpers.ReformatTasks import ReformatTasks, TasksType, TaskPropsType
import queue
from src.todoist.helpers.changeTimezone import changeTimezone
from src.todoist.helpers.convertPriority import convertPriority
from src.todoist.helpers.lookupProject import lookupProject
from src.todoist.helpers.lookupSection import lookupSection
from src.todoist.helpers.calculateEndDate import calculateEndDate
from src.notion.helpers.lookupPageByTodoistId import lookupPageByTodoistId
from src.todoist.helpers.updateNotionPage import updateNotionPage
from src.todoist.helpers.createNotionPage import createNotionPage


def formatTaskForCreateUpdate(
    t: TaskPropsType,
    reformatted_tasks: TasksType,
    require_relations: queue,
    create: bool,
):

    task_properties = reformatted_tasks[t]
    # task properties contains content, labels, description, project_id, etc

    start_date = None
    end_date = None
    time_zone = "Pacific/Auckland"

    if task_properties.get("due"):
        doIstDateTime = task_properties.get("due")
        start_date = changeTimezone(doIstDateTime)

    if task_properties.get("datetime"):
        doIstDateTime = task_properties.get("datetime")
        start_date = changeTimezone(doIstDateTime)

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

    if create:
        createNotionPage(
            t,
            task_properties.get("content"),
            start_date,
            end_date,
            time_zone,
            None,
            priority,
            project,
            section,
            task_properties.get("labels"),
            parent_id,
        )
    else:
        page_id = lookupPageByTodoistId(t)
        updateNotionPage(
            t,
            task_properties.get("content"),
            start_date,
            end_date,
            time_zone,
            None,
            priority,
            project,
            section,
            task_properties.get("labels"),
            parent_id,
            page_id,
        )
