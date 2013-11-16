#!/usr/bin/env python
# -*- coding: utf-8 -*-
import acabsl
import colorsys
import random
import time

NOOFWALLS=2

tick = 0.2

wall0 = 0
wall1 = 1

def setcol(col, r, g, b, time):
    row = int(float(col)/8.*6)
    acabsl.send(col,row,r,g,b,time,wall0);
    col = 7 - col
    acabsl.send(col,row,r,g,b,time,wall1);
    acabsl.update()

def black(time):
    for x in  range(acabsl.WALLSIZEX):
        for y in range(acabsl.WALLSIZEY):
            for wall in range(acabsl.NOOFWALLS):
                acabsl.send(x,y,0,0,0,time,wall)
h = 0
col = 0
black(tick)
acabsl.update()
while 1:
    h += random.gauss(0.02,0.05)
    h = h % 1.

    col += 1
    col = col % 8

    r,g,b = colorsys.hsv_to_rgb(h, 1., 1.)
    setcol(col, r*255, g*255, b*255, tick*3)

    time.sleep(tick)
    

