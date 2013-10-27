import urllib2
import socket
import sys, getopt

UDPHOST="localhost"
UDPPORT=6002

WALLSIZEX=6
WALLSIZEY=8
NOOFWALLS=1
WALL=0

maxx = WALLSIZEX*NOOFWALLS
maxy = WALLSIZEY

# Throws an error if an option is not recognized
# TODO: allow unknown options

opts, args = getopt.getopt(sys.argv[1:],"",["host=","port=","wall="])
#print opts, args
for opt, arg in opts:
    if opt == '--wall':
        WALL = int(arg)
    if opt == '--port':
        UDPPORT = int(arg)
    if opt == '--host':
        UDPHOST = arg

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def set_target(host, port):
    UDPHOST = host
    UDPPORT = port

def send(x,y,r,g,b,t=0,w=WALL):
  w = min(max(0,int(w)),NOOFWALLS)
  x = min(max(0,int(x)),maxx)
  y = min(max(0,int(y)),maxy)

  r = min(max(0,int(r)),255)
  g = min(max(0,int(g)),255)
  b = min(max(0,int(b)),255)
  ms = min(max(0, int(t * 1000)),65535)

  # recalculate x and y based on input x,y and wall no w
  x=((w*WALLSIZEX)+x)
  msg = "%c%cC%c%c%c%c%c"%(x,y,r,g,b,ms>>8,ms&0xFF)
  #print list(msg)
  sock.sendto(msg, (UDPHOST, UDPPORT))

def update(buffered = True):
  if buffered:
    msg = "%c%cU%c%c%c%c%c"%(1,0,0,0,0,0,0)
  else:
    msg = "%c%cU%c%c%c%c%c"%(0,0,0,0,0,0,0) 

  sock.sendto(msg, (UDPHOST, UDPPORT))
    
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
