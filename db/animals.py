from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.animals import Animal

Base = declarative_base()

class TableAnimal(Base):
  __tablename__ = "animals"

  id = Column("id", String, primary_key=True)
  name = Column("name", String)

  def __init__(self, id, name):
    self.id = id
    self.name = name

engine = create_engine("sqlite:///db/db/animals.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

def convert_to_animal(animal: TableAnimal) -> Animal:
  return Animal(
    id=animal.id,
    name=animal.name,
  )

def convert_to_table_animal(animal: Animal) -> TableAnimal:
  return TableAnimal(
    id=animal.id,
    name=animal.name,
  )

def get_animals() -> list[Animal]:
  query = session.query(TableAnimal).all()
  animals = []
  for animal in query:
    if animal != None: animals.append(convert_to_animal(animal))
  return animals

def find_animal(id: str) -> Animal:
  query = session.query(TableAnimal).filter(or_(TableAnimal.id == id)).first()
  if query == None: return None
  animal = convert_to_animal(query)
  
  return animal

def add_animal(animal: Animal) -> Animal:
  session.add(convert_to_table_animal(animal))
  session.commit()
  return animal
