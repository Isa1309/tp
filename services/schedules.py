from fastapi import HTTPException
from db.pets import find_pet
from db.schedules import get_schedules, find_schedule, add_schedule, update_schedule, delete_schedule, find_schedule_by_pet_id
from uuid import uuid4
from schemas.schedules import Schedule, AddSchedule, UpdateSchedule
from schemas.users import TokenAuth
from services.users import users_service
from utils.main import check_time

class SchedulesService:
  def get_schedules(self, token: TokenAuth) -> list[Schedule]:
    user = users_service._token_auth(token)

    return get_schedules(user.id)

  def get_schedule(self, pet_id: str, token: TokenAuth) -> Schedule:
    pet = find_pet(pet_id)
    if pet == None: raise HTTPException(status_code=404, detail="Питомец не найден")

    user = users_service._token_auth(token)
    if user.id != pet.owner_id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    schedule = find_schedule_by_pet_id(pet.id)
    if schedule == None: raise HTTPException(status_code=404, detail="Расписание не найдено")
    return schedule

  def add_schedule(self, data: AddSchedule) -> Schedule:
    user = users_service._token_auth(data.owner)
    if pet == None: raise HTTPException(status_code=404, detail="Питомец не найден")

    pet = find_pet(data.pet_id)
    if user.id != pet.owner_id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    schedule = find_schedule_by_pet_id(pet.id)
    if schedule != None: raise HTTPException(status_code=400, detail="Расписание для этого питомца уже создано")

    for i in range(len(data.time)):
      if not check_time(data.time[i]):
        raise HTTPException(status_code=400, detail="Неверный формат времени")

    new_schedule = Schedule(
      id=str(uuid4()),
      pet_id=pet.id,
      owner_id=user.id,
      time=data.time,
    )

    add_schedule(new_schedule)

    return new_schedule

  def update_schedule(self, data: UpdateSchedule) -> Schedule:
    schedule = find_schedule(data.id)
    if schedule == None: raise HTTPException(status_code=404, detail="Расписание не найдено")

    user = users_service._token_auth(data.owner)
    if schedule.owner_id != user.id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    for i in range(len(data.time)):
      if not check_time(data.time[i]):
        raise HTTPException(status_code=400, detail="Неверный формат времени")

    schedule.pet_id = data.pet_id
    schedule.time = data.time

    update_schedule(schedule)

    return schedule

  def delete_schedule(self, schedule_id: str, token: TokenAuth) -> str:
    schedule = find_schedule(schedule_id)
    if schedule == None: raise HTTPException(status_code=404, detail="Расписание не найдено")

    user = users_service._token_auth(token)
    if user.id != schedule.owner_id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    delete_schedule(schedule.id)

    return schedule.id
  
schedules_service: SchedulesService = SchedulesService()
