from multiprocessing.managers import BaseManager
import queue
import time
import random

#	發送Queue
task_Queue = queue.Queue()

#	接收Queue
result_Queue = queue.Queue()

#	==========================Function==========================

def return_task_queue():
	global task_Queue
	return task_Queue

def return_result_queue():
	global result_Queue
	return result_Queue

class Queue_Manager(BaseManager):
	pass


#	==========================main==========================

try:

	if __name__=='__main__':
		
		#	把兩個Queue註冊到網路上
		Queue_Manager.register("get_task_Queue",callable=return_task_queue)
		Queue_Manager.register("get_result_Queue",callable=return_result_queue)

		#	綁定位置與Prot 並設置驗證碼
		manager = Queue_Manager(address=('127.0.0.1', 4660), authkey=b'TTTTTTT')
	
		#	啟動Queue
		manager.start()
	
		#	建立訪問Queue之物件
		task = manager.get_task_Queue()
		result = manager.get_result_Queue()
		
		#	隨意發送任務
		for i in range(10):
			n = random.randint(0,1000)
			print("put {0} to task_Queue".format(n))
			task.put(n)
			time.sleep(1)
		
		print("Try get results......")
	
		#	接收Queue之結果
		while True:
			r = ""
			try:
				r = result.get(timeout=5)
				print('Result: {0}'.format(r))
				time.sleep(1)
			except:
				if r == "" or r == None:
					print('result is None')
					break
		
		#	關閉
		manager.shutdown()
		print('master exit.')
		
		
except Exception as ex:
	print("Error: {0}".format(ex))