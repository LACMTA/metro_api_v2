import os
from dotenv import load_dotenv

from .utils.log_helper import *

try:
    load_dotenv('.env')
    logger.info('Environment variables loaded from .env file')
except Exception as e:
    logger.exception('Environment variables not loaded from .env file: ' + str(e))

class Config:
    DB_URI = os.environ.get('URI')
    SECRET_KEY = os.environ.get('HASH_KEY')
    ALGORITHM = os.environ.get('HASHING_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES  = 30
    SWIFTLY_AUTH_KEY_BUS = os.environ.get('SWIFTLY_AUTH_KEY_BUS')
    SWIFTLY_AUTH_KEY_RAIL = os.environ.get('SWIFTLY_AUTH_KEY_RAIL')
    SERVER = os.environ.get('FTP_SERVER')
    USERNAME = os.environ.get('FTP_USERNAME')
    PASS = os.environ.get('FTP_PASS')
    REMOTEPATH = '/nextbus/prod/'
    DEBUG = True
    REPODIR = "/gtfs_rail"
    CURRENT_VERSION = "2.0.13"
    API_LAST_UPDATE_TIME = os.path.getmtime(r'app/main.py')
    LOGZIO_TOKEN = os.environ.get('LOGZIO_TOKEN')
    LOGZIO_URL = os.environ.get('LOGZIO_URL')
    RUNNING_ENV = os.environ.get('RUNNING_ENV')