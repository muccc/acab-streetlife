#!/usr/bin/python

import acabsl
import time
import random

t = 2.5 

acabsl.update()

def set_all(r,g,b):
    for w in range(acabsl.NOOFWALLS):
        for x in range(acabsl.WALLSIZEX):
            for y in range(acabsl.WALLSIZEY):
                acabsl.send(x,y,r,g,b,0,w)
    acabsl.update()


def set_random(r,g,b):
    for w in [random.choice(range(acabsl.NOOFWALLS))]:
        for x in [random.choice(range(acabsl.WALLSIZEX))]:
            for y in [random.choice(range(acabsl.WALLSIZEY))]:
                acabsl.send(x,y,r,g,b,0,w)
    acabsl.update()


while 1:
    set_all(0,0,0)
    #set_random(255,0,0)
    set_random(random.choice(range(0,255)),random.choice(range(0,255)),random.choice(range(0,255)))
    time.sleep(t)

