#!/usr/bin/env python
# -*- coding: utf-8 -*-

import acabsl
import time
t = 1

acabsl.update()

def set_all(r,g,b):
    for w in range(1):
        for x in range(2):
            for y in range(12):
                acabsl.send(x,y,r,g,b,1,1)
    acabsl.update()

while 1:
    set_all(0,0,0)
    time.sleep(t)



