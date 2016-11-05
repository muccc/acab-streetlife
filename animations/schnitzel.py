#!/usr/bin/python

import acabsl
import time
import serialinterface
import sys
import random

print sys.argv[1]

serial = serialinterface.SerialInterface(sys.argv[1],115200,1)

t = 1

acabsl.update()

def set_all(r,g,b):
    for w in range(acabsl.NOOFWALLS):
        for x in range(acabsl.WALLSIZEX):
            for y in range(acabsl.WALLSIZEY):
                acabsl.send(x,y,r,g,b,0,w)

def set_pattern():
    set_all(0,0,0)
    r = random.random()*127+127
    g = random.random()*127+127
    b = random.random()*127+127
    
    acabsl.send(5,0,r,g,b)
    acabsl.send(5,0,r,g,b)
    acabsl.send(7,0,r,g,b)
    acabsl.send(8,0,r,g,b)
    acabsl.send(9,0,r,g,b)
    acabsl.send(0xA,0,r,g,b)
    acabsl.send(0xD,0,r,g,b)


    acabsl.send(6,1,r,g,b)
    acabsl.send(8,1,r,g,b)
    acabsl.send(9,1,r,g,b)
    acabsl.send(0XC,1,r,g,b)

    acabsl.send(6,2,r,g,b)
    acabsl.send(8,2,r,g,b)
    acabsl.send(0xB,2,r,g,b)
    acabsl.send(0xC,2,r,g,b)


    acabsl.send(5,3,r,g,b)
    acabsl.send(5,3,r,g,b)
    acabsl.send(7,3,r,g,b)
    acabsl.send(0xA,3,r,g,b)
    acabsl.send(0xC,3,r,g,b)
    acabsl.send(0xD,3,r,g,b)
    acabsl.send(0xE,3,r,g,b)

    acabsl.send(0x8,4,r,g,b)
    acabsl.send(0x9,4,r,g,b)
    acabsl.send(0xB,4,r,g,b)

t0 = 0
while 1:
    #channel, message = serial.readMessage()
    message = serial.readMessage()
    #print channel, message
    #if channel and message == 'bar':
    if message == 'bar':
        if time.time() - t0 > 1:
            set_pattern()
            acabsl.update()
            t0 = time.time()
    #time.sleep(1)



