import thread
import time

#	==========================Function==========================

def Print_Time(thread_name,delay):
	count = 0
	while count < 5:
		time.sleep(delay)
		print("thread_name: {0}, count: {1} , show_Time: {2}".format(thread_name,count,time.ctime(time.time())))
		count+=1

#	==========================main==========================

try:

	thread.start_new_thread( Print_Time, ("Thread-1", 1, ) )
	thread.start_new_thread( Print_Time, ("Thread-3", 3, ) )

except Exception as ex:
	print("Error: {0}".format(ex))

input("Press Enter to continue...\n")