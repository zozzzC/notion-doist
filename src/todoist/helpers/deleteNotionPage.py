from src.notion.auth import notionAuth


def deleteNotionPage(notion_id: str):
    client = notionAuth()
    if notion_id != None:
        client.pages.update(page_id=notion_id, archived=True)
