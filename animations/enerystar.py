#!/usr/bin/python

import acabsl
import time
import sys
import schedule

turned_off = False

t = 1

acabsl.update()

def set_all(r,g,b):
    for w in range(acabsl.NOOFWALLS):
        for x in range(acabsl.WALLSIZEX):
            for y in range(acabsl.WALLSIZEY):
                acabsl.send(x,y,r,g,b,0,w)
    acabsl.update()

def turn_on():
    global turned_off
    turned_off = False

def turn_off():
    global turned_off
    turned_off = True

schedule.every().day.at("18:00").do(turn_on)
schedule.every().day.at("06:00").do(turn_off)

while 1:
    schedule.run_pending()
    if turned_off:
        set_all(0,0,0)
    time.sleep(t)



