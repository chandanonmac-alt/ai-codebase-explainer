class TaskService:

    def __init__(self, task_repo):
        self.task_repo = task_repo

    def create_task(self, user_id, title):
        task = {
            "user_id": user_id,
            "title": title,
            "status": "pending"
        }
        return self.task_repo.save(task)

    def get_tasks(self, user_id):
        return self.task_repo.find_by_user(user_id)