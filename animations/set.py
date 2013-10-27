#!/usr/bin/python

import acabsl
import time
import sys
t = 1

acabsl.update()

def set_all(r,g,b):
    for w in range(acabsl.NOOFWALLS):
        for x in range(acabsl.WALLSIZEX):
            for y in range(acabsl.WALLSIZEY):
                acabsl.send(x,y,r,g,b,0,w)
    acabsl.update()

r = int(sys.argv[1])
g = int(sys.argv[2])
b = int(sys.argv[3])

while 1:
    set_all(r,g,b)
    time.sleep(t)



