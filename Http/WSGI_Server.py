from wsgiref.simple_server import make_server
from WSGI_Request import application

#	==========================Function==========================	

def Create_Server():
	# 创建一个服务器，IP地址为空，端口是4660，处理函数是application:
	httpd = make_server('127.0.0.1', 4660, application)
	print('Serving HTTP on port 4660...')
	# 开始监听HTTP请求:
	httpd.serve_forever()

#	==========================main==========================
try:
	
	Create_Server()
	
except Exception as ex:
	print("Error: {0}".format(ex))
	
input("Press Enter to continue...\n")
