from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from app.models.common import BaseModel
from app.core.config import settings
from app.models.engine import Engine
from app.models.general_vehicle_model import General_Vehicles

class DATABASE: 
# creat constructor function
# when class is used , below dunder function  will run automaticcally
# For make connection with Database:
  def __init__(self, db_url: str):
     self.db_url = db_url.replace('postgresql','postgresql+psycopg2')
     self.engine = create_engine(db_url)

# For make Session: 

  def init__db(self) -> None:
    try:
       print("start creating database tables")
       SQLModel.metadata.create_all(self.engine)
       print ("database tables created successfully")
    except Exception as e:
       print("failed to create database tables: {e}")
       raise


  def get_db_session(self) ->  Generator[Session,None,None]:
    with Session(self.engine) as session:
        try:
          yield session
        except Exception as e:
           print(f"failed to create database session :{e}")
           raise
        finally:
           session.close()

  

db = DATABASE(settings.DATABASE_URL)

def init_db() -> None:
    db.init__db()

def get_db_session() -> Generator[Session, None, None]:
   yield from db.get_db_session()









