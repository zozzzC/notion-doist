from src.todoist.auth import doIstAuth


def createSectionId(section_name: str, project_id: str):
    api = doIstAuth()
    section = api.add_section(name=section_name, project_id=project_id, order=0)
    return section.id
