#!/usr/bin/env python
# -*- coding: utf-8 -*-

import acabsl
import time
t = .3

acabsl.update()

def set_col(col,r,g,b,t):
    for w in range(acabsl.NOOFWALLS):
        for y in range(acabsl.WALLSIZEY):
            acabsl.send(col,y,r,g,b,t,w)

def set_all(r,g,b,t):
    for w in range(acabsl.NOOFWALLS):
        for x in range(acabsl.WALLSIZEX):
            for y in range(acabsl.WALLSIZEY):
                acabsl.send(x,y,r,g,b,t,w)

midcol = 7
dcol = 0

#set_all(0,0,0,0.5)
#acabsl.update()
#time.sleep(0.5)

#set_col(midcol, 255, 0, 0, t)
#acabsl.update()
#time.sleep(t)

while True:
    dcol = 0
    while midcol+dcol < acabsl.WALLSIZEX or midcol-dcol >= 0:
        set_col(midcol+dcol, 255, 0, 0, t*3)
        set_col(midcol-dcol, 255, 0, 0, t*3)
        acabsl.update()
        time.sleep(t)
        dcol+=1
    
    dcol = 0
    while midcol+dcol < acabsl.WALLSIZEX or midcol-dcol >= 0:
        set_col(midcol+dcol, 0, 0, 0, t*3)
        set_col(midcol-dcol, 0, 0, 0, t*3)
        acabsl.update()
        time.sleep(t)
        dcol+=1
    

