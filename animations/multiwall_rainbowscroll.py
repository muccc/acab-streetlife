#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acabsl import send
from acabsl import update
import acabsl
import colorsys
import random
import time

tick = 3.7

def setcol(col, r, g, b, time):
    for wall in range(acabsl.NOOFWALLS):
        for i in range(0,acabsl.WALLSIZEY):
            send(col,i,r,g,b,time,wall);
    update()
h = 0
col = 0
update()
while 1:
    h += random.gauss(0.02,0.05)
    h = h % 1.

    col += 1
    col = col % acabsl.WALLSIZEX

    r,g,b = colorsys.hsv_to_rgb(h, 1., 1.)
    setcol(col, r*255, g*255, b*255, tick*3)

    time.sleep(tick)
    

