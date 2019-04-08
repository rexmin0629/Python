import socket
from time import gmtime, strftime

#	==========================Function==========================

#	==========================main==========================
try:

	if __name__=='__main__':
		
		server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		server_socket.bind(('127.0.0.1', 4660))
		
		print('Bind UDP on 4660...')
		
		while True:
			# 接收数据:
			data, addr = server_socket.recvfrom(1024)
			print('[Received:{0}][data:{1}].'.format(addr,data.decode('utf-8')))
			server_socket.sendto(b'Hello, %s!' % data, addr)
		
except Exception as ex:
	print("Error: {0}".format(ex))
