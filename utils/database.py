from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from typing import Annotated
import os
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_URL = os.getenv("MYSQL_URL")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
SQLEngine=create_engine(f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_URL}:{MYSQL_PORT}/{MYSQL_DATABASE}")


def insert_into_database(session, data):
    session.add(data)
    session.commit()
    session.refresh(data)

def create_db_and_tables():
    SQLModel.metadata.create_all(SQLEngine)
    
def get_session():
    with Session(SQLEngine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]