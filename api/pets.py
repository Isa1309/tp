from fastapi import APIRouter

from schemas.pets import Pet, CreatePet, UpdatePet
from schemas.users import TokenAuth
from services.pets import pets_service

router = APIRouter()

@router.post(
  "/api/pets",
  status_code=200,
  response_model=list[Pet]
)
def get_pets(data: TokenAuth):
  return pets_service.get_pets(data)

@router.post(
  "/api/pets/add",
  status_code=200,
  response_model=Pet
)
def add_pet(data: CreatePet):
  return pets_service.add_pet(data)

@router.put(
  "/api/pets/update",
  status_code=200,
  response_model=Pet
)
def update_pet(data: UpdatePet):
  return pets_service.update_pet(data)

@router.post(
  "/api/pets/{pet_id}",
  status_code=200,
  response_model=Pet
)
def get_pet(pet_id: str, data: TokenAuth):
  return pets_service.get_pet(pet_id, data)

@router.delete(
  "/api/pets/delete/{pet_id}",
  status_code=200,
  response_model=str
)
def delete_pet(pet_id: str, data: TokenAuth):
  return pets_service.delete_pet(pet_id, data)

