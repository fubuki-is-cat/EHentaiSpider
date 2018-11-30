#coding : utf-8


import sys
sys.path.append("./lib")
from multiprocessing.managers import BaseManager
import queue
from random import randint
import time
import os

import logging
logFileName = (str(time.ctime() + "_TaskClient_Log.log").replace(":","-").replace(" ",""))
logger = logging.getLogger("TaskClient")
logFormat = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
logHandler = logging.FileHandler("./log/" + logFileName)
logHandler.setFormatter(logFormat)
logger.addHandler(logHandler)

#Log Level
logger.setLevel(logging.DEBUG)


class QueueManager(BaseManager):
	pass

class TaskClient(object):
	def __init__(self,serverHost,serverPort,serverAuth):
		QueueManager.register('get_task_queue')
		QueueManager.register('get_result_queue')
		self.__qm = QueueManager(address=(serverHost,serverPort),authkey = serverAuth)
		self.__task = None
		self.__result = None

	def begin(self):
		try:
			self.__qm.connect()
			self.__task = self.__qm.get_task_queue()
		except ConnectionRefusedError:
			return -1
		except Exception as e:
			print("Exception %s on connect to server." % str(e))
			logger.exception("Could not connect to server.")

	def getTask(self):
		try:
			#self.__task.put("Hello")
			keyword = self.__task.get(timeout=10)
			return keyword
		except queue.Empty:
			logger.info("Server Task Queue Empty.")
			return -1
		except Exception as e:
			logger.exception("")
			return -2

	def putTask(self,task):
		try:
			logger.info("Upload Task : %s" % task)
			print ("Upload Task : %s" % task)
			self.__task.put(task)
			logger.info("Uploaded Task : %s" % task)
			print ("Uploaded Task : %s" % task)
		except Exception as e:
			logger.exception("")
			print ("Upload Task : %s Failed." % task)
			return -1

