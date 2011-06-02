import urllib2
import time
import socket
import random

matrix = []

def gen_matrix():
    y = 0
    x = 0
    while ( y <= 5 ):
        while (x <=7 ):
            p =  str(x) + str(y)
            matrix.append(p)
            x = x + 1
            
        y = y + 1
        x = 0

def rcolor():
  return int(random.random()*255)

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

def socksend(payload, IP="127.1", PORT=5005):
  sock.sendto(payload, (IP, PORT))
        
gen_matrix()

#IP="127.1"
#PORT=5005

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )




while "True":
  chosen = []
  i=0
  while ( i < 10):
   chosen.append(random.choice(matrix))
   i=i+1
  r=rcolor()
  b=rcolor()
  g=rcolor()
  t=2+(random.random()*5)
  print chosen
  print r, b, g, t
  for p in chosen:
     m = "/%i/%i/%i/%i/%i/%i" % (int(p[0]), int(p[1]), r, b, g, t*1000)
     f = urllib2.urlopen("http://127.1:8080"+m)
     time.sleep(t/10) 
  time.sleep(.5)


