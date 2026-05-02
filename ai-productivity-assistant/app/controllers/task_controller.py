class TaskController:

    def __init__(self, task_service):
        self.task_service = task_service

    def create_task(self, user_id, title):
        return self.task_service.create_task(user_id, title)

    def get_tasks(self, user_id):
        return self.task_service.get_tasks(user_id)