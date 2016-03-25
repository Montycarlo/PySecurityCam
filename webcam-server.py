import socket
import os
import threading
import subprocess

LISTEN_INTERFACE = ''
LISTEN_PORT = 5000
LISTEN_QUEUE_MAX = 5

class VideoStream:
  '''
  A video stream that is used to between threads.
  Call setFrame(f) to set the current frame, and query
  the `VideoStream.frame` property to get the current frame.
  '''

  def __init__(self):
    self.__frame = ""
    self.__new = False;

  def setFrame(self, f):
    self.__frame = f
    self.__new = True;

  @property
  def frame(self):
    return self.__frame

  @property
  def isNew(self): return self.__new
  def flagOld(self): self.__new = False;


class VideoStreamWorker(threading.Thread):
  '''
  Worker thread for getting the latest frame from a source,
  updating the VideoStream object, and re-running the cycle.
  '''

  def __init__(self, video):
    '''
    @param video: VideoStream
    '''
    super(VideoStreamWorker, self).__init__()
    self.video = video
    self.__closed = False;

  def run(self):
    '''
    Constantly query fswebcam for an image, read out the image, and then
    save that image in the VideoStream object.

    Specifying the filename as - causes fswebcam to print the img to stout.
    '''
    while self.__closed == False:
      PIPE = subprocess.PIPE
      p = subprocess.Popen("fswebcam -p YUYV -d /dev/video0 -i 0 -", shell=True, stderr=PIPE, stdout=PIPE)
      (out, err) = p.communicate()
      self.video.setFrame(out)

  def close(self):
    self.__closed = True

class PictureSocket:
  '''
  Socket wrapper for implementation of the Picture communication protocol.
  Sends an image by specifying the image length, followed by a semicolon (;),
  followed by the image string.

  Receive all until the \n character is received.
  '''

  def __init__(self, sock):
    self.__s = sock

  def sendImg(self, img):
    '''
    @param img: String
    '''
    msg = "%d;%s" % (len(img), img)
    t = 0
    MSG_LEN = len(msg)
    while t < MSG_LEN:
      sent = self.__s.send(msg[t:])
      if sent == 0:
        raise Exception("socket broken")
      t += sent

  #def recv(self):
  #  while 1:
  #    chunk = self.__s.recv(2048)
  #    if chunk == '\n': break

class WorkThread(threading.Thread):
  '''
  Controller thread for a given socket. Responsible for the client-server behaviour, where
  the client requests a new image by sending a newline character \n, then the thread responds
  by collecting the latest frame from the VideoStream instance, and sending it back.
  '''

  def __init__(self, sock, video):
    '''
    @param sock: socket.socket
    @param video: VideoStream
    '''
    super(WorkThread, self).__init__()
    self.__s = PictureSocket(sock)
    self.__video = video
    self.__closed = False

  def run(self):
    while self.__closed == False:
      if self.__video.isNew:
        self.__s.sendImg(self.__video.frame)
        self.__video.flagOld()

  def close(self):
    self.__closed = True

def main():
  '''
  Main controlling function. Sets up the server to listen for incomming requests
  on port LISTEN_PORT, initalizes a VideoStream object to hold a video stream,
  starts a thread to collect new frames and finally spawns a worker thread to handle any connections.
  '''
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((LISTEN_INTERFACE, LISTEN_PORT))
  s.listen(LISTEN_QUEUE_MAX)

  v = VideoStream()
  vsw = VideoStreamWorker(v)
  vsw.start()

  wts = []
  try:
    while 1:
      print "listening..."
      (cs, ad) = s.accept()
      print "Connected with %s" % str(ad)
      wt = WorkThread(cs, v)
      wt.start()
      wts.append(wt)
  except KeyboardInterrupt:
    for w in wts: w.close()
    vsw.close()
main()
