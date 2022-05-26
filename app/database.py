# Using SQLAlchemy to connect to the Database

from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import Config
from .utils.log_helper import *

engine = create_engine(Config.DB_URI, echo=False)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = Session()

Base = declarative_base(metadata=MetaData(schema="metro_api"))

def get_db():
    db = Session()
    try:
        logger.info('Connected to the database')
        yield db
    finally:
        db.close()