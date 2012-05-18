import acabsl
import random
import time

t=0.2
ft=0.2
target=0
def colord(color_old):
 tc=0
 i=0
 color_nu=[]
 while i < 3:
  color_nu.append(min(255,max(0,color_old[i]+int(random.gauss(target,10)))))
  i=i+1
  tc=tc+1
 return color_nu

scolor=[]
i =0
while i <3:
 scolor.append(int(random.random()*255))
 i=i+1

color_n=scolor

while 1:
 j=0
 while j < 6:
  acabsl.send(i,j,color_n[0],color_n[1],color_n[2],ft)
  color_n=colord(color_n)
  time.sleep(t)
  j=j+1
 i=i+1
 if i >15 :
  i=0
 
