from typing import Dict
from src.notion.types.PagesTypes import PagesType


def getCompletedPages(pages: Dict[str, PagesType]) -> Dict[str, PagesType]:
    completed_pages = pages.copy()
    for page in pages:
        if pages[page]["Status"] == False:
            del completed_pages[page]

    return completed_pages
