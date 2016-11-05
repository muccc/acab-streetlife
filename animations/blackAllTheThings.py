#!/usr/bin/env python
# -*- coding: utf-8 -*-

import acabsl
import time
t = 1

acabsl.update()

def set_all(r,g,b):
    acabsl.set_target("127.0.0.1",6002)
    for w in range(acabsl.NOOFWALLS):
        for x in range(acabsl.WALLSIZEX):
            for y in range(acabsl.WALLSIZEY):
                acabsl.send(x,y,r,g,b,1,w)
    acabsl.update()
    acabsl.set_target("127.0.0.1",8002)
    for w in range(acabsl.NOOFWALLS):
        for x in range(acabsl.WALLSIZEX):
            for y in range(acabsl.WALLSIZEY):
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
