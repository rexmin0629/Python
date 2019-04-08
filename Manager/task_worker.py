from multiprocessing.managers import BaseManager
import queue
import time
import sys


#	==========================Function==========================

class Queue_Manager(BaseManager):
	pass

#	==========================main==========================
try:
	
	if __name__=='__main__':
		
		#	註冊網路上之Queue(因為是從網路上註冊的 所以只需要填入名字)
		Queue_Manager.register("get_task_Queue")
		Queue_Manager.register("get_result_Queue")
		
		#	綁定位置與Prot 並設置驗證碼
		manager = Queue_Manager(address=('127.0.0.1',4660), authkey=b'TTTTTTT')
		
		#	連線
		manager.connect()
		
		#	建立訪問Queue之物件
		task = manager.get_task_Queue()
		result = manager.get_result_Queue()
		
		#	取得task Queue之內容 並回送
		while True:
			t = ""
			try:
				t = task.get(timeout = 2)
				print("Run task : {0}".format(t))
				str_back = "{0}_back".format(t)
				result.put(str_back)
				time.sleep(1)
			except:
				if t == "" or t == None:
					print('task is None')
					break
		
		print('worker exit.')
		
except Exception as ex:
	print("Error: {0}".format(ex))
