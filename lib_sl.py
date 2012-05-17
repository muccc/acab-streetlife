import urllib2
import socket

HOST="127.1"
PORT=8080

UDPHOST="127.0.0.1"
UDPPORT=5005
SIMULATORPORT=5006
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(x,y,r,g,b,t=0):
  x=int(x)
  y=int(y)
  r=int(r)
  g=int(g)
  b=int(b)
  ms = int(t * 1000)
  msg = "%c%cC%c%c%c%c%c"%(x,y,r,g,b,ms>>8,ms&0xFF)
  sock.sendto(msg, (UDPHOST, UDPPORT))
  sock.sendto(msg, (UDPHOST, SIMULATORPORT))

def update(buffered = True):
  if buffered:
    msg = "%c%cU%c%c%c%c%c"%(1,0,0,0,0,0,0)
  else:
    msg = "%c%cU%c%c%c%c%c"%(0,0,0,0,0,0,0) 

  sock.sendto(msg, (UDPHOST, UDPPORT))
  sock.sendto(msg, (UDPHOST, SIMULATORPORT))
    
def speedfade(x,y,r,g,b,speed):
  x=int(x)
  y=int(y)
  r=int(r)
  g=int(g)
  b=int(b)
  msg = "%c%cF%c%c%c%c%c"%(x,y,r,g,b,speed>>8,speed&0xFF)
  sock.sendto(msg, (UDPHOST, UDPPORT))
  sock.sendto(msg, (UDPHOST, SIMULATORPORT))

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

update(False)
update(False)
