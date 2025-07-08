from src.notion.types.NotionTypes import NotionPropsType
from src.notion.types.PagesTypes import PagesType
from pprint import pprint
from src.notion.helpers.getParentId import getParentId
from src.todoist.auth import doIstAuth
from src.notion.auth import notionAuth
from datetime import datetime
from src.notion.helpers.getTime import getTime
from src.notion.helpers.convertPriority import convertPriority
from src.notion.helpers.section.createSectionId import createSectionId
from src.notion.helpers.section.getSectionId import getSectionId
from src.notion.helpers.project.createProjectId import createProjectId
from src.notion.helpers.project.getProjectId import getProjectId
from todoist_api_python.models import Task
from src.todoist.helpers.ReformatTasks import TasksType


def updateDoIstTask(
    pageId: str,
    page: PagesType,
    doist_parent_id: str | None,
    add_to_doist_cache: TasksType,
):
    api = doIstAuth()
    client = notionAuth()
    content = page["Name"]

    date = page["Date"]
    start_date = None
    start_time = None
    end_date = None

    due_date = None
    due_datetime = None
    duration = None
    duration_unit = None

    if date != None:
        # then there must be a start date (at least.)
        start_date = date["start"]
        # check if start_date has a time.
        start_time = getTime(start_date)

        if start_time != None:
            due_date = datetime.fromisoformat(start_date).date().strftime("%Y%m%d")
        else:
            due_datetime = datetime.fromisoformat(start_date).isoformat()

        end_date = date["end"]

        if end_date != None:
            # then there is a duration -- this could be either a day duration (if start and end dates do not have a time field)
            # OR it could be a time duration
            if start_time != None:
                # in this case its a time duration
                duration = (
                    datetime.fromisoformat(end_date)
                    - datetime.fromisoformat(start_date)
                ).total_seconds() / 3600
                duration_unit = "minute"
            else:
                # in this case it is a day duration
                duration = (
                    datetime.fromisoformat(end_date).date()
                    - datetime.fromisoformat(start_date).date()
                ).days
                duration_unit = "day"
            # TODO fix duration, must be string, but right now its a timedelta obj

    deadline = page["Deadline"]

    deadline_date = None

    if deadline != None:
        deadline_date = datetime.fromisoformat(deadline["start"]).date().isoformat()

    labels = page["Label"]

    priority = convertPriority(page["Priority_Level"])

    # for projects, we first check if the project exists, if not, then create the project.

    project_id = getProjectId("Inbox")

    if page["Project"] != None:
        project_id = getProjectId(page["Project"])
        if project_id == None:
            project_id = createProjectId(page["Project"])

    # for sections, we need to do the same as the projects

    section_id = None

    if page["Section"] != None:
        section_id = getSectionId(page["Section"])

        if project_id == getProjectId("Inbox"):
            print(
                "Page "
                + pageId
                + " has section but no project ID, so section is not being synced."
            )
            section_id = None
        elif section_id == None and project_id != getProjectId("Inbox"):
            section_id = createSectionId(page["Section"], project_id)

    if doist_parent_id != None:
        print("Doist parent id is: " + doist_parent_id)

    task_id = page["ToDoistId"]

    due_date_str = None

    if due_date != None:
        due_date_str = datetime.fromisoformat(due_date)

    due_datetime_str = None

    if due_datetime != None:
        due_datetime_str = datetime.fromisoformat(due_datetime)

    deadline_date_str = None
    if deadline_date != None:
        deadline_date_str = datetime.fromisoformat(deadline_date)

    api.update_task(
        task_id=task_id,
        content=content,
        labels=labels,
        priority=priority,
        due_date=due_date_str,
        due_datetime=due_datetime_str,
        duration=duration,
        duration_unit=duration_unit,
        deadline_date=deadline_date_str,
    )

    api.move_task(
        task_id=task_id,
        project_id=project_id,
        section_id=section_id,
        parent_id=doist_parent_id,
    )

    add_to_doist_cache[task_id] = {
        "content": content,
        "project_id": project_id,
        "section_id": section_id,
        "parent_id": doist_parent_id,
        "labels": labels,
        "priority": priority,
        "due_date": due_date,
        "due_datetime": due_datetime,
        "duration": duration,
        "duration_unit": duration_unit,
        "deadline_date": deadline_date,
    }
