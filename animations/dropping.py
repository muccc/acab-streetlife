from acabsl import send
from acabsl import update
import acabsl

import colorsys
import random
import time

tick = 0.3

def setcol(col, r, g, b, rtime):
    for i in range(0,acabsl.WALLSIZEY):
        send(col,i,r,g,b,rtime);
    	update()
	time.sleep(tick)
h = 0
col = 0
update()
while 1:
    h += 0.08
    h = h % 1.

    for col in range(0,acabsl.WALLSIZEX):
    	r,g,b = colorsys.hsv_to_rgb(h, 1., 1.)
    	setcol(col, r*255, g*255, b*255, tick*3)   
	col += 1 

