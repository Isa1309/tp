from fastapi import APIRouter

from schemas.schedules import Schedule, AddSchedule, UpdateSchedule
from schemas.users import TokenAuth
from services.schedules import schedules_service

router = APIRouter()

@router.post(
  "/api/schedules",
  status_code=200,
  response_model=list[Schedule]
)
def get_schedules(data: TokenAuth):
  return schedules_service.get_schedules(data)

@router.post(
  "/api/schedules/add",
  status_code=200,
  response_model=Schedule
)
def add_schedule(data: AddSchedule):
  return schedules_service.add_schedule(data)

@router.put(
  "/api/schedules/update",
  status_code=200,
  response_model=Schedule
)
def update_schedule(data: UpdateSchedule):
  return schedules_service.update_schedule(data)

@router.post(
  "/api/schedules/{pet_id}",
  status_code=200,
  response_model=Schedule
)
def get_schedule(pet_id: str, data: TokenAuth):
  return schedules_service.get_schedule(pet_id, data)

@router.delete(
  "/api/schedules/delete/{schedule_id}",
  status_code=200,
  response_model=str
)
def delete_schedule(schedule_id: str, data: TokenAuth):
  return schedules_service.delete_schedule(schedule_id, data)

