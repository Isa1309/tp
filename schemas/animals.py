from pydantic import BaseModel

class Animal(BaseModel):
  id: str
  name: str

class Breed(BaseModel):
  id: str
  name: str
  animal_id: str

class CreateAnimal(BaseModel):
  name: str

class CreateBreed(BaseModel):
  name: str
  animal_id: str