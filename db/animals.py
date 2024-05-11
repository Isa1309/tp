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

def convert_to_user(user: TableAnimal) -> Animal:
  return Animal(
    id=user.id,
    name=user.name,
  )

def convert_to_table_user(user: Animal) -> TableAnimal:
  return TableAnimal(
    id=user.id,
    name=user.name,
  )

def get_animals() -> list[Animal]:
  query = session.query(TableAnimal).all()
  users = []
  for user in query:
    if user != None: users.append(convert_to_user(user))
  return users

def find_animal(id: str) -> Animal:
  query = session.query(TableAnimal).filter(or_(TableAnimal.id == id)).first()
  if query == None: return None
  user = convert_to_user(query)
  
  return user

def add_animal(user: Animal) -> Animal:
  session.add(convert_to_table_user(user))
  session.commit()
  return user
