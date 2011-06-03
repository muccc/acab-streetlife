import urllib2
import acabsl
import socket

HOST="127.1"
PORT=8080
UDPPORT=5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(x,y,r,g,b,t=0):
  message = "/%s/%s/%i/%i/%i/%i" % (x, y, r, g, b, t*1000)
  urllib2.urlopen("http://%s:%i"% (HOST, PORT)+message)
  ms = int(t * 1000)
  msg = "%c%c%c%c%c%c%c"%(x,y,r,g,b,ms>>8,ms&0xFF)
  sock.sendto(msg, (HOST, UDPPORT))

def matrix(targetsize_x=8,targetsize_y=6):
  x=0
  y=0
  matrix = []
  while ( y < targetsize_y):
    while ( x < targetsize_x):
      p =  str(x) + str(y)
      matrix.append(p)
      x = x + 1

    y = y + 1
    x = 0
  return matrix
