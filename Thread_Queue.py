import queue
import threading
import time

ThreadLock = threading.Lock()
Threads = []
exitFlag = 0
nameList = ["One", "Two", "Three", "Four", "Five"]
workQueue = queue.Queue(10)

#	==========================Function==========================

class Thread_Queue(threading.Thread):
	def __init__(self,threadID,thread_name,myqueue):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = thread_name
		self.queue = myqueue
	def run(self):
		print("Starting {0}".format(self.name))
		Process_Queue(self.name,self.queue)
		print("Exiting {0}".format(self.name))

def Process_Queue(thread_name,myqueue):
	while not exitFlag:
		ThreadLock.acquire()
		try:
			if not myqueue.empty():
				data = myqueue.get()
				print("Thread: {0} , Queue data : {1}".format(thread_name,data))
		except:
			print("Error: {0}".format(ex))
		finally:
			ThreadLock.release()
		
		time.sleep(1)

#	==========================main==========================

try:

	# 创建新线程 Thread_Queue
	for i in range(1,4):
		thread = Thread_Queue(i, "Thread-%s" % i,workQueue)
		Threads.append(thread)
		thread.start()
	
	# Add data to Queue
	ThreadLock.acquire()
	for str in nameList:
		workQueue.put(str)
	ThreadLock.release()
		
	while not workQueue.empty():
		pass
		
	# 通知线程是时候退出
	exitFlag = 1

	# 等待所有线程完成
	for t in Threads:
		t.join()

except Exception as ex:
	print("Error: {0}".format(ex))

input("Press Enter to continue...\n")