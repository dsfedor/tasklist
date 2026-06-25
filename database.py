from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings
 
#DATABASE_URL = "postgresql+psycopg://tasklist:tasklist@localhost:5432/tasklist"
 
engine = create_engine(settings.database_url)
 
 
class Base(DeclarativeBase):
    pass
 
 
SessionLocal = sessionmaker(bind=engine)

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()