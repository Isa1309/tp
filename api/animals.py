from fastapi import APIRouter

from schemas.animals import Animal, CreateAnimal
from services.animals import animals_service

router = APIRouter()

@router.get(
  "/api/animals",
  status_code=200,
  response_model=list[Animal]
)
def get_animals():
  return animals_service.get_animals()

@router.post(
  "/api/animals/add",
  status_code=200,
  response_model=Animal
)
def add_animals(data: CreateAnimal):
  return animals_service.add_animal(data)
