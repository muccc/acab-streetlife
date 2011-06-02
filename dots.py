import random,time,lib_sl

def rcolor():
 color=[]
 color.append(int(random.random()*255))
 color.append(int(random.random()*255))
 color.append(int(random.random()*255))
 return color

def dimcolor(color):
 nucolor=[]
 for i in color:
  i = i-25
  if i < 0:
   i=0
  nucolor.append(i)
 return nucolor


t=3.0

while 1:
 start=random.choice(lib_sl.matrix())
 c=rcolor()
 lib_sl.send(start[0],start[1],c[0],c[1],c[2],t)
 n=[]
 for i in lib_sl.matrix():
  if (int(i[0]) == int(start[0]) and (int(i[1]) == int(start[1])+1 or int(i[1]) == int(start[1])-1)) or (int(i[1]) == int(start[1]) and (int(i[0]) == int(start[0])+1 or int(i[0]) ==int( start[0])-1)):
   n.append(i)
 time.sleep(float(t/4))

 c=dimcolor(c)
 for p in n:
  lib_sl.send(p[0],p[1],c[0],c[1],c[2],t) 

 m=[]
 for i in lib_sl.matrix():
  if (int(i[0]) == int(start[0])+1 or int(i[0]) == int(start[0])-1) and  (int(i[1]) == int(start[1])+1 or int(i[1]) == int(start[1])-1):
   m.append(i)
 time.sleep(float(t/4))
 c=dimcolor(c)
 for p in m:
  lib_sl.send(p[0],p[1],c[0],c[1],c[2],t)

 o=[]
 for i in lib_sl.matrix():
  if ((int(i[0]) == int(start[0])+2 or int(i[0]) == int(start[0])-2) and  int(i[1]) == int(start[1])) or ((int(i[1]) == int(start[1])-2 or int(i[1]) == int(start[1])+2) and int(i[0]) == int(start[0])):
   o.append(i)
 time.sleep(float(t/4))
 c=dimcolor(c)
 for p in o:
  lib_sl.send(p[0],p[1],c[0],c[1],c[2],t)
 time.sleep(float(t/4))

