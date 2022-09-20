#!/usr/bin/env python
# -*- coding: utf-8 -*-

import acabsl
import time
t = 1

acabsl.update()

def set_all(r,g,b):
    set_wall(r,g,b)
    set_decke(r,g,b)

def set_wall(r,g,b):
    acabsl.set_target("127.0.0.1",6002)
    for w in range(1):
        for x in range(6):
            for y in range(8):
                acabsl.send(x,y,r,g,b,1,w)
    acabsl.update()

def set_decke(r,g,b):
    acabsl.set_target("127.0.0.1",8002)
    for w in range(2):
        for x in range(12):
            for y in range(12):
                acabsl.send(x,y,r,g,b,1,w)
    acabsl.update()

def set_all_to_black():
    set_all(0,0,0)

def main():
    while 1:
        set_all_to_black()
        time.sleep(t)
 
if __name__ == '__main__':
    main()
