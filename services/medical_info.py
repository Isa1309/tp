from fastapi import HTTPException
from uuid import uuid4
from db.medical_info import find_medical_card, add_medical_card, delete_medical_card, find_medical_card_by_pet_id
from db.pets import find_pet
from schemas.users import TokenAuth
from schemas.medical_info import MedicalCard, MedicalInfo, Vaccination, CreateMedicalCard, CreateMedicalInfo, CreateVaccination
from services.users import users_service

class MedicalInfoService:
  def get_medical_info(self, card_id: str, token: TokenAuth) -> MedicalCard:
    user = users_service._token_auth(token)
    card = find_medical_card(card_id)

    if card == None: raise HTTPException(status_code=404, detail="Медицинская карта не найдена")
    if user.id != card.owner_id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    return card
  
  def get_medical_info_by_pet_id(self, pet_id: str, token: TokenAuth) -> MedicalCard:
    user = users_service._token_auth(token)
    card = find_medical_card_by_pet_id(pet_id)

    if card == None: raise HTTPException(status_code=404, detail="Медицинская карта не найдена")
    if user.id != card.owner_id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    return card

  def add_medical_info(self, data: CreateMedicalCard) -> MedicalCard:
    user = users_service._token_auth(data.owner)

    pet = find_pet(data.pet_id)

    if pet == None: raise HTTPException(status_code=404, detail="Питомец не найден")
    if pet.owner_id != user.id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    card_id = str(uuid4())
    vaccination: list[Vaccination] = []
    medical_info: list[MedicalInfo] = []

    for i in range(len(data.vaccinations)):
      vaccination.append(Vaccination(
        id=str(uuid4()),
        card_id=card_id,
        title=data.vaccinations[i].title,
        date=data.vaccinations[i].date,
        periodicity=data.vaccinations[i].periodicity
      ))

    for i in range(len(data.medical_info)):
      medical_info.append(MedicalInfo(
        id=str(uuid4()),
        card_id=card_id,
        date=data.medical_info[i].date,
        clinic=data.medical_info[i].clinic,
        doctor=data.medical_info[i].doctor,
        symptoms=data.medical_info[i].symptoms,
        diagnosis=data.medical_info[i].diagnosis,
        recipe=data.medical_info[i].recipe
      ))

    new_medical_card = MedicalCard(
      id=card_id,
      owner_id=user.id,
      pet_id=pet.id,
      vaccinations=vaccination,
      medical_info=medical_info
    )

    add_medical_card(new_medical_card)

    return new_medical_card

  def delete_medical_info(self, card_id: str, token: TokenAuth) -> str:
    user = users_service._token_auth(token)
    card = find_medical_card(card_id)

    if card == None: raise HTTPException(status_code=404, detail="Медицинская карта не найдена")
    if user.id != card.owner_id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    return delete_medical_card(card.id)
  
medical_info_service: MedicalInfoService = MedicalInfoService()
