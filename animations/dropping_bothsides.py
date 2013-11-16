#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from acabsl import send
from acabsl import update
import acabsl

import colorsys
import random
import time

tick = 0.2

def setcol(col, r, g, b, rtime):
    for i in range(0,acabsl.WALLSIZEY):
        send(col,i,r,g,b,rtime,0);
	send(acabsl.WALLSIZEX - col - 1,i,r,g,b,rtime,0);
    	update()
	time.sleep(tick)
h = 0
col = 0
update()
while 1:
    h += 0.12
    h = h % 1.

    for col in range(0,(acabsl.WALLSIZEX / 2) + 1):
    	r,g,b = colorsys.hsv_to_rgb(h, 1., 1.)
    	setcol(col, r*255, g*255, b*255, tick*1)   
	col += 1 

