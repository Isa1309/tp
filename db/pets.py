from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.pets import Pet

Base = declarative_base()

class TablePet(Base):
  __tablename__ = "pets"

  id = Column("id", String, primary_key=True)
  name = Column("name", String)
  owner_id = Column("owner_id", String)
  age = Column("age", Integer)
  gender = Column("gender", String)
  birthday = Column("birthday", Integer)
  animal_id = Column("animal_id", String)
  breed_id = Column("breed_id", String)
  weight = Column("weight", Integer)
  height = Column("height", Integer)
  about = Column("about", String)

  def __init__(self, id, owner_id, name, age, gender, birthday, animal_id, breed_id, weight, height, about):
    self.id = id
    self.owner_id = owner_id
    self.name = name
    self.age = age
    self.gender = gender
    self.birthday = birthday
    self.animal_id = animal_id
    self.breed_id = breed_id
    self.weight = weight
    self.height = height
    self.about = about

engine = create_engine("sqlite:///db/db/pets.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

def convert_to_pet(pet: TablePet) -> Pet:
  return Pet(
    id=pet.id,
    owner_id=pet.owner_id,
    name=pet.name,
    age=pet.age,
    gender=pet.gender,
    birthday=pet.birthday,
    animal_id=pet.animal_id,
    breed_id=pet.breed_id,
    weight=pet.weight,
    height=pet.height,
    about=pet.about,
  )

def convert_to_table_pet(pet: Pet) -> TablePet:
  return TablePet(
    id=pet.id,
    owner_id=pet.owner_id,
    name=pet.name,
    age=pet.age,
    gender=pet.gender,
    birthday=pet.birthday,
    animal_id=pet.animal_id,
    breed_id=pet.breed_id,
    weight=pet.weight,
    height=pet.height,
    about=pet.about,
  )

def get_pets(owner_id: str) -> list[Pet]:
  query = session.query(TablePet).filter(or_(TablePet.owner_id == owner_id)).all()
  pets = []
  for pet in query:
    if pet != None: pets.append(convert_to_pet(pet))
  return pets

def find_pet(id: str) -> Pet:
  query = session.query(TablePet).filter(or_(TablePet.id == id)).first()
  if query == None: return None
  pet = convert_to_pet(query)
  
  return pet

def add_pet(pet: Pet) -> Pet:
  session.add(convert_to_table_pet(pet))
  session.commit()
  return pet

def change_pet(pet: Pet) -> Pet:
  session.begin_nested()
  query = session.query(TablePet).get(pet.id)
  if query == None: return None
  query.name = pet.name
  query.age = pet.age
  query.gender = pet.gender
  query.birthday = pet.birthday
  query.animal_id = pet.animal_id
  query.breed_id = pet.breed_id
  query.weight = pet.weight
  query.height = pet.height
  query.about = pet.about

  session.commit()
  return pet

def delete_pet(pet_id: str) -> str:
  query = session.query(TablePet).get(pet_id)
  if query == None: return None
  session.delete(query)

  session.commit()
  return pet_id
