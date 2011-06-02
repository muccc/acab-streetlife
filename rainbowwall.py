import lib_sl
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
#  if tc > 500:
#   tc=0
#   target=int(random.randint(-30,+30)
# for i in color_nu:
#  if i < 0:
#   i = 0
#  if i > 255:
#   i = 255
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
  print (i,j,color_n[0],color_n[1],color_n[2],ft)
  lib_sl.send(i,j,color_n[0],color_n[1],color_n[2],ft)
  color_n=colord(color_n)
  time.sleep(t)
#  lib_sl.send(i,j,colord(scolor)[0],colord(scolor)[1],colord(scolor)[2],t)
  j=j+1
# time.sleep(t) 
 i=i+1
 if i >7 :
  i=0
 
