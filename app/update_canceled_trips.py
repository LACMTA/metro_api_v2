from app.config import Config
from app.utils.ftp_helper import *

TARGET_FILE = "CancelledTripsRT.json"
REMOTEPATH = '/nextbus/prod/'
LOCALPATH = 'app/data/'
# ftp_json_file_time = ''

def run_update():
    try:
        print('get_file_from_ftp')
        if connect_to_ftp(REMOTEPATH, Config.SERVER, Config.USERNAME, Config.PASS):
            get_file_from_ftp(TARGET_FILE, LOCALPATH)
            # ftp_json_file_time = file_modified_time
        disconnect_from_ftp()
    except Exception as e:
        print('FTP transfer failed')
        print(e)
        exit()
