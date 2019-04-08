import socket
from time import gmtime, strftime

#	==========================Function==========================

#	==========================main==========================
try:

	if __name__=='__main__':
		
		client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		
		for data in [b'Michael', b'Tracy', b'Sarah']:
			# 发送数据:
			client_socket.sendto(data, ('127.0.0.1', 4660))
			# 接收数据:
			print(client_socket.recv(1024).decode('utf-8'))
			
		client_socket.close()
		
except Exception as ex:
	print("Error: {0}".format(ex))