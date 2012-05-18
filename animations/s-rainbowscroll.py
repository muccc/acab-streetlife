from acabsl import send
import colorsys
import random
import time

tick = 0.1

def setcol(col, r, g, b, time):
    for i in range(0,6):
    	send(col,i,r,g,b,time);

h = 0
col = 0

while 1:
    h += random.gauss(0.02,0.05)
    h = h % 1.

    col += 1
    col = col % 8

    r,g,b = colorsys.hsv_to_rgb(h, 1., 1.)
    setcol(col, r*255, g*255, b*255, tick*3)

    time.sleep(tick)
    

