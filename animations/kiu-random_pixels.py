import acabsl
import random
import time

cs =	[
	    [255,255,000,000,000,255],
	    [000,255,255,255,000,000],
	    [000,000,000,255,255,255],
	]

def rcolor():
    c = random.randint(0,6)
    
l = 1
s = 0.1

while 1:

    r = random.randint(0,5)
    c = random.randint(0,15)

    col = random.randint(0,5)
    acabsl.send(c,r,cs[0][col],cs[1][col],cs[2][col],0.5)

    time.sleep(0.1)

