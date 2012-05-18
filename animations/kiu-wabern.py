import acabsl
import random
import time

cs =	[
	    [255,255,000,000,000,255],
	    [000,255,255,255,000,000],
	    [000,000,000,255,255,255],
	]
dir =	[
	    [01,-1,00,00],
	    [00,00,01,-1]
	]

x1=2
y1=3

x2=14
y2=3

def draws(x,y,c,t,f):
    if (x < 0 or x > 15):
	return
    if (y < 0 or y > 5):
	return
    c1 = max(0,cs[0][c] - f)
    c2 = max(0,cs[1][c] - f)
    c3 = max(0,cs[2][c] - f)
    
    acabsl.send(x,y,c1,c2,c3,t)
    
acabsl.update()
def draw(x,y,c):

#    draws(x-1,y-1,c,300,200)
    draws(x-1,y,c,0.3,100)
#    draws(x-1,y+1,c,300,200)

    draws(x,y-1,c,0.3,100)
    draws(x,y,c,1,0)
    draws(x,y+1,c,0.3,100)

#   draws(x+1,y-1,c,300,200)
    draws(x+1,y,c,0.3,100)
#    draws(x+1,y+1,c,300,200)

while 1:

    x1 = max(1,min(14,x1 + dir[0][random.randint(0,3)]))
    y1 = max(1,min(4,y1 + dir[1][random.randint(0,3)]))

    x2 = max(1,min(14,x2 + dir[0][random.randint(0,3)]))
    y2 = max(1,min(4,y2 + dir[1][random.randint(0,3)]))
    
    col1 = random.randint(0,5)
    col2 = random.randint(0,5)

    draw(x1,y1,col1) 
    draw(x2,y2,col2) 

    acabsl.update()
    time.sleep(0.1)

