#!/usr/bin/env python
# -*- coding: utf-8 -*-

import acabsl
import acabsl2
import time
import random
t = 0.1

acabsl.update()
acabsl2.update()

def set_all(r,g,b):
    for w in range(acabsl.NOOFWALLS):
        for x in range(acabsl.WALLSIZEX):
            for y in range(acabsl.WALLSIZEY):
                acabsl.send(x,y,r,g,b,0,w)
                acabsl2.send(x,y,r,g,b,0,w)
    acabsl.update()
    acabsl2.update()

while 1:
    r = random.randrange(0, 255, 1)
    g = random.randrange(0, 255, 1)
    b = random.randrange(0, 255, 1)
    set_all(r,g,b)
    time.sleep(t)



