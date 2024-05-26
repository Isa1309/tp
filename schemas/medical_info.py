from pydantic import BaseModel

from schemas.users import TokenAuth


class Vaccination(BaseModel):
    id: str
    card_id: str
    title: str
    date: int
    periodicity: int


class MedicalInfo(BaseModel):
    id: str
    card_id: str
    date: int
    clinic: str
    doctor: str
    symptoms: str
    diagnosis: str
    recipe: str


class MedicalCard(BaseModel):
    id: str
    owner_id: str
    pet_id: str
    vaccinations: list[Vaccination]
    medical_info: list[MedicalInfo]


class CreateVaccination(BaseModel):
    title: str
    date: int
    periodicity: int


class CreateMedicalInfo(BaseModel):
    date: int
    clinic: str
    doctor: str
    symptoms: str
    diagnosis: str
    recipe: str


class EditMedicalCard(BaseModel):
    owner: TokenAuth
    pet_id: str
    vaccinations: list[CreateVaccination]
    medical_info: list[CreateMedicalInfo]
    card_id: str
    date: int
    clinic: str
    doctor: str
    symptoms: str
    diagnosis: str
    recipe: str

class CreateMedicalCard(BaseModel):
    owner: TokenAuth
    pet_id: str
    vaccinations: list[CreateVaccination]
    medical_info: list[CreateMedicalInfo]
