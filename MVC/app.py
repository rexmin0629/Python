from flask import Flask
from flask import request
from flask import render_template

app =Flask(__name__)

#	==========================Function==========================

@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
	return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
	username = request.form['username']
	password = request.form['password']
	if username=='admin' and password=='password':
		return render_template('signin_OK.html', username=username)
	return render_template('form.html', message='Bad username or password', username=username)

#	==========================main==========================

try:
	if __name__ == '__main__':
		app.run()
	
except Exception as ex:
	print("Error: {0}".format(ex))
