from .config import Config
from .utils.ftp_helper import *
from .utils.log_helper import *

TARGET_FILE = "CancelledTripsRT.json"
REMOTEPATH = '/nextbus/prod/'
LOCALPATH = 'app/data/'
# ftp_json_file_time = ''

def run_update():
    try:
        logger.info('pulling CancelledTripsRT.json from FTP')
        if connect_to_ftp(REMOTEPATH, Config.SERVER, Config.USERNAME, Config.PASS):
            get_file_from_ftp(TARGET_FILE, LOCALPATH)
            # ftp_json_file_time = file_modified_time
            Config.API_LAST_UPDATE_TIME = os.path.getmtime(LOCALPATH + TARGET_FILE)
        disconnect_from_ftp()
    except Exception as e:
        logger.exception('FTP transfer failed: ' + str(e))
