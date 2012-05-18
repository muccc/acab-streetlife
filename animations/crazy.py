import random,time,acabsl

def rcolor():
  color=[]
  color.append(int(random.random()*255))
  color.append(int(random.random()*255))
  color.append(int(random.random()*255))
  return color

t=0.2

while 1:
 start=random.choice(acabsl.matrix())
 c=rcolor()
 acabsl.send(start[0],start[1],c[0],c[1],c[2],t)
 time.sleep(t)
