import socket
import sys
import os
import threading
import subprocess

class VideoStream:

  def __init__(self):
    self.__frame = ""

  def setFrame(self, f):
    self.__frame = f

  @property
  def frame(self):
    return self.__frame

class VideoStreamWorker(threading.Thread):

  def __init__(self, video):
    super(VideoStreamWorker, self).__init__()
    self.video = video

  def run(self):
    while 1:
      PIPE = subprocess.PIPE
      p = subprocess.Popen("fswebcam -p YUYV -d /dev/video0 -i 0 -", shell=True, stderr=PIPE, stdout=PIPE)
      (out, err) = p.communicate()
      self.video.setFrame(out)

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
      if chunk == '\n': break

class WorkThread(threading.Thread):

  def __init__(self, sock, video):
    super(WorkThread, self).__init__()
    self.__s = PictureSocket(sock)
    self.__video = video

  def run(self):
    while 1:
      self.__s.recv()
      img = self.__video.frame
      self.__s.send("%d;%s"%(len(img), img))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5002))
s.listen(5)

v = VideoStream()
VideoStreamWorker(v).start()

while 1:
  print "listening..."
  (cs, ad) = s.accept()
  print "Connected with %s" % str(ad)
  wt = WorkThread(cs, v)
  wt.start()
