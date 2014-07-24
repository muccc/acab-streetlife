#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Strong colors (red, green, blue), with short color transitions, good for taking photos.

from acabsl import send
from acabsl import update
import acabsl

import colorsys
import random
import time

tick = 0.5

def setcol(cols, time):
    for x in range(0,acabsl.WALLSIZEX):
        r,g,b = colorsys.hsv_to_rgb(cols[x], 1., 1.)
        for y in range(0,acabsl.WALLSIZEY):
            send(x,y,r*255,g*255,b*255,time);
    update()

def rotate(l,n):
    return l[n:] + l[:n]

h = 0
col = 0
cols = []
for i in range(0,acabsl.WALLSIZEX):
    cols.append(0)
update()

index = 0
colors = [
    0.97 ,
    0.98 ,
    0.99 ,
    0.00 ,
    0.01 ,
    0.02 ,
    0.03 ,

    0.04,
    0.08,
    0.10,
    #0.12,
    #0.16,
    0.20,
    0.22,
    0.24,
    0.28,

    0.29 ,
    0.30 ,
    0.31 ,
    0.32 ,
    0.33 ,
    0.34 ,
    0.35 ,
    0.36 ,

    0.38,
    0.42,
    0.46,
    0.50,
    0.54,
    0.58,
    0.62,

    0.63 ,
    0.64 ,
    0.65 ,
    0.66 ,
    0.66 ,
    0.67 ,
    0.68 ,
    0.69 ,

    0.70,
    0.74,
    0.78,
    0.82,
    0.86,
    0.90,
    0.96
    ]

while 1:
    index += 1
    index = index % len(colors)

    cols = rotate(cols,-1)
    cols[0] = colors[index] 

    setcol(cols, .1)

    time.sleep(tick)
    

