import lib_sl
import random
import time

cs =	[
	    [255,255,000,000,000,255],
	    [000,255,255,255,000,000],
	    [000,000,000,255,255,255],
	]

def draw(x,y,r,g,b,t):
	if (x < 0 or x > 7):
	    return
	lib_sl.send(x,y,r,g,b,t)

def pix(x,y,c):
	draw(x-1,y,0,0,0,600)
	draw(x+1,y,0,0,0,600)
	draw(x,y,cs[0][c],cs[1][c],cs[2][c],300)

def col(c):
    if c > 5:
	return c - 6
    return c
    
c = 0

while 1:
    
    for x in range(0,7):
	pix(x,0,col(c))
	pix(7-x,1,col(c+1))
	pix(x,2,col(c+2))
	pix(7-x,3,col(c+3))
	pix(x,4,col(c+4))
	pix(7-x,5,col(c+5))

	time.sleep(0.3)

    c = c + 2
    if (c > 5):
	c = 0

    for x in range(0,7):
	pix(7-x,0,col(c))
	pix(x,1,col(c+1))
	pix(7-x,2,col(c+2))
	pix(x,3,col(c+3))
	pix(7-x,4,col(c+4))
	pix(x,5,col(c+5))

	time.sleep(0.3)

    c = c + 1
    if (c > 5):
	c = 0
