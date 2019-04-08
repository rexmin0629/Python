import threading

local_school = threading.local()
Threads = []

#	==========================Function==========================
'''
# 不用此方式建立Thread是因為此方式以內所建立之物件只會在各自的Thread中可用(*重點在 __init__) , 所以無法存取local_school(此物件是在主執行續建立的)
class Process_Thread(threading.Thread):
	def __init__(self,thread_name,student_name):
		threading.Thread.__init__(self)
		self.name = thread_name
		local_school.student = student_name
	def run(self):
		Show_Name()
	
def Show_Name():
	str = local_school.student
	print("Thread:{0} , Student:{1}".format(threading.current_thread().name,str))
'''

def process_student():
	# 获取当前线程关联的student:
	std = local_school.student
	print("Hello, {0} (in {1})".format(std, threading.current_thread().name))

def process_thread(name):
	# 绑定ThreadLocal的student:
	local_school.student = name
	process_student()
	
#	==========================main==========================
try:

	for i in range(1,4):
		th = threading.Thread(target= process_thread, args=("Rex-{0}".format(i),), name="Thread-{0}".format(i))
		Threads.append(th)
		th.start()
		
	for t in Threads:
		t.join()


except Exception as ex:
	print("Error: {0}".format(ex))

input("Press Enter to continue...\n")