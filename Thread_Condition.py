import threading
import random
import logging
import time

count = 5
exitFlag = 0

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')

#	==========================Function==========================

class Product_Thread(threading.Thread):
	def __init__(self ,datas:list ,cond:threading.Condition ,thread_name=None):
		threading.Thread.__init__(self)
		self.datas = datas
		self.cond = cond
		
		if thread_name is not None:
			self.name = thread_name
			
	def run(self):
		global exitFlag
		global count
		while True:
			try:
				if exitFlag:
					break
				
				if count <= 0:
					exitFlag = 1
				
				data = random.randint(1,100)
				logging.info(data)
				self.datas.append(data)
				self.cond.acquire()
				self.cond.notify()
				self.cond.release()
				count-=1
				time.sleep(1)
			except Exception as ex:
				print("Error: {0}".format(ex))
				exitFlag = 1
				break
		print("Exit Thread:{0}".format(self.name))

class Consumer_Thread(threading.Thread):
	def __init__(self ,datas:list ,cond:threading.Condition ,thread_name=None):
		threading.Thread.__init__(self)
		self.datas = datas
		self.cond = cond
		
		if thread_name is not None:
			self.name = thread_name
			
	def run(self):
		global exitFlag
		global count
		while True:
			try:
				if exitFlag:
					break
			
				self.cond.acquire()
			
				if len(self.datas) > 0:
					data = self.datas.pop()
					logging.info(data)
					
				self.cond.wait()
				self.cond.release()
			except Exception as ex:
				print("Error: {0}".format(ex))
				exitFlag = 1
				
		print("Exit Thread:{0}".format(self.name))

#	==========================main==========================

if __name__ == '__main__' :
	try:

		Threads = []
		datas = []
		cond = threading.Condition()
	
		th_P = Product_Thread(datas,cond,"Product")
		th_C = Consumer_Thread(datas,cond,"Consumer")
	
		Threads.append(th_P)
		th_P.start()
		Threads.append(th_C)
		th_C.start()
	
		# 等待所有线程完成
		for t in Threads:
			t.join()

	except Exception as ex:
		print("Error: {0}".format(ex))

	input("Press Enter to continue...\n")