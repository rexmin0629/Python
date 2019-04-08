import asyncio
import thread
import threading
import time

#	==========================Function==========================	

def consumer():
	r = ''
	while True:
		n = yield r
		if not n:
			return
		print('[CONSUMER] Consuming {0}...'.format(n))
		r = '200 OK'

def produce(c):
	c.send(None)
	n = 0
	while n < 5:
		n = n + 1
		print('[PRODUCER] Producing {0}...'.format(n))
		r = c.send(n)
		print('[PRODUCER] Consumer return: {0}'.format(r))
	c.close()

@asyncio.coroutine
def hello_1():
	count = 0
	
	#while count < 10:
	#	print("Hello {0} times".format(count))
	#	count += 1
	#	r = yield from asyncio.sleep(1)
		
	print("Hello world!")
	# 异步调用asyncio.sleep(1):
	r = yield from asyncio.sleep(1)
	print("Hello again!  r:{0}".format(r))
	
@asyncio.coroutine
def hello_2():
	print('Hello world! {0}'.format(threading.currentThread()))
	yield from asyncio.sleep(1)
	print('Hello again! {0}'.format(threading.currentThread()))
	
@asyncio.coroutine
def web_get(host):
	print("Web host :{0}".format(host))
	connect = asyncio.open_connection(host,80)
	reader , writer = yield from connect
	header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
	writer.write(header.encode('utf-8'))
	yield from writer.drain()
	while True:
		line = yield from reader.readline()
		if line == b'\r\n':
			break
		print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
	# Ignore the body, close the socket
	writer.close()
	
#	==========================main==========================
try:
	
	model = int(input("Enter Test Function:"))
	
	if model == 1:
		#	非同步
		c = consumer()
		produce(c)
	
	elif model == 2:
		# 获取EventLoop:
		loop = asyncio.get_event_loop()
		# 执行coroutine
		loop.run_until_complete(hello_1())
		loop.close()
		
	elif model == 3:
		# 获取EventLoop:
		loop = asyncio.get_event_loop()
		# 执行coroutine
		tasks = [hello_2(), hello_2()]
		loop.run_until_complete(asyncio.wait(tasks))
		loop.close()
	
	elif model == 4:
		# 获取EventLoop:
		loop = asyncio.get_event_loop()
		# 执行coroutine
		tasks = [web_get(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
		loop.run_until_complete(asyncio.wait(tasks))
		loop.close()
	
except Exception as ex:
	print("Error: {0}".format(ex))

#input("Press Enter to continue...\n")