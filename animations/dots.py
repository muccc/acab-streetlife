import random,time,acabsl

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


t=2.0

acabsl.update()

while 1:
 start=random.choice(acabsl.matrix())
 c=rcolor()
 acabsl.send(start[0],start[1],c[0],c[1],c[2],t)
 acabsl.update()
 n=[]
 for i in acabsl.matrix():
  if (int(i[0]) == int(start[0]) and (int(i[1]) == int(start[1])+1 or int(i[1]) == int(start[1])-1)) or (int(i[1]) == int(start[1]) and (int(i[0]) == int(start[0])+1 or int(i[0]) ==int( start[0])-1)):
   n.append(i)
 time.sleep(float(t/4))

 c=dimcolor(c)
 for p in n:
  acabsl.send(p[0],p[1],c[0],c[1],c[2],t) 
 acabsl.update()

 m=[]
 for i in acabsl.matrix():
  if (int(i[0]) == int(start[0])+1 or int(i[0]) == int(start[0])-1) and  (int(i[1]) == int(start[1])+1 or int(i[1]) == int(start[1])-1):
   m.append(i)
 time.sleep(float(t/4))
 c=dimcolor(c)
 for p in m:
  acabsl.send(p[0],p[1],c[0],c[1],c[2],t)
 acabsl.update()

 o=[]
 for i in acabsl.matrix():
  if ((int(i[0]) == int(start[0])+2 or int(i[0]) == int(start[0])-2) and  int(i[1]) == int(start[1])) or ((int(i[1]) == int(start[1])-2 or int(i[1]) == int(start[1])+2) and int(i[0]) == int(start[0])):
   o.append(i)
 time.sleep(float(t/4))
 c=dimcolor(c)
 for p in o:
  acabsl.send(p[0],p[1],c[0],c[1],c[2],t)
 acabsl.update()
 time.sleep(float(t/4))

