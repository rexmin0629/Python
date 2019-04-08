import threading
import time
import socket
from time import gmtime, strftime

exitFlag = 0

#	==========================Function==========================

class TcpLink(threading.Thread):
	def __init__(self,sock: socket,addr):
		threading.Thread.__init__(self)
		self.sock=sock
		self.addr=addr
	def run(self):
		try:
			print('Accept new connection from {0}\n'.format(self.addr))
			
			#	Server先回覆Clien Ack
			self.sock.send("[{0}][Ack]".format(self.addr).encode('utf-8'))
			
			#	持續接收此Client資料 , 直到收到'exit'代表Client要求斷線
			while True:
				data = self.sock.recv(1024).decode('utf-8')
				if data == 'exit':
					print("[{0}][{1}][Close]\n".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()),self.addr))
					self.sock.close()
					break
				print("[{0}][{1}][Receive: {2}]\n".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()),self.addr,data))
				self.sock.send("server received you message.".encode('utf-8'))
				time.sleep(1)
		except Exception as ex:
			print("Error: {0}".format(ex))

#	==========================main==========================
try:

	if __name__=='__main__':
		
		#	建立監聽Socket
		listen_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		
		#	監聽之IP & Port
		listen_socket.bind(('127.0.0.1', 4660))
		
		#	監聽Client最大數量
		listen_socket.listen(5)
		print('Waiting for connection...\n')
		
		while True:
			#	Server監聽到一Client連線
			sock, addr = listen_socket.accept()
			
			#	建立此Client之接收Thread
			th_Client = TcpLink(sock,addr)
			th_Client.start()
			
			#while True:
			#	data = sock.recv(1024)
			#	print("[Receive: {0}]".format(data))
			#	sock.send("server received you message.".encode('utf-8'))

except Exception as ex:
	print("Error: {0}".format(ex))
