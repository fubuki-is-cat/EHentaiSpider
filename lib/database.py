#coding:utf-8
#Author : VinylChloride

import sqlite3
import os
import sys

#Define Log Module

import logging
if (not os.path.exists("./log") or os.path.isfile("./log")):
	os.mkdir("./log")
logFileName = (str(time.ctime() + "_SQLite_Log.log").replace(":","-").replace(" ",""))
logger = logging.getLogger("EHentaiMain")
logFormat = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
logHandler = logging.FileHandler("./log/" + logFileName)
logHandler.setFormatter(logFormat)
logger.addHandler(logHandler)

#Log Level
logger.setLevel(logging.DEBUG)


class EHentaiDB(object):
	def __init__(self):
		self.__db = ""
		self.__dbConn = None
		self.__dbCsr = None

	def connect(self,dbFile):
		if (not os.path.exists(dbFile)):
			logger.critical("Db file not found.")
			return -1
		self.__db = dbFile;
		if ((self.__dbConn = sqlite3.connect(self.__db)) != None):
			if ((self.__dbCsr = self.__dbConn.cursor()) != None):
				logger.info("Db Connected.")
				return 0
		logger.error("Db Connection Failed.")
		return -1

	def addEHentaiData(publishedTime,resourcesPageLink,resourcesType,resourcesName,resourcesUploader,resourcesTorrentPageLink,resourcesTorrentData):
		pass
		

class dbOperation(object):
	def __init__(self,dbFile = None):
		if (not dbFile):
			logger.critical("Database Not Found.Exiting...")
			print("Database Not Found.Exiting...")
			sys.exit(1)
		self.dbConn = sqlite3.connect(dbFile)
		if (not self.dbConn):
			logger.critical("Could not connect to databse,Exiting...")
			print("Could not connect to databse,Exiting...")
			sys.exit(1)
		self.dbCursor = self.dbConn.cursor()
		if (not self.dbCursor):
			logger.critical("Could not get databse cursor,Exiting...")
			print(("Could not get databse cursor,Exiting..."))
			sys.exit(1)
		logger.info("Databse Initilized.")

		self.tableName = ""
		self.resPages = []
