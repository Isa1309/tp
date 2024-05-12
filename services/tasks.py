from fastapi import HTTPException
from db.pets import find_pet
from db.tasks import get_tasks, find_task, add_task, update_task, delete_task
from uuid import uuid4
from schemas.tasks import Task, AddTask, UpdateTask
from schemas.users import TokenAuth
from services.users import users_service
from utils.main import check_time

class TasksService:
  def get_tasks(self, token: TokenAuth) -> list[Task]:
    user = users_service._token_auth(token)

    return get_tasks(user.id)

  def get_task(self, id: str, token: TokenAuth) -> Task:
    task = find_task(id)
    if task == None: raise HTTPException(status_code=404, detail="Расписание не найдено")

    user = users_service._token_auth(token)
    if user.id != task.owner_id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    return task

  def add_task(self, data: AddTask) -> Task:
    pet = find_pet(data.pet_id)
    if pet == None: raise HTTPException(status_code=404, detail="Питомец не найден")

    user = users_service._token_auth(data.owner)
    if user.id != pet.owner_id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    new_task = Task(
      id=str(uuid4()),
      pet_id=pet.id,
      owner_id=user.id,
      title=data.title,
      description=data.description,
      date=data.date
    )

    add_task(new_task)

    return new_task

  def update_task(self, data: UpdateTask) -> Task:
    task = find_task(data.id)
    if task == None: raise HTTPException(status_code=404, detail="Расписание не найдено")

    user = users_service._token_auth(data.owner)
    if task.owner_id != user.id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    task.pet_id = data.pet_id
    task.title = data.title
    task.description = data.description
    task.date = data.date

    update_task(task)

    return task

  def delete_task(self, task_id: str, token: TokenAuth) -> str:
    task = find_task(task_id)
    if task == None: raise HTTPException(status_code=404, detail="Расписание не найдено")

    user = users_service._token_auth(token)
    if user.id != task.owner_id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    delete_task(task.id)

    return task.id
  
tasks_service: TasksService = TasksService()
