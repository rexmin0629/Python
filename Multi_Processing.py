from multiprocessing import Process
import os

#	==========================Function==========================

# 子进程要执行的代码
def run_proc(name):
	print("Run child process {0} ({1})...".format(name, os.getpid()))


#	==========================main==========================
try:

	if __name__=='__main__':
		print("Parent process {0}.".format(os.getpid()))
		p = Process(target=run_proc, args=('test',))
		print('Child process will start.')
		p.start()
		p.join()
		print('Child process end.')
		
		
except Exception as ex:
	print("Error: {0}".format(ex))

#input("Press Enter to continue...\n")

