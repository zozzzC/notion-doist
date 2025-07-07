from src.notion.auth import notionAuth

def markNotionPageAsIncomplete(notionId: str):
    client = notionAuth()
    client.pages.update(page_id=notionId, properties={"Done": {"checkbox": False}})
