from pydantic import BaseModel
from schemas.users import TokenAuth

class Animal(BaseModel):
  id: str
  name: str

class Breed(BaseModel):
  id: str
  name: str
  animal_id: str

class CreateAnimal(BaseModel):
  name: str
  admin: TokenAuth

class CreateBreed(BaseModel):
  name: str
  animal_id: str
  admin: TokenAuth