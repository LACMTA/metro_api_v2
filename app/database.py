# Using SQLAlchemy to connect to the Database

from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import Config

engine = create_engine(Config.DB_URI, echo=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = Session()

Base = declarative_base(metadata=MetaData(schema="metro_api"))

def get_db():
    db = Session()
    try:
        print('From database.py: ')
        print(type(db))
        yield db
    finally:
        db.close()