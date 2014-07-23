#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acabsl import send
from acabsl import update
import acabsl

import colorsys
import random
import time

tick = 0.1

def setcol(cols, time):
    for x in range(0,acabsl.WALLSIZEX):
        r,g,b = colorsys.hsv_to_rgb(cols[x], 1., 1.)
        for y in range(0,acabsl.WALLSIZEY):
            send(x,y,r*255,g*255,b*255,time);
    update()

def shift(l,n):
    return l[n:] + l[:n]

h = 0
cols = []
for i in range(0,acabsl.WALLSIZEX):
    cols.append(0)
update()
while 1:
    h += random.gauss(0.02,0.05)
    h = h % 1.

    cols = shift(cols,-1)
    cols[0] = h 

    setcol(cols, tick*3)

    time.sleep(tick)
    

