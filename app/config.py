import os
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig
# from dotenv import dotenv_values

try:
    load_dotenv()
    print('.env loaded')
except Exception as e:
    print(e)
    try:
        from .secrets import *
        load_secrets()
        print(os.environ.get('FTP_USERNAME'))
    except Exception as e:
        print(e)
class Config:
    DB_URI = os.environ.get('URI')
    SECRET_KEY = os.environ.get('HASH_KEY')
    ALGORITHM = os.environ.get('HASHING_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES  = 0
    SWIFTLY_AUTH_KEY_BUS = os.environ.get('SWIFTLY_AUTH_KEY_BUS')
    SWIFTLY_AUTH_KEY_RAIL = os.environ.get('SWIFTLY_AUTH_KEY_RAIL')
    SERVER = os.environ.get('FTP_SERVER')
    USERNAME = os.environ.get('FTP_USERNAME')
    PASS = os.environ.get('FTP_PASS')
    REMOTEPATH = '/nextbus/prod/'
    DEBUG = True
    REPODIR = "/gtfs_rail"
    CURRENT_VERSION = "2.0.5"
    API_LAST_UPDATE_TIME = os.path.getmtime(r'app/main.py')


conf = ConnectionConfig(
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM = os.environ.get('MAIL_FROM'),
    MAIL_PORT = os.environ.get('MAIL_PORT'),
    MAIL_SERVER = os.environ.get('MAIL_SERVER'),
    MAIL_TLS = os.environ.get('MAIL_TLS'),
    MAIL_SSL = os.environ.get('MAIL_SSL'),
    USE_CREDENTIALS = os.environ.get('USE_CREDENTIALS'),
    VALIDATE_CERTS = os.environ.get('VALIDATE_CERTS')
)