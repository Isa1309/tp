from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.medical_info import MedicalCard, MedicalInfo, Vaccination

Base = declarative_base()

class TableMedicalCard(Base):
  __tablename__ = "cards"

  id = Column("id", String, primary_key=True)
  owner_id = Column("owner_id", String)
  pet_id = Column("pet_id", String)

  def __init__(self, id, owner_id, pet_id):
    self.id = id
    self.owner_id = owner_id
    self.pet_id = pet_id

class TableMedicalInfo(Base):
  __tablename__ = "info"

  id = Column("id", String, primary_key=True)
  card_id = Column("card_id", String)
  date = Column("date", Integer)
  clinic = Column("clinic", String)
  doctor = Column("doctor", String)
  symptoms = Column("symptoms", String)
  diagnosis = Column("diagnosis", String)
  recipe = Column("recipe", String)

  def __init__(self, id, card_id, date, clinic, doctor, symptoms, diagnosis, recipe):
    self.id = id
    self.card_id = card_id
    self.date = date
    self.clinic = clinic
    self.doctor = doctor
    self.symptoms = symptoms
    self.diagnosis = diagnosis
    self.recipe = recipe

class TableVaccination(Base):
  __tablename__ = "vaccinations"

  id = Column("id", String, primary_key=True)
  card_id = Column("card_id", String)
  title = Column("title", String)
  date = Column("date", Integer)
  periodicity = Column("periodicity", Integer)

  def __init__(self, id, card_id, title, date, periodicity):
    self.id = id
    self.card_id = card_id
    self.title = title
    self.date = date
    self.periodicity = periodicity

engine = create_engine("sqlite:///db/db/medical_info.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

def convert_to_medical_card(table_medical_card: TableMedicalCard, table_medical_info: list[TableMedicalInfo], table_vaccinations: list[TableVaccination]) -> MedicalCard:
  medical_info: list[MedicalInfo] = []
  vaccinations: list[Vaccination] = []

  for i in range(len(table_medical_info)):
    medical_info.append(MedicalInfo(
      id=table_medical_info[i].id,
      card_id=table_medical_info[i].card_id,
      date=table_medical_info[i].date,
      clinic=table_medical_info[i].clinic,
      doctor=table_medical_info[i].doctor,
      symptoms=table_medical_info[i].symptoms,
      diagnosis=table_medical_info[i].diagnosis,
      recipe=table_medical_info[i].recipe
    ))

  for i in range(len(table_vaccinations)):
    vaccinations.append(Vaccination(
      id=table_vaccinations[i].id,
      card_id=table_vaccinations[i].card_id,
      title=table_vaccinations[i].title,
      date=table_vaccinations[i].date,
      periodicity=table_vaccinations[i].periodicity
    ))

  return MedicalCard(
    id=table_medical_card.id,
    owner_id=table_medical_card.owner_id,
    pet_id=table_medical_card.pet_id,
    vaccinations=vaccinations,
    medical_info=medical_info
  )

def convert_to_table_medical_card_objects(medical_card: MedicalCard) -> tuple[TableMedicalCard, list[TableMedicalInfo], list[TableVaccination]]:
  table_medical_card: TableMedicalCard = TableMedicalCard(
    id=medical_card.id,
    pet_id=medical_card.pet_id,
    owner_id=medical_card.owner_id
  )

  table_medical_info: list[TableMedicalInfo] = []
  table_vaccinations: list[TableVaccination] = []

  for i in range(len(medical_card.medical_info)):
    table_medical_info.append(TableMedicalInfo(
      id=medical_card.medical_info[i].id,
      card_id=medical_card.medical_info[i].card_id,
      date=medical_card.medical_info[i].date,
      clinic=medical_card.medical_info[i].clinic,
      doctor=medical_card.medical_info[i].doctor,
      symptoms=medical_card.medical_info[i].symptoms,
      diagnosis=medical_card.medical_info[i].diagnosis,
      recipe=medical_card.medical_info[i].recipe
    ))

  for i in range(len(medical_card.vaccinations)):
    table_vaccinations.append(TableVaccination(
      id=medical_card.vaccinations[i].id,
      card_id=medical_card.vaccinations[i].card_id,
      title=medical_card.vaccinations[i].title,
      date=medical_card.vaccinations[i].date,
      periodicity=medical_card.vaccinations[i].periodicity
    ))

  return (table_medical_card, table_medical_info, table_vaccinations)

def find_medical_card_by_pet_id(pet_id: str) -> MedicalCard:
  table_medical_card = session.query(TableMedicalCard).filter(or_(TableMedicalCard.pet_id == pet_id)).first()
  if table_medical_card == None: return None

  table_medical_info = session.query(TableMedicalInfo).filter(or_(TableMedicalInfo.card_id == table_medical_card.id)).all()
  table_vaccinations = session.query(TableVaccination).filter(or_(TableVaccination.card_id == table_medical_card.id)).all()

  medical_card = convert_to_medical_card(table_medical_card, table_medical_info, table_vaccinations)
  
  return medical_card

def find_medical_card(card_id: str) -> MedicalCard:
  table_medical_card = session.query(TableMedicalCard).get(card_id)
  if table_medical_card == None: return None

  table_medical_info = session.query(TableMedicalInfo).filter(or_(TableMedicalInfo.card_id == card_id)).all()
  table_vaccinations = session.query(TableVaccination).filter(or_(TableVaccination.card_id == card_id)).all()

  medical_card = convert_to_medical_card(table_medical_card, table_medical_info, table_vaccinations)
  
  return medical_card

def add_medical_card(data: MedicalCard) -> MedicalCard:
  table_medical_card_data = convert_to_table_medical_card_objects(medical_card=data)

  session.add(table_medical_card_data[0])

  for i in range(len(table_medical_card_data[1])):
    session.add(table_medical_card_data[1][i])

  for i in range(len(table_medical_card_data[2])):
    session.add(table_medical_card_data[2][i])

  session.commit()

  return data

def delete_medical_card(card_id: str) -> str:
  table_medical_card = session.query(TableMedicalCard).get(card_id)
  if table_medical_card == None: return None

  table_medical_info = session.query(TableMedicalInfo).filter(or_(TableMedicalInfo.card_id == card_id)).all()
  table_vaccinations = session.query(TableVaccination).filter(or_(TableVaccination.card_id == card_id)).all()

  for i in range(len(table_medical_info)):
    session.delete(table_medical_info[i])

  for i in range(len(table_vaccinations)):
    session.delete(table_vaccinations[i])

  session.delete(table_medical_card)

  session.commit()
  return card_id
