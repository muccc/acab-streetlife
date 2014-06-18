#!/usr/bin/env python
# -*- coding: utf-8 -*-

import acabsl
import time

acabsl.update()

def set_all(r,g,b):
    for w in range(acabsl.NOOFWALLS):
        for x in range(acabsl.WALLSIZEX):
            for y in range(acabsl.WALLSIZEY):
                acabsl.send(x,y,r,g,b,0,w)
    acabsl.update()

while 1:
    set_all(0,0,255)
    time.sleep(4/144.)
    set_all(0,0,0)
    time.sleep(12/144.)
    set_all(0,0,255)
    time.sleep(4/144.)
    set_all(0,0,0)
    time.sleep(100/144.)
