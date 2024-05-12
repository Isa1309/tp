from pydantic import BaseModel
from schemas.users import TokenAuth

class Task(BaseModel):
  id: str
  owner_id: str
  pet_id: str
  title: str
  description: str
  date: int

class AddTask(BaseModel):
  pet_id: str
  title: str
  description: str
  date: int
  owner: TokenAuth

class UpdateTask(BaseModel):
  id: str
  pet_id: str
  title: str
  description: str
  date: int
  owner: TokenAuth

