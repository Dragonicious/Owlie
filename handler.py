import logging
logger = logging.getLogger('rpi')
logger.setLevel(logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s | %(threadName)-12.12s | %(levelname)-10.10s | %(message)s","%m-%d %H:%M:%S")

consoleLogger = logging.StreamHandler()
consoleLogger.setLevel(logging.DEBUG)
consoleLogger.setFormatter(logFormatter)

fileLogger = logging.FileHandler(r'debug.log')
fileLogger.setLevel(logging.DEBUG)
fileLogger.setFormatter(logFormatter)

logger.addHandler(consoleLogger)
logger.addHandler(fileLogger)



import subprocess
import threading
import os
import sys
from time import sleep
# from run import owlie


PID = os.getpid()
with open("PID_HANDLER.txt","w") as PID_FILE:
	PID_FILE.write(str(PID))
	logger.debug('Handler trace created: ' + str(PID))


class owl:

	def __init__(self):
		self.config_os() #determines OS
		self.handler = threading.Thread(target=self.owlie_handler)
		self.handler.start()



		# self.ui = threading.Thread(target=self.interface)
		# self.ui.start()
		# print(str(self.ui),flush=True)

		CURRENT_PID = ""

	def interface(self):
		while True:
			print("""Actions:
				1. Owlie status
				2. PID""",flush=True)
			action = input()

			if action == '1':
				print("Thread: " + str(self.handler.isAlive()) + " -- " + str(self.handler),flush=True)
			elif action == '2':
				print("PID: ", self.CURRENT_PID)



	def config_os(self):
		opsys = sys.platform
		if opsys in ['win32', 'win64']:
			self.platform = 'win'
		else:
			self.platform = 'linux'
		print("os:",opsys,flush=True)




	def PID_running(self):
		try:
			with open("PID.txt","r") as PID_FILE:
				PID = int(PID_FILE.read())
		except FileNotFoundError:
			return False
		except Exception as e:
			logger.critical("Can't open PID file.: "+str(e.__class__.__name__)+'\n'+str(e.args))
		else:
			if(os.path.exists("/proc/"+str(PID))):
				return True
			else:
				logger.warning('Process file not found')
				return False
			self.CURRENT_PID = str(PID)

	def owlie_handler(self):
		while True:
			if self.PID_running():
				sleep(5)
			else:
				owlie = subprocess.Popen(['/bin/sh', os.path.expanduser('startup.sh')])
				logger.debug("Starting new Owlie. PID: " +str(owlie.pid))
			sleep(5)

if __name__ == "__main__":
	owl = owl()