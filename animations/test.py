#!/usr/bin/env python
# -*- coding: utf-8 -*-

import acabsl
import time
t = 1

acabsl.update()

def set_all(r,g,b):
    for w in range(acabsl.NOOFWALLS):
        for x in range(acabsl.WALLSIZEX):
            for y in range(acabsl.WALLSIZEY):
                acabsl.send(x,y,r,g,b,0,w)
                acabsl.update()
                time.sleep(4)
                #input("Press Enter to continue... %d %d"%(x,y) )

while 1:
    set_all(0,0,255)
    time.sleep(t)



