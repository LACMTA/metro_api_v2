from .config import Config
from .utils.ftp_helper import *
from .utils.log_helper import *

TARGET_FILE = "CancelledTripsRT.json"
REMOTEPATH = '/nextbus/prod/'
LOCALPATH = 'app/data/'
# ftp_json_file_time = ''

logger.debug('update_canceled_trips.py loaded')

def run_update():
    try:
        logger.debug('run_update()')
        if connect_to_ftp(REMOTEPATH, Config.SERVER, Config.USERNAME, Config.PASS):
            get_file_from_ftp(TARGET_FILE, LOCALPATH)
            # ftp_json_file_time = file_modified_time
        disconnect_from_ftp()
    except Exception as e:
        logger.error('FTP transfer failed: ' + str(e))
