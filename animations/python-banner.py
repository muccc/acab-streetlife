#!/usr/bin/env python
# -*- coding: utf-8 -*-
from acabsl import send
from acabsl import update
import acabsl

import colorsys
import random
import time

tick = 0.8

def setdata(data, time):
    for x in range(0,acabsl.WALLSIZEX):
        for y in range(0,acabsl.WALLSIZEY):
            r,g,b = colorsys.hsv_to_rgb(data[x][y], 1., 1.)
            send(x,y,r*255,g*255,b*255,time);
    update()

def shift(l,n):
    return l[n:] + l[:n]

f = 0.66
b = 0.16
data = [
[f,f,b, b, b,b,b, b, b,f,b ,b ,f,b,b ,b ,b,b,b ,b ,b,b,b ,b,b,b],
[f,b,f, b, f,b,f, b, b,f,b ,b ,f,f,b ,b ,b,f,b ,b ,f,f,b ,b,b,b],
[f,f,b, b, f,b,f, b, f,f,f ,b ,f,b,f ,b ,f,b,f ,b ,f,b,f ,b,b,b],
[f,b,b, b, f,b,f, b, b,f,b ,b ,f,b,f ,b ,f,b,f ,b ,f,b,f ,b,b,b],
[f,b,b, b, b,f,b, b, b,f,b ,b ,f,b,f ,b ,b,f,b ,b ,f,b,f ,b,b,b],
[b,b,b, b, f,b,b, b, b,b,b ,b ,b,b,b ,b ,b,b,b ,b ,b,b,b ,b,b,b]
]
data = zip(*data)
update()
while 1:
    data = shift(data,1)
    setdata(data, 0.1)
    time.sleep(tick)
    

