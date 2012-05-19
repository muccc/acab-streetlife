import random, time, acabsl

t = 1

def rcolor():
    color=[]
    color.append(int(random.random()*255))
    color.append(int(random.random()*255))
    color.append(int(random.random()*255))
    return color


while 1:
    offset = random.choice([0,1,2])
    c=rcolor()
    acabsl.send(0,offset+1,c[0],c[1],c[2],t)
    acabsl.send(0,offset+2,c[0],c[1],c[2],t)
    acabsl.send(0,offset+3,c[0],c[1],c[2],t)
    acabsl.send(1,offset+2,c[0],c[1],c[2],t)

    for i in range(4,16):
        acabsl.send(i,offset+2, c[0],c[1],c[2],t)
        time.sleep(0.2)
        acabsl.send(i,offset+2, 0,0,0,t)
    
    acabsl.send(0,offset+1,0,0,0,t)
    acabsl.send(0,offset+2,0,0,0,t)
    acabsl.send(0,offset+3,0,0,0,t)
    acabsl.send(1,offset+2,0,0,0,t)