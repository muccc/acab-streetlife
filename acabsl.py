import socket
import sys, getopt

UDPHOST="localhost"
UDPPORT=6002

WALLSIZEX=16
WALLSIZEY=16
NOOFWALLS=1
WALL=0
# Throws an error if an option is not recognized
# TODO: allow unknown options


#opts, args = getopt.getopt(sys.argv[1:],"",["host=","port=","wall=","wallsizex=","wallsizey="])

filtered = [e for e in sys.argv[1:] if e.split('=')[0] in ["--host", "--port", "--wall", "--wallsizex", "--wallsizey"]]
print(filtered)
#filtered = [e for e in sys.argv[1:] if '=' in e]

opts, args = getopt.getopt(filtered,"",["host=","port=","wall=","wallsizex=","wallsizey="])
#print opts, args
for opt, arg in opts:
    if opt == '--wall':
        WALL = int(arg)
    if opt == '--port':
        UDPPORT = int(arg)
    if opt == '--host':
        UDPHOST = arg
    if opt == '--wallsizex':
        WALLSIZEX = int(arg)
    if opt == '--wallsizey':
        WALLSIZEY = int(arg)

maxx = WALLSIZEX*NOOFWALLS
maxy = WALLSIZEY

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def set_target(host, port):
    global UDPHOST
    global UDPPORT
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
  msg = bytes([x,y,ord('C'),r,g,b,ms>>8,ms&0xFF])
  #print(list(msg))
  sock.sendto(msg, (UDPHOST, UDPPORT))

def update(buffered = True):
  if buffered:
    msg = bytes([1,0,ord('U'),0,0,0,0,0])
  else:
    msg = bytes([0,0,ord('U'),0,0,0,0,0])

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

def set_all(r,g,b):
    for w in range(NOOFWALLS):
        for x in range(WALLSIZEX):
            for y in range(WALLSIZEY):
                send(x,y,r,g,b,0,w)
    update()

