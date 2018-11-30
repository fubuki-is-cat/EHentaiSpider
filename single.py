#coding:utf-8
#Author : VinylChloride
#Version : 0.1a

DOWNLOAD_PAGE_COUNT = 1
needLogin = False
username = ""
password = ""

import sys
sys.path.append("./lib")
from random import randint
import threading
import time
import os

from spider import EHentaiSpider

#Define Log Module

import logging
if (not os.path.exists("./log") or os.path.isfile("./log")):
	os.mkdir("./log")
logFileName = (str(time.ctime() + "_SingleSpider_Log.log").replace(":","-").replace(" ",""))
logger = logging.getLogger("EHentaiMain")
logFormat = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
logHandler = logging.FileHandler("./log/" + logFileName)
logHandler.setFormatter(logFormat)
logger.addHandler(logHandler)

#Log Level
logger.setLevel(logging.DEBUG)


if (__name__ == "__main__"):
	ehs = EHentaiSpider()
	ehs.setDownloadPage(DOWNLOAD_PAGE_COUNT)
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
	keyword = input("Searching Keyword : ")
	if (keyword.strip() == ""):
		sys.exit(0)
	ehs.search(keyword)

