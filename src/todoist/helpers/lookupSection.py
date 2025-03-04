from src.todoist.auth import doIstAuth


def lookupSection(section_id: str):
    api = doIstAuth()

    return api.get_section(section_id).name
