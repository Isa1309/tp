from sqlalchemy import create_engine, Column, String, or_, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.tasks import Task

Base = declarative_base()

class TableTask(Base):
  __tablename__ = "tasks"

  id = Column("id", String, primary_key=True)
  pet_id = Column("pet_id", String)
  owner_id = Column("owner_id", String)
  title = Column("title", String)
  description = Column("description", String)
  date = Column("date", Integer)

  def __init__(self, id, pet_id, owner_id, title, description, date):
    self.id = id
    self.pet_id = pet_id
    self.owner_id = owner_id
    self.title = title
    self.description = description
    self.date = date

engine = create_engine("sqlite:///db/db/tasks.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

def convert_to_task(task: TableTask) -> Task:
  return Task(
    id=task.id,
    pet_id=task.pet_id,
    owner_id=task.owner_id,
    title=task.title,
    description=task.description,
    date=task.date,
  )

def convert_to_table_task(task: Task) -> TableTask:
  return TableTask(
    id=task.id,
    pet_id=task.pet_id,
    owner_id=task.owner_id,
    title=task.title,
    description=task.description,
    date=task.date,
  )

def get_tasks(owner_id: str) -> list[Task]:
  query = session.query(TableTask).filter(or_(TableTask.owner_id == owner_id)).all()
  tasks = []
  for task in query:
    if task != None: tasks.append(convert_to_task(task))
  return tasks

def find_task(id: str) -> Task:
  query = session.query(TableTask).get(id)
  if query == None: return None
  task = convert_to_task(query)
  
  return task

def add_task(task: Task) -> Task:
  session.add(convert_to_table_task(task))
  session.commit()
  return task

def update_task(task: Task) -> Task:
  session.begin_nested()
  query = session.query(TableTask).get(task.id)
  if query == None: return None
  query.pet_id = task.pet_id
  query.title = task.title
  query.description = task.description
  query.date = task.date

  session.commit()
  return task

def delete_task(id: str) -> str:
  query = session.query(TableTask).get(id)
  if query == None: return None
  session.delete(query)

  session.commit()
  return id
