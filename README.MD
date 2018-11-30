

# EHentai Spider

 - [Introduction](#Introduction)
 - [Features](#Features)
 - [Quick Start](#Quick-Start)
 - [Detailed Configuration](#Detailed-Configuration)
 - [User-Agent Configuration](#User-Agent-Configuration)
 - [Proxy Configuration](#Proxy-Configuration)

## Introduction
This is a program that automatically searches for resources on EHentai by keyword and automatically downloads torrent files. Distributed deployment programs are supported through Python MultiProcessing.

## Features

 - [x] Support distributed deployment
 - [x] Support for randomizing UserAgents through a customized list of UAs
 - [x] Support for randomizing agents through a custom proxy list

## Quick Start
### Single Mode
```
python single.py
```
and enter the keyword and the torrent file on the first page of the search results will be automatically downloaded.
### Distributed Mode

 1. Modify the connection information at the beginning of the server.py file and run the server.py file on the server.
 2. Confirm that the firewall has released the corresponding port.
 3. Modify the information at the beginning of the client.py and client_task_uploader.py files, and then run client.py on the client, the program will automatically connect to the server and wait for the task; run client_task_uploader.py, the program can upload the task to the server after connecting to the server.

## Detailed Configuration
- serverHost : The address of server.
- serverPort : The port of server.
- serverAuth : The authentication code of server.
- REFUSED_SLEEP_TIME : The wait time for automatic retry when the server rejects the connection. The unit is seconds.
- EMPTY_SLEEP_TIME : Retry the wait time when the server task list is empty. The unit is seconds.
- DOWNLOAD_PAGE_COUNT : The results of the first x pages in the search result list are automatically downloaded, and all are downloaded when the value is -1.
- needLogin : Whether you need to log in, the value is a Boolean value.

## User-Agent Configuration
The UA list is stored in the "ua.txt" file, one data per line. Examples of data values are as follows:
`Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36`

## Proxy Configuration
The proxy list is stored in the "proxy.txt" file, one proxy per line, and currently supports http proxy. An example is as follows:
`http://127.0.0.1:1080`







