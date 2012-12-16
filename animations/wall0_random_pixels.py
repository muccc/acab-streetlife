import acabsl
import random
import time

WALL=0
NOOFPIXELSX=8
NOOFPIXELSY=6

cs =	[
	    [255,255,000,000,000,255],
	    [000,255,255,255,000,000],
	    [000,000,000,255,255,255],
	]

def rcolor():
    c = random.randint(0,NOOFPIXELSY)
    
l = 1
s = 0.1

while 1:
    r = random.randint(0,NOOFPIXELSY-1)
    c = random.randint(0,NOOFPIXELSX-1)
    col = random.randint(0,NOOFPIXELSY-1)
    acabsl.send(WALL,c,r,cs[0][col],cs[1][col],cs[2][col],0.5)
    time.sleep(0.1)

