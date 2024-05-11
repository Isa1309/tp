from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.animals import Breed

Base = declarative_base()

class TableBreed(Base):
  __tablename__ = "breed"

  id = Column("id", String, primary_key=True)
  name = Column("name", String)
  animal_id = Column("animal_id", String)

  def __init__(self, id, name, animal_id):
    self.id = id
    self.name = name
    self.animal_id = animal_id

engine = create_engine("sqlite:///db/db/animals.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

def convert_to_breed(breed: TableBreed) -> Breed:
  return Breed(
    id=breed.id,
    name=breed.name,
    animal_id=breed.animal_id,
  )

def convert_to_table_breed(breed: Breed) -> TableBreed:
  return TableBreed(
    id=breed.id,
    name=breed.name,
    animal_id=breed.animal_id
  )

def get_breeds(animal_id: str) -> list[Breed]:
  query = session.query(TableBreed).filter(or_(TableBreed.animal_id == animal_id)).all()
  breeds = []
  for breed in query:
    if breed != None: breeds.append(convert_to_breed(breed))
  return breeds

def find_breed(id: str) -> Breed:
  query = session.query(TableBreed).filter(or_(TableBreed.id == id)).first()
  if query == None: return None
  breed = convert_to_breed(query)
  
  return breed

def add_breed(breed: Breed) -> Breed:
  session.add(convert_to_table_breed(breed))
  session.commit()
  return breed
