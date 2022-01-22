import os
import ftplib
from app.config import Config


WORKSPACE = os.environ.get('GITHUB_WORKSPACE')
TARGET_FILE = "CancelledTripsRT.json"

REMOTEPATH = '/nextbus/prod/'
directory = REMOTEPATH




ftp = ftplib.FTP(Config.SERVER)
ftp.login(Config.USERNAME, Config.PASS)


ftp.cwd(directory)
ftp.retrlines("LIST")
os.chdir("app/data/")


def get_file_from_ftp():
	for filename in ftp.nlst(TARGET_FILE): # Loop - looking for matching files
		if filename == TARGET_FILE:
			print("Found file: " + filename)
			fhandle = open(filename, 'wb')
			print('Opening Remote file: ' + filename) #for comfort sake, shows the file that's being retrieved
			transfer_result = ftp.retrbinary('RETR ' + filename, fhandle.write)
			fhandle.close()
			if transfer_result == '226 Transfer complete.':
				print('Transfer complete')
				return True
			else:
				print('Transfer failed')
				return False
	ftp.quit()


ftp_json_file_time = os.path.getmtime(TARGET_FILE)