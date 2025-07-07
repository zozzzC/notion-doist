from todoist_api_python.models import Task
import pprint
from typing import Iterator, TypedDict, List, Dict


class TaskPropsType(TypedDict):
    content: str
    duration: str | None
    duration_unit: str | None
    datetime: str | None
    description: str | None
    parent_id: str | None
    is_completed: bool
    labels: List[str | None]
    timezone: str | None
    priority: int
    project_id: str | None
    section_id: str | None
    due: str | None
    recurring: bool


TasksType = Dict[str, TaskPropsType]

class ReformatTasks:

    def __init__(self):
        self.reformatted: Dict[str, TaskPropsType] = {}

    def getReformattedTasks(self):
        return self.reformatted

    def addIndividualTask(self, t: Task):
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
                "due": t.due.date.isoformat(),
                "recurring": t.due.is_recurring,
                "datetime": t.due.date.isoformat(),
                "timezone": "Pacific/Auckland",
            }

            self.reformatted.get(t.id).update(reformatted_due)

        if t.duration:
            duration = str(t.duration.amount)
            duration_unit = str(t.duration.unit)
            reformatted_duration = {
                "duration": duration,
                "duration_unit": duration_unit,
            }
            self.reformatted.get(t.id).update(reformatted_duration)

        if t.parent_id:
            self.reformatted.get(t.id).update({"parent_id": t.parent_id})

    def reformatTasks(self, tasks: Iterator[list[Task]]) -> Dict[str, TaskPropsType]:
        for t in next(tasks):
            self.addIndividualTask(t)

        return self.reformatted

    def idExists(self, id: str) -> bool:
        if self.reformatted.get(id):
            return True

        return False
