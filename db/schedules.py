from sqlalchemy import create_engine, Column, String, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.schedules import Schedule

Base = declarative_base()

class TableSchedule(Base):
  __tablename__ = "schedules"

  id = Column("id", String, primary_key=True)
  pet_id = Column("pet_id", String)
  owner_id = Column("owner_id", String)
  time = Column("time", String)

  def __init__(self, id, pet_id, owner_id, time):
    self.id = id
    self.pet_id = pet_id
    self.owner_id = owner_id
    self.time = time

engine = create_engine("sqlite:///db/db/schedules.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)()

def convert_to_schedule(schedule: TableSchedule) -> Schedule:
  return Schedule(
    id=schedule.id,
    pet_id=schedule.pet_id,
    owner_id=schedule.owner_id,
    time=schedule.time.split(";"),
  )

def convert_to_table_schedule(schedule: Schedule) -> TableSchedule:
  return TableSchedule(
    id=schedule.id,
    pet_id=schedule.pet_id,
    owner_id=schedule.owner_id,
    time=";".join(schedule.time),
  )

def get_schedules(owner_id: str) -> list[Schedule]:
  query = session.query(TableSchedule).filter(or_(TableSchedule.owner_id == owner_id)).all()
  schedules = []
  for schedule in query:
    if schedule != None: schedules.append(convert_to_schedule(schedule))
  return schedules

def find_schedule_by_pet_id(pet_id: str) -> Schedule:
  query = session.query(TableSchedule).filter(or_(TableSchedule.pet_id == pet_id)).first()
  if query == None: return None
  schedule = convert_to_schedule(query)
  
  return schedule

def find_schedule(id: str) -> Schedule:
  query = session.query(TableSchedule).get(id)
  if query == None: return None
  schedule = convert_to_schedule(query)
  
  return schedule

def add_schedule(schedule: Schedule) -> Schedule:
  session.add(convert_to_table_schedule(schedule))
  session.commit()
  return schedule

def update_schedule(schedule: Schedule) -> Schedule:
  session.begin_nested()
  query = session.query(TableSchedule).get(schedule.id)
  if query == None: return None
  query.pet_id = schedule.pet_id
  query.owner_id = schedule.owner_id
  query.time = ";".join(schedule.time)

  session.commit()
  return schedule

def delete_schedule(id: str) -> str:
  query = session.query(TableSchedule).get(id)
  if query == None: return None
  session.delete(query)

  session.commit()
  return id
