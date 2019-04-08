from tkinter import *
import tkinter.messagebox as messagebox

#	==========================Function==========================

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		
		#self.helloLabel = Label(self, text='Hello, world!')
		#self.helloLabel.pack()
		
		self.nameInput = Entry(self)
		self.nameInput.grid(row=0,column=0)
		#self.nameInput.pack()
		self.alertButton = Button(self, text='Hello', command=self.hello)
		self.alertButton.grid(row=1,column=0)
		#self.alertButton.pack()
		self.quitButton = Button(self, text='Quit', command=self.quit)
		self.quitButton.grid(row=1,column=1)
		#self.quitButton.pack()
	
	def hello(self):
		name = self.nameInput.get() or 'world'
		messagebox.showinfo('Message', 'Hello, %s' % name)

#	==========================main==========================

try:

	app = Application()
	# 设置窗口标题:
	app.master.title('Hello World')
	# 主消息循环:
	app.mainloop()

except Exception as ex:
	print("Error: {0}".format(ex))
	
