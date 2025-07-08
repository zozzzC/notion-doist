from notion_client.typing import SyncAsync
from pprint import pprint
from typing import Any, cast
from src.notion.types.NotionTypes import NotionPropsType
from src.notion.types.PagesTypes import PagesType
from typing import Dict
from datetime import datetime, timedelta


class ReformatPages:

    def __init__(self):
        self.reformatted: Dict[str, PagesType] = {}

    def getReformattedPages(self):
        return self.reformatted

    def addIndividualPage(self, page_id: str, page: NotionPropsType):

        # ensure date does exist first before trying to access start and end date.

        date = None
        if page["Date"]["date"] != None:
            start_date = (
                datetime.fromisoformat(page["Date"]["date"]["start"])
                + timedelta(days=1)
            ).isoformat()

            end_date = None

            if page["Date"]["date"]["end"] != None:
                end_date = (
                    datetime.fromisoformat(page["Date"]["date"]["end"])
                    + timedelta(days=1)
                ).isoformat()
            date = {"end": end_date, "start": start_date}

        deadline = None

        if page["Deadline"]["date"] != None:
            deadline_start_date = (
                datetime.fromisoformat(page["Deadline"]["date"]["start"])
                + timedelta(days=1)
            ).isoformat()

            deadline_end_date = None

            if page["Deadline"]["date"]["end"] != None:
                deadline_end_date = (
                    datetime.fromisoformat(page["Deadline"]["date"]["end"])
                    + timedelta(days=1)
                ).isoformat()
            deadline = {
                "end": deadline_end_date,
                "start": deadline_start_date,
            }

        done = page["Done"]["checkbox"]
        notion_label = page["Label"]["multi_select"]
        label = notion_label

        # format the label depending on whether it is null or not.
        if len(page["Label"]["multi_select"]) != 0:
            label = []
            for l in page["Label"]["multi_select"]:
                label.append(l["name"])

        name = page["Name"]["title"][0]["plain_text"]

        if name == None:
            return

        notion_parent = page["Parent"]["relation"]
        parent_id = None

        # parent gives us the id.
        if len(notion_parent) != 0:
            parent_id = notion_parent[0]["id"]

        notion_priority_level = page["Priority Level"]["select"]
        priority_level = notion_priority_level

        if (notion_priority_level) != None:
            priority_level = notion_priority_level["name"]

        notion_project = page["Project"]["select"]
        project = notion_project

        if (notion_project) != None:
            project = notion_project["name"]

        notion_section = page["Section"]["select"]
        section = notion_section

        if (notion_section) != None:
            section = notion_section["name"]

        toDoIst_id = None
        if len(page["ToDoistId"]["rich_text"]) != 0:
            toDoIst_id = page["ToDoistId"]["rich_text"][0]["plain_text"]

        pprint(date)

        pprint(deadline)

        self.reformatted.update(
            {
                page_id: {
                    "Date": date,
                    "Deadline": deadline,
                    "Label": label,
                    "Name": name,
                    "ParentId": parent_id,
                    "Priority_Level": priority_level,
                    "Project": project,
                    "Section": section,
                    "ToDoistId": toDoIst_id,
                    "Status": done,
                }
            }
        )

    def reformatPages(self, pages: SyncAsync[Any]) -> Dict[str, PagesType]:
        for page in pages["results"]:
            typedPage = cast(NotionPropsType, page["properties"])
            self.addIndividualPage(page["id"], typedPage)

        return self.reformatted
