import os
from dotenv import load_dotenv
from dotenv import dotenv_values

try:
    load_dotenv()
except:
    print('dotenv not found')
class Config:
    SWIFTLY_AUTH_KEY = os.environ.get('SWIFTLY_AUTH_KEY')
    SERVER = os.environ.get('FTP_SERVER')
    USERNAME = os.environ.get('FTP_USERNAME')
    PASS = os.environ.get('FTP_PASS')
    REMOTEPATH = '/nextbus/prod/'
    DEBUG = True
    REPODIR = "/gtfs_rail"