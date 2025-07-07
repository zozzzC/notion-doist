from typing import Dict
from src.notion.types.PagesTypes import PagesType


def removeCompletedPages(
    pages: Dict[str, PagesType], completed_pages: Dict[str, PagesType]
) -> Dict[str, PagesType]:
    for completed_page in completed_pages:
        del pages[completed_page]

    return pages
