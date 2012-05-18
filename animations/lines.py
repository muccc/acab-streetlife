import random
import lib_sl
import time


def rcolor():
  return int(random.random()*255)

t=5.1
n=0
i=j=0

while 1:
 j=0
 r=rcolor()
 g=rcolor()
 b=rcolor() 
 x=int(random.random()*16)
 while (j < 6):
    y=j
    lib_sl.send(x,y,r,g,b,t)
    j=j+1
    time.sleep(t/(4*t))
 j=0
 time.sleep(t/(4*t))


   


