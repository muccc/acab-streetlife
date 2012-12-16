import urllib2
import socket

HOST="127.1"
PORT=8080

UDPHOST="127.0.0.1"
UDPPORT=5005
SIMULATORPORT=5006

WALLSIZEX=8
WALLSIZEY=6
NOOFWALLS=2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(w,x,y,r,g,b,t=0):
  w=int(w)
  x=int(x)
  y=int(y)
  r=int(r)
  g=int(g)
  b=int(b)
  ms = int(t * 1000)

  # recalculate x and y based on input x,y and wall no w
  x=((w*WALLSIZEX)+x)

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
    
def speedfade(w,x,y,r,g,b,speed):
  w=int(w)
  x=int(x)
  y=int(y)
  r=int(r)
  g=int(g)
  b=int(b)
  
  # recalculate x and y based on input x,y and wall no w
  x=((w*WALLSIZEX)+x)
  
  msg = "%c%cF%c%c%c%c%c"%(x,y,r,g,b,speed>>8,speed&0xFF)
  sock.sendto(msg, (UDPHOST, UDPPORT))
  sock.sendto(msg, (UDPHOST, SIMULATORPORT))

def matrix(targetsize_x=WALLSIZEX,targetsize_y=WALLSIZEY):
  x=0
  y=0
  matrix = []
  while ( y < targetsize_y):
    while ( x < targetsize_x):
      p =  (x,y)
      matrix.append(p)
      x = x + 1

    y = y + 1
    x = 0
  return matrix

update(False)
update(False)
