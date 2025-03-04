from src.notion.helpers import lookupPage


def syncRelations(pageToDoIstId: str, parentToDoIstId: str):
    # after all the tasks are synced from todoist to notion, we must look at the tasks which have relations which were unable
    # to make a relation due to the page not existing yet, and add the relation
    page = lookupPage(pageToDoIstId, "Name")
    parentNotionId = lookupPage(parentToDoIstId, "TodoistId")

    page.update({"Parent": {"relation": [{"id": parentNotionId}]}})
