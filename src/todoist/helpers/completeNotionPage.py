from src.notion.auth import notionAuth


def completeNotionPage(notion_id: str):
    client = notionAuth()
    if notion_id == None:
        print("Notion page ID:" + notion_id + " was already deleted.")

    properties = {"Done": {"checkbox": True}}

    client.pages.update(page_id=notion_id, properties=properties)
