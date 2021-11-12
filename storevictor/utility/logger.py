import logging
import os
from django.conf import settings

logfile = os.path.join(settings.BASE_DIR,'app.log')

logging.basicConfig(filename=logfile, filemode='a', format='%(name)s - %(levelname)s - %(message)s')

def appLogs(*error_msg):

	for error in error_msg:
		logging.error(error)
	
	return
