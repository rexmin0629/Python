from multiprocessing import Pool
import os, time

#	==========================Function==========================

def Long_time_task(name , time_span):
	print("Run task name:{0} os:{1} span:{2}...".format(name, os.getpid(),time_span))
	time_start = time.time()
	time.sleep(time_span)
	time_end = time.time()
	print('Task %s runs %0.2f seconds.' % (name, (time_end - time_start)))

#	==========================main==========================

try:

	if __name__=='__main__':
		print("Parent process {0}.".format(os.getpid()))
		
		total_process = 4
		p = Pool(total_process)
		for i in range(total_process+1):
			p.apply_async(Long_time_task, args=(i,3,))
		print('Waiting for all subprocesses done...')
		p.close()
		p.join()
		print('All subprocesses done.')
	
except Exception as ex:
	print("Error: {0}".format(ex))

#input("Press Enter to continue...\n")