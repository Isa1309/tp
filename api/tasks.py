from fastapi import APIRouter

from schemas.tasks import Task, AddTask, UpdateTask
from schemas.users import TokenAuth
from services.tasks import tasks_service

router = APIRouter()

@router.post(
  "/api/tasks",
  status_code=200,
  response_model=list[Task]
)
def get_tasks(data: TokenAuth):
  return tasks_service.get_tasks(data)

@router.post(
  "/api/tasks/add",
  status_code=200,
  response_model=Task
)
def add_task(data: AddTask):
  return tasks_service.add_task(data)

@router.put(
  "/api/tasks/update",
  status_code=200,
  response_model=Task
)
def update_task(data: UpdateTask):
  return tasks_service.update_task(data)

@router.post(
  "/api/tasks/{task_id}",
  status_code=200,
  response_model=Task
)
def get_task(pet_id: str, data: TokenAuth):
  return tasks_service.get_task(pet_id, data)

@router.delete(
  "/api/tasks/delete/{task_id}",
  status_code=200,
  response_model=str
)
def delete_task(task_id: str, data: TokenAuth):
  return tasks_service.delete_task(task_id, data)

