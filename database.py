from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

""" SQLALCHEMY_DATABASE_URL = 'sqlite:///./database.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
 """
 
# PostgreSQL Database URL
DATABASE_URL = "postgresql://administrator:mypassword@localhost:5432/cofoundr"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 #No need for Declarative base in SqlModel
""" Base = declarative_base() """
 
 
 # Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
