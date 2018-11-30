#coding:utf-8
#Author : VinylChloride
#Version : 0.1a

serverHost = '127.0.0.1'
serverPort = 10086
serverAuth = b'Password'

import sys
sys.path.append("./lib")
import random, time, queue
from multiprocessing.managers import BaseManager

task_queue = queue.Queue()
result_queue = queue.Queue()

class QueueManager(BaseManager):
	pass

if (__name__ == "__main__"):
	QueueManager.register('get_task_queue', callable=lambda: task_queue)
	QueueManager.register('get_result_queue', callable=lambda: result_queue)
	manager = QueueManager(address=(serverHost, serverPort), authkey=serverAuth)
	serve = manager.get_server()
	print("Listening %s:%d with authkey : %s" % (serverHost,serverPort,str(serverAuth)))
	serve.serve_forever()



