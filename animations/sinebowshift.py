#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Alogrithm from http://basecase.org/env/on-rainbows

from acabsl import send
from acabsl import update
import acabsl

import colorsys
import random
import time
import math

tick = 0.2

def setcol(cols, time):
    for x in range(0,acabsl.WALLSIZEX):
        h = cols[x]
        r = math.sin(math.pi * h)
        g = math.sin(math.pi * (h + 1.0/3))
        b = math.sin(math.pi * (h + 2.0/3))
        for y in range(0,acabsl.WALLSIZEY):
            send(x,y,r*r*255,g*g*255,b*b*255,time);
    update()

def rotate(l,n):
    return l[n:] + l[:n]

h = 0
col = 0
cols = []
for i in range(0,acabsl.WALLSIZEX):
    cols.append(0)
update()
while 1:
    h += 0.01
    h = h % 1.

    cols = rotate(cols,-1)
    cols[0] = h 

    setcol(cols, tick*3)

    time.sleep(tick)
    

