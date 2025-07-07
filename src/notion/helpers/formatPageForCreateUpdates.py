# from src.notion.types.NotionTypes import notionPropsType, pagesType
# from datetime import datetime
# from src.notion.helpers.getTime import getTime
# from src.notion.helpers.convertPriority import convertPriority
# from src.notion.helpers.section.createSectionId import createSectionId
# from src.notion.helpers.section.getSectionId import getSectionId
# from src.notion.helpers.project.createProjectId import createProjectId
# from src.notion.helpers.project.getProjectId import getProjectId
# from todoist_api_python.models import Task


# def formatPageForCreateUpdate(page: dict[pagesType]) -> :
#     date = page["Date"]
#     start_date = None
#     start_time = None
#     end_date = None

#     due_date = None
#     due_datetime = None
#     duration = None
#     duration_unit = None

#     if date != None:
#         # then there must be a start date (at least.)
#         start_date = date["start"]
#         # check if start_date has a time.
#         start_time = getTime(start_date)

#         if start_time != None:
#             due_date = datetime.fromisoformat(start_date).date()
#         else:
#             due_datetime = datetime.fromisoformat(start_date)

#         end_date = date["end"]

#         if end_date != None:
#             # then there is a duration -- this could be either a day duration (if start and end dates do not have a time field)
#             # OR it could be a time duration
#             if start_time != None:
#                 # in this case its a time duration
#                 duration = datetime.fromisoformat(end_date) - start_date
#                 duration_unit = "day"
#             else:
#                 # in this case it is a day duration
#                 duration = (
#                     datetime.fromisoformat(end_date).date() - start_date
#                 ).total_seconds() * 60
#                 duration_unit = "minute"

#     deadline = page["Deadline"]

#     deadline_date = None

#     if deadline != None:
#         deadline_date = datetime.fromisoformat(deadline["start"]).date().isoformat()

#     labels = page["Label"]

#     content = page["Name"]

#     # TODO: parentIds are a special case -- if there is no corresponding ticktick id for it, then we cannot get the parent id. if there is, then we CAN get the parent id.
#     # to do this, first we can try to use  

#     priority = convertPriority(page["Priority_Level"])

#     # for projects, we first check if the project exists, if not, then create the project.
#     project_id = getProjectId(page["Project"])

#     if project_id == None:
#         project_id = createProjectId(page["Project"])

#     # for sections, we need to do the same as the projects

#     section_id = getSectionId(page["Section"])

#     if section_id == None:
#         section_id = createSectionId(page["Section"])

#     # TODO: parentIDs are not yet supported
#     return {
#         "content": content,
#         "deadline": deadline_date,
#         "duration": duration,
#         "duration_unit": duration_unit,
#         "due_date": due_date,
#         "due_datetime": due_datetime,
#         "labels": labels,
#         "section_id": section_id,
#         "project_id": project_id,
#         "priority": priority,
#     }
