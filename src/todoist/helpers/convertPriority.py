from syncTasks import tasksType


def convertPriority(reformatted_doist_task: dict[tasksType]) -> str | None:
    priority_number = reformatted_doist_task.get("priority")

    if priority_number == 4:
        return "High"
    elif priority_number == 3:
        return "Medium"
    elif priority_number == 2:
        return "Low"

    return None
