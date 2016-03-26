#! /bin/python2

import socket
import time
import Tkinter
import threading
from PIL import ImageTk

CONNECT_IP = '127.0.0.1'
CONNECT_PORT = 5000
IMAGE_PATH = '/tmp/webcam.jpg'


class ReceiverThread(threading.Thread):

  def __init__(self, mt):
    super(ReceiverThread, self).__init__()
    self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__s.connect((CONNECT_IP, CONNECT_PORT))
    self.__mt = mt
    self.__close = False

  def run(self):
    while self.__close == False:
      t = self.__s.recv(2048)
      i = t.find(";")
      b = t[i+1:]
      c = int(t[:i])
      b_len = len(b)

      while b_len < c:
        t = self.__s.recv(min(2048, c-b_len))
        if t == '':
          raise Exception("Connection closed! :(")
        b += t
        b_len += len(t)
        print "recvd %d/%d bytes" % (b_len, c)

      with open('/tmp/webcam.jpg', 'wb') as f: f.write(b)

      try:
        self.__mt.updateImage()
      except RuntimeError:
        pass

  def close(self):
    self.__close = True


class MainThread(threading.Thread):

  def __init__(self):
    super(MainThread, self).__init__()

  def run(self):
    root = Tkinter.Tk()
    root.title('Webcam')
    startframe = Tkinter.Frame(root)
    self.canvas = Tkinter.Canvas(startframe, width=1280, height=720)
    startframe.pack()
    self.canvas.pack()

    im = ImageTk.PhotoImage(file=IMAGE_PATH)
    self.canvas.img = im
    self.canvasImg = self.canvas.create_image((0,0), image=im, anchor='nw')

    root.mainloop()

  def updateImage(self):
    img2 = ImageTk.PhotoImage(file=IMAGE_PATH)
    self.canvas.itemconfig(self.canvasImg, image=img2)
    self.canvas.img = img2

m = MainThread()
rt = ReceiverThread(m)
rt.start()

try:
  m.run()
except KeyboardInterrupt:
  rt.close()



