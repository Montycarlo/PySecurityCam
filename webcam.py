#! /bin/python2

import socket
import time

import Tkinter

CONNECT_IP = '127.0.0.1'
CONNECT_PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((CONNECT_IP, CONNECT_PORT))


# open a SPIDER image and convert to byteformat
#im = Image.open('slice001.hrs').convert2byte()

root = Tkinter.Tk()
# A root window for displaying objects
# Convert the Image object into a TkPhoto object

while 1:
	s.send("\n")

	t = s.recv(2048)
	i = t.find(";")

	b = t[i+1:]
	c = int(t[:i])
	b_len = len(b)
	while b_len < c:
		t = s.recv(min(2048, c-b_len))
		if t == '':
			raise Exception("Connection closed! :(")
		b += t
		b_len += len(t)
		print "recvd %d/%d bytes" % (b_len, c)

	print "Fin recv img"
	f = open('/tmp/webcam.jpg', 'wb')
	f.write(b)
	f.close()

	tkimage = Tkinter.PhotoImage(b)

	Tkinter.Label(root, image=tkimage).pack()
	# Put it in the display window

	root.mainloop() # Start the GUI

