from app.controllers.task_controller import TaskController
from repository.task_repo import TaskRepository
from app.services.task_service import TaskService

repo = TaskRepository("data/mock_db.json")
service = TaskService(repo)
controller = TaskController(service)

def create_task(user_id, title):
    return controller.create_task(user_id, title)

def get_tasks(user_id):
    return controller.get_tasks(user_id)