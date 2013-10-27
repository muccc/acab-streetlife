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

while 1:
    set_all(255,255,255)
    time.sleep(t)



