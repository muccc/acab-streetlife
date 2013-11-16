#!/usr/bin/env python
# -*- coding: utf-8 -*-
import acabsl
from acabsl import send
from acabsl import update

import colorsys
import random
import time
import math

tick = 0.4

def setcol(col, r, g, b, time):
    for i in range(0,6):
    	send(col,i,r,g,b,time);

h = 0
col = 0

midcol = acabsl.WALLSIZEX/2
midrow = acabsl.WALLSIZEY/2

maxdist = 0
for row in range(0,acabsl.WALLSIZEY):
  for col in range(0,acabsl.WALLSIZEX):
    dc = col - midcol
    dr = row - midrow
    dist = math.sqrt(dc**2+dr**2)
    if dist > maxdist:
      maxdist = dist

hoffset = 0
update()
while 1:
  midcol = min(acabsl.WALLSIZEX-2,max(1, midcol + random.gauss(0,0.1)))
  midrow = min(acabsl.WALLSIZEY-2,max(1, midrow + random.gauss(0,0.1)))

  #hoffset += random.gauss(0.01,0.02)
  hoffset += 0.03
  hoffset = hoffset % 1.
  #t = time.time()

  for row in range(0,acabsl.WALLSIZEY):
    for col in range(0,acabsl.WALLSIZEX):
      dc = col - midcol
      dr = row - midrow
      dist = math.sqrt(dc**2+dr**2)/maxdist
      h = (math.atan2(dc, dr) + math.pi/2)/math.pi/2
      h = (h+hoffset) % 1.
      r,g,b = colorsys.hsv_to_rgb(h, dist, 1)
      send(int(col), int(row), r*255, g*255, b*255, tick*2)
  #print time.time()-t
  update()
  time.sleep(tick)
    

