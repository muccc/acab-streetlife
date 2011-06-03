import lib_sl
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
    c = random.randint(0,7)

    col = random.randint(0,5)
    lib_sl.send(c,r,cs[0][col],cs[1][col],cs[2][col],500)

    time.sleep(0.1)

