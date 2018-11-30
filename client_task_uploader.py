#coding:utf-8
#Author : VinylChloride
#Version : 0.1a

serverHost = '127.0.0.1'
serverPort = 10086
serverAuth = b'Password'

import sys
sys.path.append("./lib")
import queue
import time
import os

from taskclient import TaskClient

#Define Log Module

import logging
if (not os.path.exists("./log") or os.path.isfile("./log")):
	os.mkdir("./log")
logFileName = (str(time.ctime() + "_TaskUploader_Log.log").replace(":","-").replace(" ",""))
logger = logging.getLogger("TaskUploader")
logFormat = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
logHandler = logging.FileHandler("./log/" + logFileName)
logHandler.setFormatter(logFormat)
logger.addHandler(logHandler)

#Log Level
logger.setLevel(logging.DEBUG)

if (__name__ == "__main__"):
	tc = TaskClient(serverHost,serverPort,serverAuth)
	tc.begin()
	while(True):
		keyword = input("Enter KeyWord : ")
		if (keyword.strip() == ""):
			continue
		tc.putTask(keyword)

