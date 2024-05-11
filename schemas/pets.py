from pydantic import BaseModel

from schemas.users import TokenAuth

class Pet(BaseModel):
  id: str
  owner_id: str
  name: str
  age: int
  gender: str
  birthday: int
  animal_id: str
  breed_id: str
  weight: int
  height: int
  about: str

class CreatePet(BaseModel):
  name: str
  age: int
  gender: str
  owner: TokenAuth

class UpdatePet(BaseModel):
  id: str
  name: str
  age: int
  gender: str
  birthday: int
  animal_id: str
  breed_id: str
  weight: int
  height: int
  about: str
  owner: TokenAuth
