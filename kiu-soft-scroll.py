import lib_sl
import random
import time

cs =	[
	    [255,255,000,000,000,255],
	    [000,255,255,255,000,000],
	    [000,000,000,255,255,255],
	]

def draw(x,y,r,g,b,t):
	if (x < 0 or x > 15):
	    return
	lib_sl.send(x,y,r,g,b,t)

def pix(x,y,c):
	draw(x-1,y,0,0,0,0.6)
	draw(x+1,y,0,0,0,0.6)
	draw(x,y,cs[0][c],cs[1][c],cs[2][c],0.3)

def col(c):
    if c > 5:
	return c - 6
    return c
    
c = 0

lib_sl.update()
while 1:
    
    for x in range(0,15):
	pix(x,0,col(c))
	pix(15-x,1,col(c+1))
	pix(x,2,col(c+2))
	pix(15-x,3,col(c+3))
	pix(x,4,col(c+4))
	pix(15-x,5,col(c+5))
	lib_sl.update()

	time.sleep(0.3)

    c = c + 2
    if (c > 5):
	c = 0

    for x in range(0,15):
	pix(15-x,0,col(c))
	pix(x,1,col(c+1))
	pix(15-x,2,col(c+2))
	pix(x,3,col(c+3))
	pix(15-x,4,col(c+4))
	pix(x,5,col(c+5))
	lib_sl.update()

	time.sleep(0.3)

    c = c + 1
    if (c > 5):
	c = 0
