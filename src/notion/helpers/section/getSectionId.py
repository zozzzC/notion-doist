from src.todoist.auth import doIstAuth


def getSectionId(section_name: str) -> str | None:

    api = doIstAuth()

    sections_list = api.get_sections()

    for section in next(sections_list):
        if section.name == section_name:
            return section.id

    return None
