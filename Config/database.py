from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# create database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# define file_record table
class file_record(Base):
    __tablename__ = 'file_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String, nullable=False)
    extracted_text = Column(Text)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Get a database session
# tao mot doi tuong dai dien hoat dong, thưc hien thao tac tren csdl
def get_db():
    db = SessionLocal()
    try:
        yield db # day la doi tuong dai dien
    finally:
        db.close()


