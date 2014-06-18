#!/usr/bin/env python
# -*- coding: utf-8 -*-

import acabsl
from acabsl import send
from acabsl import update
import colorsys
import random
import time

tick = 0.6

wall_count=acabsl.NOOFWALLS
rows=acabsl.WALLSIZEY
cols=acabsl.WALLSIZEX

r = 0
g = 180
b = 250
shade = 3

def blank_walls(row, time):
  for col in range(cols):
    for wall in range(wall_count):
      send(col,(row-2)%rows,0,0,0,time,wall);
  update()

def warp_ring(wall, row, time):
  for i in range(cols):
    if row < rows - 1: 
      send(i,(row+1)%rows,r/shade,g/shade,b/shade,time*1.5,wall);
    if row <= rows - 1:
      send(i,row,r,g,b,time/2,wall);
    if row > 0 and row <= rows:
      send(i, (row-1)%(rows),r/shade,g/shade,b/shade,time*1.5,wall);
  update()


c = 0

blank_walls(0, 0)

while 1:
  for wall in range(wall_count):
    warp_ring(wall, c, tick)

  c += 1
  c = c % (rows + 0)

  if c == 0:
    r, g, b = map(lambda x: x*255, colorsys.hsv_to_rgb(random.random(), 1, 1))
    print 'Warp Color:', r, g, b

  blank_walls(c, tick*1.5)
  time.sleep(tick*.8)


