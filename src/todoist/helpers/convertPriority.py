def convertPriority(priority_number: int) -> str | None:
    if priority_number == 4:
        return "High"
    elif priority_number == 3:
        return "Medium"
    elif priority_number == 2:
        return "Low"

    return None
