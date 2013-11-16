#!/usr/bin/env python
# -*- coding: utf-8 -*-
import acabsl
import colorsys
import random
import time

NOOFWALLS=2

tick = 0.5

def set(r,g,b,time):
    for x in  range(acabsl.WALLSIZEX):
        for y in range(acabsl.WALLSIZEY):
            for wall in range(acabsl.NOOFWALLS):
                acabsl.send(x,y,r,g,b,time,wall)
h = 0
col = 0
acabsl.update()
while 1:
    h += random.gauss(0.02,0.05)
    h = h % 1.

    col += 1
    col = col % 8

    r,g,b = colorsys.hsv_to_rgb(h, 1., 1.)
    set(r*255, g*255, b*255, tick)
    acabsl.update()
    time.sleep(tick*3)

    set(0, 0, 0, tick*3)
    acabsl.update()
    time.sleep(tick*3)

    

