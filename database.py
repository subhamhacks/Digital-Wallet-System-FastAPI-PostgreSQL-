#database

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker 
import os
from dotenv import load_dotenv

#Load vars from .env
load_dotenv()

#fetch database URL from .env file
DB_URL=os.getenv("DATABASE_URL")

#Create DB engine
engine = create_engine(DB_URL)

#Create Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base class for ORM models
Base = declarative_base()