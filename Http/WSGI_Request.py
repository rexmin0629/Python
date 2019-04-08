
#	==========================Function==========================	

def Body(environ):
	body = "<h1>Hello, {0}!</h1>".format((environ['PATH_INFO'][1:] or 'web'))
	return body
	
def application(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/html')])
	body = Body(environ)
	return [body.encode('utf-8')]

#	==========================main==========================
#try:
	
	
#except Exception as ex:
#	print("Error: {0}".format(ex))