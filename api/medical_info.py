from fastapi import APIRouter

from schemas.medical_info import MedicalCard, CreateMedicalCard
from services.medical_info import medical_info_service
from schemas.users import TokenAuth

router = APIRouter()

@router.post(
  "/api/medical_info/add",
  status_code=200,
  response_model=MedicalCard
)
def add_animals(data: CreateMedicalCard):
  return medical_info_service.add_medical_info(data)

@router.post(
  "/api/medical_info/{card_id}",
  status_code=200,
  response_model=MedicalCard
)
def get_animals(card_id: str, data: TokenAuth):
  return medical_info_service.get_medical_info(card_id, data)

@router.post(
  "/api/medical_info/pet_id/{pet_id}",
  status_code=200,
  response_model=MedicalCard
)
def get_animals_by_pet_id(pet_id: str, data: TokenAuth):
  return medical_info_service.get_medical_info_by_pet_id(pet_id, data)

@router.delete(
  "/api/medical_info/delete/{card_id}",
  status_code=200,
  response_model=str
)
def add_breed(card_id: str, data: TokenAuth):
  return medical_info_service.delete_medical_info(card_id, data)

