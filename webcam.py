import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.0.22', 5002))

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

