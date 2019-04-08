import threading
import time
import socket
import os
from time import gmtime, strftime

exitFlag = 0

#	==========================Function==========================

class Thread_Send(threading.Thread):
	def __init__(self, mySocket:socket):
		threading.Thread.__init__(self)
		self.mySocket = mySocket
		
	def run(self):
		global exitFlag
		try:
			count = 0
			str_data = "mother fuck~~"
			
			while True:
				if exitFlag:
					break
				
				if count > 10:
					exitFlag = 1
					str_data = "exit"	#	通知Server斷線
					
				print("[{0}][Send:{1}]\n".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()),str_data))
				self.mySocket.send(str_data.encode('utf-8'))
				count +=1
				time.sleep(1)
			
		except Exception as ex:
			print("Error: {0}".format(ex))
	
	
class Thread_Recev(threading.Thread):
	def __init__(self, mySocket:socket):
		threading.Thread.__init__(self)
		self.mySocket = mySocket
		
	def run(self):
		global exitFlag
		try:
			
			while True:
				if exitFlag:
					break
				
				d = self.mySocket.recv(1024).decode('utf-8')
				print("[{0}][Recev:{1}]\n".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()),d))
				time.sleep(1)
			
		except Exception as ex:
			print("Error: {0}".format(ex))

#	==========================main==========================
try:

	if __name__=='__main__':
		
		#	建立與Server連線之Socket
		client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		client_socket.connect(('127.0.0.1', 4660))
		
		#	建立Client之發送訊息Thread
		th_Send = Thread_Send(client_socket)
		th_Send.start()
		
		#	建立Client之接收訊息Thread
		th_Receive = Thread_Recev(client_socket)
		th_Receive.start()
		
		th_Send.join()
		th_Receive.join()
		
		client_socket.close()

except Exception as ex:
	print("Error: {0}".format(ex))