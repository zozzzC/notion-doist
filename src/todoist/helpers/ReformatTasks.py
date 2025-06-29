from todoist_api_python.models import Task
import pprint

type tasksType = dict[
    str,
    dict[
        "content":str,
        "duration" : str | None,
        "duration_unit" : str | None,
        "datetime" : str | None,
        "description":str,
        "parent_id" : str | None,
        "is_completed":bool,
        "labels" : list[str | None],
        "timezone" : str | None,
        "priority":int,
        "project_id" : str | None,
        "due" : str | None,
        "recurring":bool,
    ],
]

type taskType = dict[
    "content":str,
    "duration" : str | None,
    "duration_unit" : str | None,
    "datetime" : str | None,
    "description":str,
    "parent_id" : str | None,
    "is_completed":bool,
    "labels" : list[str | None],
    "timezone" : str | None,
    "priority":int,
    "project_id" : str | None,
    "section_id" : str | None,
    "due" : str | None,
    "recurring":bool,
    "parent_id" : str | None,
]


class ReformatTasks:

    def __init__(self):
        self.reformatted: dict[str : dict[tasksType]] = {}

    def getReformattedTasks(self):
        return self.reformatted

    def addIndividualTask(self, t: Task):
        pprint.pprint(t)

        self.reformatted.update(
            {
                t.id: {
                    "is_completed": t.is_completed,
                    "content": t.content,
                    "description": t.description,
                    "parent_id": t.parent_id,
                    "project_id": t.project_id,
                    "labels": t.labels,
                    "priority": t.priority,
                    "section_id": t.section_id,
                }
            }
        )

        if t.due:
            reformatted_due = {
                "due": t.due.date,
                "recurring": t.due.is_recurring,
                "datetime": t.due.datetime,
                "timezone": t.due.timezone,
            }

            self.reformatted.get(t.id).update(reformatted_due)

        if t.duration:
            print(t.duration.amount)
            duration = str(t.duration.amount)
            duration_unit = str(t.duration.unit)
            reformatted_duration = {
                "duration": duration,
                "duration_unit": duration_unit,
            }
            self.reformatted.get(t.id).update(reformatted_duration)

        if t.parent_id:
            self.reformatted.get(t.id).update({"parent_id": t.parent_id})

    def reformatTasks(self, tasks: list[Task]) -> dict[str : dict[tasksType]]:
        for t in tasks:
            self.addIndividualTask(t)

        return self.reformatted

    def idExists(self, id: str) -> bool:
        if self.reformatted.get(id):
            return True

        return False
