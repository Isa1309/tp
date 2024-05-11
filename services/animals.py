from schemas.animals import Animal, CreateAnimal
from db.animals import get_animals, add_animal
from uuid import uuid4

class AnimalsService:
  def get_animals(self) -> list[Animal]:
    animals: list[Animal] = get_animals()

    return animals

  def add_animal(self, data: CreateAnimal):
    new_animal: Animal = Animal(
      id=str(uuid4()),
      name=data.name,
    )

    add_animal(new_animal)
    return new_animal
  
animals_service: AnimalsService = AnimalsService()