import lib_sl
import random
import time

target=0
t=0.1
ft=5
tc=0
change=40

def colord(color_old,target):
 i=0
 color_nu=[]
 while i < 3:
  color_nu.append(min(255,max(0,color_old[i]+int(random.gauss(target,10)))))
  i=i+1
 return color_nu

def color_next(r,g,nr,ng):
 color_c=[]
 color_c.append(max(min(10+r-(r-nr)/30+int(random.gauss(0,10)),255),0))
 color_c.append(min(max(min(g-(g-ng)/30+int(random.gauss(0,10)),255),0),int(color_c[0]/2)))
 return color_c

targets=[
[255,0],
[255,80],
[0,0],
]



scolor=[255,0 ,0]
i =0
#while i < 3:
# scolor.append(int(random.random()*255))
# i=i+1

color_n=scolor
n=0
while 1:
 j=0
 while j < 6:
#  print (i,j,color_n[0],color_n[1],color_n[2],ft)
  print color_n
  lib_sl.send(i,j,color_n[0] ,color_n[1],0,ft)
  color_n=color_next(color_n[0],targets[n][0],color_n[1],targets[n][1])
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
  n=(n+1)%3
  tc=0
