from pydantic import BaseModel
from schemas.users import TokenAuth

class Schedule(BaseModel):
  id: str
  pet_id: str
  owner_id: str
  time: list[str]

class AddSchedule(BaseModel):
  pet_id: str
  time: list[str]
  owner: TokenAuth

class UpdateSchedule(BaseModel):
  id: str
  pet_id: str
  time: list[str]
  owner: TokenAuth
