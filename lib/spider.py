#coding : utf-8

import sys
sys.path.append("./lib")
import requests
from requests import exceptions as requestsErr
from random import randint
from bs4 import BeautifulSoup
import time
import os
import json
import re

import logging
logFileName = (str(time.ctime() + "_Spider_Log.log").replace(":","-").replace(" ",""))
logger = logging.getLogger("Spider")
logFormat = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
logHandler = logging.FileHandler("./log/" + logFileName)
logHandler.setFormatter(logFormat)
logger.addHandler(logHandler)

#Log Level
logger.setLevel(logging.DEBUG)


class Spider(object):
	def __init__(self):
		logger.info("Spider Framework Loaded.")
		self.isUAFileExists = False
		self.isProxyFileExists = False
		self.retryList = []
		self.Session = requests.Session()

	def randomUA(self):
		userAgentList = []
		if (not os.path.exists("ua.txt")):
			logger.warn("Could not find User Agent File.")
			print("Warring : Could not find User Agent file.")
			self.isUAFileExists = False
		else:
			self.isUAFileExists = True
		if (self.isUAFileExists):
			with open("ua.txt","r+") as uaFile:
				userAgentList = uaFile.readlines()
				uaFile.close()
			if (userAgentList == []):return
			return (userAgentList[randint(0,len(userAgentList) - 1)]).strip()

	def randomProxy(self):
		proxyList = []
		if (not os.path.exists("proxy.txt")):
			logger.warn("Could not find proxy file.")
			print("Warring : Could not find proxy file.")
			self.isProxyFileExists = False
		else:
			self.isProxyFileExists = True

		if (self.isProxyFileExists):
			with open("proxy.txt","r+") as proxyFile:
				proxyList = proxyFile.readlines()
				proxyFile.close()
			if (proxyList == []):return 
			return (proxyList[randint(0,len(proxyList) - 1)]).strip()

	def postPage(self,URL,data = {}):
		try:
			header = {}
			header['User-Agent'] = self.randomUA()
			proxy = {}
			proxy['http'] = self.randomProxy()
			try:
				logger.debug("Requests : %s\nUsing Header : %s\nUsing Proxy : %s" % (URL,str(header),str(proxy)))
				response = self.Session.post(URL,data=data,headers = header,proxies = proxy)
			except requestsErr.ConnectionError:
				self.retryList.append(URL)
				logger.error("Connection Refused By Server On Link : %s , Try Again Later." % URL)
				print ("Connection Refused By Server On Link : %s , Try Again Later." % URL)
				logger.exception("")
				return -1
			except:
				logger.exception("Error On Requests Page.")
				return -1;
			if (response.status_code == requests.codes.ok):
				logger.debug("Successfully Requests : %s" % URL)
				return response
			else:
				logger.error("Error On Requests Page : %s With Code : %s" % (URL,str(response.status_code)))
				return -1
		except:
			logger.exception("Error On Requests Page : %s" % URL)
			return -1

	def requestPage(self,URL):
		try:
			header = {}
			header['User-Agent'] = self.randomUA()
			proxy = {}
			proxy['http'] = self.randomProxy()
			try:
				logger.debug("Requests : %s\nUsing Header : %s\nUsing Proxy : %s" % (URL,str(header),str(proxy)))
				response = self.Session.get(URL,headers = header,proxies = proxy)
			except requestsErr.ConnectionError:
				self.retryList.append(URL)
				logger.error("Connection Refused By Server On Link : %s , Try Again Later." % URL)
				print ("Connection Refused By Server On Link : %s , Try Again Later." % URL)
				return -1
			except:
				logger.exception("Error On Requests Page.")
				return -1;
			if (response.status_code == requests.codes.ok):
				logger.debug("Successfully Requests : %s" % URL)
				return response
			else:
				logger.error("Error On Requests Page : %s With Code : %s" % (URL,str(response.status_code)))
				return -1
		except:
			logger.exception("Error On Requests Page : %s" % URL)
			return -1


