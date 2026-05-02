def validate_task(title):
    if not title:
        raise ValueError("Task title cannot be empty")