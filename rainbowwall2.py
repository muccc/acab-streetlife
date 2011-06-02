import lib_sl
import random
import time

target=0
t=0.2
ft=0.2
tc=0
change=80

def colord(color_old,target):
 i=0
 color_nu=[]
 while i < 3:
  color_nu.append(min(255,max(0,color_old[i]+int(random.gauss(target,10)))))
  i=i+1
 return color_nu

scolor=[]
i =0
while i < 3:
 scolor.append(int(random.random()*255))
 i=i+1

color_n=scolor

while 1:
 j=0
 while j < 6:
  print (i,j,color_n[0],color_n[1],color_n[2],ft)
  lib_sl.send(i,j,color_n[0],color_n[1],color_n[2],ft)
  color_n=colord(color_n,target)
  time.sleep(t)
  tc=tc+1
#  lib_sl.send(i,j,colord(scolor)[0],colord(scolor)[1],colord(scolor)[2],t)
  j=j+1
# time.sleep(t) 
 i=i+1
 if i >7 :
  i=0
 print tc
 print target
 if tc > change:
  target= int(random.randint(-8,+8))
  print "target changed" 
  tc=0
