import os, ftplib

from .log_helper import *

ftp_client = None
ftp_server = ''
file_modified_time = None

def connect_to_ftp(remote_dir, server, user, pw):
	global ftp_client 
	global ftp_server
	ftp_server = server
	
	ftp_client = ftplib.FTP(server)
	login_result = ftp_client.login(user, pw)
	
	if '230' in login_result:
		logger.info("Successfully connected to " + server)
		ftp_client.cwd(remote_dir)
		logger.info("In remote directory: " + ftp_client.pwd())
		return True
	else:
		logger.error("Failed to connect to " + server)
		return False
	#ftp.retrlines("LIST")

def get_file_from_ftp(file, local_dir):
	global file_modified_time
	for filename in ftp_client.nlst(file): # Loop - looking for matching files
		if filename == file:
			fhandle = open(local_dir + filename, 'wb')
			logger.info('Opening remote file: ' + filename) #for comfort sake, shows the file that's being retrieved
			transfer_result = ftp_client.retrbinary('RETR ' + filename, fhandle.write)
			file_modified_time = os.path.getmtime(local_dir + filename)
			logger.info('File modified time: ' + str(file_modified_time))
			
			if '226' in transfer_result:
				logger.info('Transfer complete: ' + local_dir + filename)
				fhandle.close()
				return True
			else:
				logger.info('Transfer failed: ' + transfer_result)
				fhandle.close()
				return False

def disconnect_from_ftp():
	ftp_client.quit()
	logger.info("Disconnected from " + ftp_server)