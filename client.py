#coding:utf-8
#Author : VinylChloride
#Version : 0.1a

REFUSED_SLEEP_TIME = 60
EMPTY_SLEEP_TIME = 10
DOWNLOAD_PAGE_COUNT = 1
needLogin = False
username = ""
password = ""
serverHost = '127.0.0.1'
serverPort = 10086
serverAuth = b'Password'

import sys
sys.path.append("./lib")
from random import randint
import threading
import time
import os
import json
import re
from taskclient import TaskClient
from spider import EHentaiSpider

#Define Log Module

import logging
if (not os.path.exists("./log") or os.path.isfile("./log")):
	os.mkdir("./log")
logFileName = (str(time.ctime() + "_Client_Log.log").replace(":","-").replace(" ",""))
logger = logging.getLogger("Client")
logFormat = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
logHandler = logging.FileHandler("./log/" + logFileName)
logHandler.setFormatter(logFormat)
logger.addHandler(logHandler)

#Log Level
logger.setLevel(logging.DEBUG)

"""
if (__name__ == "__main__"):
	tc = TaskClient()
	tc.begin()
	tc.getTask()
"""

if (__name__ == "__main__"):
	ehs = EHentaiSpider()
	ehs.setDownloadPage = DOWNLOAD_PAGE_COUNT
	if (needLogin):
		print("Starting login.")
		logger.info("Starting login.")
		if (ehs.login()):
			print("Logged.")
			logger.info("Logged.")
		else:
			print ("Failed.")
			logger.critical("Failed")
			sys.exit(-1)
	else:
		print("Skip login.")
		logger.info("Skip login.")
	tc = TaskClient(serverHost,serverPort,serverAuth)
	while True:
		if (tc.begin() == -1):
			print("Server refused connection.Try again in %d secs" % REFUSED_SLEEP_TIME)
			logger.error("Server refused connection.Try again in %d secs" % REFUSED_SLEEP_TIME)
			time.sleep(REFUSED_SLEEP_TIME)
			continue
		break
	while True:
		keyword = tc.getTask()
		if (keyword == -1):
			print("Task queue empty.sleep %d secs." % EMPTY_SLEEP_TIME)
			logger.info("Task queue empty.sleep %d secs." % EMPTY_SLEEP_TIME)
			time.sleep(EMPTY_SLEEP_TIME)
			continue
		if (keyword == -2):
			sys.exit(-1)
		logger.info("Got task %s from server." % keyword)
		ehs.search(keyword)
		print("Task : %s Done." % keyword)
		logger.info("Task : %s Done." % keyword)
	"""
	if (keyword.strip() == ""):
		sys.exit(0)
	ehs.search(keyword)
	"""
