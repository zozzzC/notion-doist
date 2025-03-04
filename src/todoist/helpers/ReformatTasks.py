from src.todoist.syncTasks import tasksType, Task


class ReformatTasks:

    def __init__(self):
        self.reformatted_tasks: dict[str : dict[tasksType]] = {}
        return self.reformatted_tasks

    def addIndividualTask(self, t: Task):
        self.reformatted_tasks.update(
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

            self.reformatted_tasks.get(t.id).update(reformatted_due)

        if t.duration:
            print(t.duration.amount)
            duration = str(t.duration.amount)
            duration_unit = str(t.duration.unit)
            reformatted_duration = {
                "duration": duration,
                "duration_unit": duration_unit,
            }
            self.reformatted_tasks.get(t.id).update(reformatted_duration)

        if t.parent_id:
            self.reformatted_tasks.get(t.id).update({"parent_id": t.parent_id})

    def reformatTasks(self, tasks: list[Task]) -> dict[str : dict[tasksType]]:
        for t in tasks:
            self.addIndividualTask(t)

        return self.reformatted_tasks