class EHentaiSpider(Spider):

	def __init__(self):
		Spider.__init__(self)

		self.__downloadPage = 1
		self.__loginUrl = "https://forums.e-hentai.org/index.php?act=Login&CODE=01"
		self.__searchUrl = "https://e-hentai.org/?f_doujinshi=%d&f_manga=%d&f_artistcg=%d&f_gamecg=%d&f_western=%d&f_non-h=%d&f_imageset=%d&f_cosplay=%d&f_asianporn=%d&f_misc=%d&f_search=%s&f_apply=Apply+Filter"

	def setDownloadPage(self,page):
		self.__downloadPage = page

	def search(self,keyword):
		print("Searching : %s" % keyword)
		logger.info("Searching : %s" % keyword)
		searchUrl = self.__querySearchUrl(keyword)
		rep = self.requestPage(searchUrl)
		if (rep == -1):
			print("Request failed with keyword : %s" % keyword)
			return -1
		if ("No hits found" in rep.text):
			print("No hits found.")
			loggin.info("No hits found.")
			return -2
		bs = BeautifulSoup(rep.text,"html.parser")
		
		#get page count
		pageCount = 0
		for item in bs.find_all("td",{'onclick':"document.location=this.firstChild.href"}):
			for childItem in item.children:
				#print type(childItem)
				if (str(type(childItem)) == "<class \'bs4.element.Tag\'>" and childItem.name == "a"):
					try:
						cPageCount = int(childItem.string)
					except ValueError:
						continue
					if (cPageCount > pageCount):pageCount=cPageCount

		print("Total Pages : %d" % pageCount)
		logger.info("Total Pages : %d" % pageCount)

		if (self.__downloadPage == -1):
			pass
		elif (pageCount > self.__downloadPage):
			pageCount = self.__downloadPage
		logger.info("Selected Pages : %d" % pageCount)
		print ("Selected Pages : %d" % pageCount)
		for i in range(0,pageCount):
			tmpUrl = searchUrl
			if (i != 0):
				tmpUrl += "&page=%d" % i

			rep = self.requestPage(searchUrl)
			if (rep == -1):
				print("Request failed with keyword : %s on page : %d" % (keyword,i+1))
				logger.error("Request failed with keyword : %s on page : %d" % (keyword,i+1))
				continue
			pageRep = self.requestPage(tmpUrl)
			if (pageRep == -1):
				print ("Failed on request page : %s" % tmpUrl)
				logger.error("Failed on request page : %s" % tmpUrl)
				continue
			pageBs = BeautifulSoup(pageRep.text,"html.parser")
			for pageItem in pageBs.find_all("tr",{"class":"gtr0"}):
				logger.debug(pageItem)
				self.__getResBaseInfo(pageItem)
			for pageItem in pageBs.find_all("tr",{"class":"gtr1"}):
				logger.debug(pageItem)
				self.__getResBaseInfo(pageItem)


	def login(self):
		global username
		global password
		try:
			data = {
					"referer": "https://forums.e-hentai.org/index.php?act=Login&CODE=00",
					"b":"", 
					"bt":"", 
					"UserName": username,
					"PassWord": password,
					"CookieDate": "1"
				}
			rep = self.postPage(self.__loginUrl,data)
			if (rep == -1):
				logger.critical("Login Failed")
				return False
			#logger.debug(rep.text)
			if ("You are now logged in as" in rep.text):
				return True
			elif ("IF YOU DO NOT SEE THE CAPTCHA, ENABLE JAVASCRIPT AND DISABLE YOUR ADBLOCKER" in rep.text):
				print("Captcha required,login failed.")
				logger.critical("Captcha required,login failed.")
				return False
			logger.critical("Login Failed : \n"+rep.text)

			return False
		except :
			logger.exception("Login Error : ")
			return False

	def __getTorrentInfo(self,torrentPageUrl):
		try:
			_dict = {
				"list":[
					#Torrent Dict info
					#For Example:
					#{
					#	"torrentURL":"XXXX",
					#	"torrentPostedTime":"XXXX",
					#	"fileSize":"xxx MB",
					#	"fileName":"XXXX",
					#	"torrentUploader":"XXX"
					#}
				]
			}
			_list = []
			_doneList = []
			rep = self.requestPage(torrentPageUrl)
			if (rep == -1):
				logger.error("Could not request torrent page : %s" % torrentPageUrl)
				print ("Could not request torrent page : %s" % torrentPageUrl)
				return False
			bs = BeautifulSoup(rep.text,"html.parser")
			for item in bs.find_all("form",{"method":"post","action":True}):
				torrentDict = {
					"torrentURL":"",
					"torrentPostedTime":"",
					"fileSize":"",
					"fileName":"",
					"torrentUploader":""
				}
				childBS = BeautifulSoup(str(item),"html.parser")
				for childItem in childBS.find_all("td"):
				#	logger.debug(childItem)
					for gChildItem in childItem.children:
						#logger.debug(list(childItem.children))
						#logger.debug(gChildItem)
						if (str(gChildItem.name) == 'span'):
							if (str(gChildItem.string) == "Posted:"):
								torrentDict['torrentPostedTime'] = list(childItem.children)[1]
							elif(str(gChildItem.string) == "Size:"):
								torrentDict['fileSize'] = list(childItem.children)[1]
							elif(str(gChildItem.string) == "Uploader:"):
								torrentDict['torrentUploader'] = list(childItem.children)[1]
						elif(str(gChildItem.name) == "a" and gChildItem.has_attr("href") and gChildItem.has_attr("onclick")):
							torrentDict['torrentURL'] = gChildItem['href']
							torrentDict['fileName'] = gChildItem.string
					try:
					#	logger.debug(torrentDict)
						pass
					except UnicodeEncodeError:
						pass
					if (torrentDict["torrentURL"].replace(" ","") != ""):
						_list.append(torrentDict)
			for item in _list:
				#logger.debug(item)
				#logger.debug(_doneList)
				if (item["torrentURL"] not in _doneList):
					if (re.sub("\s",'',item["torrentURL"]) == ""):continue
					print (re.sub("\s",'',item["torrentURL"]))
					self.__downloadTorrent(item["torrentURL"])
					_doneList.append(item["torrentURL"])
		except:
			logger.exception("Exception on downloading torrent file.")
			print ("Exception on downloading torrent file.Checking log file.")

	def __downloadTorrent(self,url):
		try:
			if (url == ""): return
			filename = url[url.rfind("/")+1:]
			print("Downloading : %s , filename : %s" % (url,filename))
			logger.info("Downloading : %s , filename : %s" % (url,filename))
			rep = self.requestPage(url)
			if (rep == -1):
				logger.error("Download %s Failed." % url)
				print("Download %s Failed." % url)
				return -1
			with open("./torrent/" + filename,"wb+") as f:
				f.write(rep.content)
				f.close()
			print("Downloaded %s " % url)
			logger.info("Downloaded %s " % url)
		except:
			logger.exception("")


	def __getResBaseInfo(self,pageItem):
		try:
			publishedTime = ""
			resourcesPageLink = ""
			resourcesType = ""
			resourcesName = ""
			resourcesUploader = ""
			resourcesTorrentPageLink = ""
			resourcesTorrentData = ""
			bs = BeautifulSoup(str(pageItem),"html.parser")
			for tmpItem in bs.find_all("a",{"href":True,"onmouseover":True,"onmouseout":True}):
				#logger.debug(tmpItem)
				#return
				resourcesPageLink = tmpItem['href']
				resourcesName = (tmpItem.string)
			for tmpItem in bs.find_all("a",{'href':True,"onclick":True,"onmouseout":False,"onmouseover":False,"rel":True}):
				logger.debug(tmpItem['href'])
				resourcesTorrentPageLink = tmpItem['href']
			#	resourcesTorrentData = self.__getTorrentInfo(resourcesTorrentPageLink)
				resourcesTorrentData = None
				if not resourcesTorrentData:resourcesTorrentData = "";
			for pageItemChild in pageItem.children:
				#print pageItemChild['class']
				#logger.debug(pageItemChild)
				if (str(pageItemChild.name) == "div" and pageItemChild.has_attr("class") and str(pageItemChild['class']) == "itu"):
						resourcesUploader = (pageItemChild.a.string)
				if (str(pageItemChild.name) == "td" and pageItemChild.has_attr("style")):
					publishedTime = str(pageItemChild.string)
				try:
					if (pageItemChild.has_attr("class") and pageItemChild['class'][0] == 'itdc'):
						resourcesType = pageItemChild.img["alt"]
				except:
					print("Could not get resources type,check log file.")
					logger.exception("Could not get resources type")
			logger.debug("publishedTime : %s \n resourcesPageLink : %s \n resourcesType : %s \n resourcesName : %s \n resourcesUploader : %s \n resourcesTorrentPageLink : %s \n resourcesTorrentData : %s " % (publishedTime,resourcesPageLink,resourcesType,resourcesName,resourcesUploader,resourcesTorrentPageLink,resourcesTorrentData))
			self.__getTorrentInfo(resourcesTorrentPageLink)
		except:
			logger.exception("Could not get resources base info.")
			print("Could not get resources base info.")
			return -1

	def __querySearchUrl(self,keyword,doujinshi = 0,manga = 0,artistcg = 0,gamecg = 0,western = 0,nonh = 0,imageset = 0,cosplay = 0,asianporn = 0,misc = 0):
		return (self.__searchUrl % (doujinshi,manga,artistcg,gamecg,western,nonh,imageset,cosplay,asianporn,misc,keyword))


