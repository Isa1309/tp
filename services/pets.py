from fastapi import HTTPException
from db.pets import get_pets, find_pet, add_pet as add_pet_db, change_pet, delete_pet as delete_pet_db
from db.users import find_user
from db.animals import find_animal
from db.breeds import find_breed
from uuid import uuid4
from schemas.pets import Pet, CreatePet, UpdatePet
from schemas.users import TokenAuth
from schemas.animals import Animal, Breed

class PetsService:
  def get_pet(self, pet_id: str, token: TokenAuth) -> Pet:
    user = find_user(token.token)
    if user == None: raise HTTPException(status_code=404, detail="Пользователь не найден")

    pet: Pet = find_pet(pet_id)
    if pet == None: raise HTTPException(status_code=404, detail="Питомец не найден")

    if user.id != pet.owner_id: raise HTTPException(status_code=403, detail="Отказано в доступе")
    return pet

  def get_pets(self, token: TokenAuth) -> list[Pet]:
    user = find_user(token.token)
    if user == None: raise HTTPException(status_code=404, detail="Пользователь не найден")

    return get_pets(user.id)

  def add_pet(self, data: CreatePet) -> Pet:
    user = find_user(data.owner.token)
    if user == None: raise HTTPException(status_code=404, detail="Пользователь не найден")

    new_pet: Pet = Pet(
      id=str(uuid4()),
      owner_id=user.id,
      name=data.name,
      age=data.age,
      gender=data.gender,
      birthday=0,
      animal_id="",
      breed_id="",
      weight=0,
      height=0,
      about="",
    )

    return add_pet_db(new_pet)

  def update_pet(self, data: UpdatePet) -> Pet:
    user = find_user(data.owner.token)
    if user == None: raise HTTPException(status_code=404, detail="Пользователь не найден")

    pet: Pet = find_pet(data.id)
    if pet == None: raise HTTPException(status_code=404, detail="Питомец не найден")

    if user.id != pet.owner_id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    animal: Animal = find_animal(data.animal_id)
    if animal == None: raise HTTPException(status_code=404, detail="Животное с переданным id не найдено")

    breed: Breed = find_breed(data.breed_id)
    if breed == None: raise HTTPException(status_code=404, detail="Породы с переданным id не найдено")

    if animal.id != breed.animal_id: raise HTTPException(status_code=400, detail="Неверно передано id животного и id породы")
    
    pet.name = data.name
    pet.age = data.age
    pet.gender = data.gender
    pet.birthday = data.birthday
    pet.animal_id = data.animal_id
    pet.breed_id = data.breed_id
    pet.weight = data.weight
    pet.height = data.height
    pet.about = data.about

    return change_pet(pet)

  def delete_pet(self, pet_id: str, token: TokenAuth) -> str:
    user = find_user(token.token)
    if user == None: raise HTTPException(status_code=404, detail="Пользователь не найден")

    pet: Pet = find_pet(pet_id)
    if pet == None: raise HTTPException(status_code=404, detail="Питомец не найден")

    if user.id != pet.owner_id: raise HTTPException(status_code=403, detail="Отказано в доступе")

    return delete_pet_db(pet.id)
  
pets_service: PetsService = PetsService()
