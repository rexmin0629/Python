from multiprocessing import Process , Queue
import os
import time
import random

#	==========================Function==========================

def Write(queue):
	print("Write Process {0}".format(os.getpid()))
	
	list = ["AAAA","BBBB","CCCC"]
	for i in list:
		print("Put {0} to Queue".format(i))
		queue.put(i)
		time.sleep(1)
	
def Read(queue):
	print("Read Process {0}".format(os.getpid()))
	
	while True:	
		msg = queue.get()
		print("Get {0} from Queue".format(msg))
		time.sleep(1)

#	==========================main==========================

try:

	if __name__ == "__main__":
		q = Queue()
		p_W = Process(target = Write,args=(q,))
		p_R = Process(target = Read,args=(q,))
		
		p_W.start()
		p_R.start()
		
		p_W.join()
		p_R.terminate()

except Exception as ex:
	print("Error: {0}".format(ex))

#input("Press Enter to continue...\n")