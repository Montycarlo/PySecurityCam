import socket
import sys
import os
import threading

class PictureSocket:

	def __init__(self, sock):
		self.__s = sock

	def send(self, msg):
		t = 0
		MSG_LEN = len(msg)
		while t < MSG_LEN:
			sent = self.__s.send(msg[t:])
			if sent == 0:
				raise Exception("socket connection broken")
			t += sent

	def recv(self):
		while 1:
			chunk = self.__s.recv(2048)
			if chunk == '\n':
				#raise RuntimeError("socket connection broken")
				break


class WorkThread(threading.Thread):

	def __init__(self, sock):
		self.__s = PictureSocket(sock)

	def start(self):
		while 1:
			self.__s.recv()
			os.system("fswebcam -p YUYV -d /dev/video0 --save /tmp/video.jpg -i 0 -s Brightness=80% -s Sharpness=50%")
			with open('/tmp/video.jpg', 'rb') as f:
				img = f.read()
			self.__s.send("%d;%s"%(len(img), img))
			
			
		

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5002)) # socket.gethostname()
s.listen(5)

while 1:
	print "listening..."
	(cs, ad) = s.accept()
	print "Connected with %s" % str(ad)
	wt = WorkThread(cs)
	wt.start()
	
	
