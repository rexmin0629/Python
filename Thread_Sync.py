import threading
import time

ThreadLock = threading.Lock()
Threads = []
exitFlag = 0

#	==========================Function==========================

class Thread_Sync(threading.Thread):		#继承父类threading.Thread
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self):							#把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
		print("Starting {0}".format(self.name))
		try:
			ThreadLock.acquire()
			Print_Time(self.name,self.counter,5)
		except Exception as ex:
			print("Error: {0}".format(ex))
		finally:
			ThreadLock.release()
		
		print("Exiting {0}".format(self.name))
	
def Print_Time(thread_name, delay, counter):
    while counter:
        if exitFlag:
            (threading.Thread).exit()
        time.sleep(delay)
        print("{0}: {1}".format(thread_name, time.ctime(time.time())))
        counter -= 1

#	==========================main==========================

try:

	# 创建新线程
	for i in range(1,3):
		thread = Thread_Sync(i, "Thread-%s" % i,i)
		Threads.append(thread)
		thread.start()
		
	# 等待所有线程完成
	for t in Threads:
		t.join()
	
except Exception as ex:
	print("Error: {0}".format(ex))

input("Press Enter to continue...\n")