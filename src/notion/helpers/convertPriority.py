def convertPriority(priority_name: str) -> int | None:
    if priority_name == "High":
        return 4
    elif priority_name == "Medium":
        return 3
    elif priority_name == "Low":
        return 2

    return None
