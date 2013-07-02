#!/usr/bin/python

import acabsl
from acabsl import send
from acabsl import update
import colorsys
import random
import time

tick = 0.5

wall_count=acabsl.NOOFWALLS
rows=acabsl.WALLSIZEY
cols=acabsl.WALLSIZEX

r = 0
g = 180
b = 250
shade = 3

def blank_walls():
  for col in range(cols):
    for row in range(rows):
      for wall in range(wall_count):
        send(col,row,0,0,0,0,wall);
        print col,row,wall
  update()

def warp_ring(wall, row, time):
  for i in range(cols):
    if row < rows - 1: 
      send(i,row+1,r/shade,g/shade,b/shade,time,wall);
      print i,row+1,wall
    if row <= rows - 1:
      send(i,row,r,g,b,time,wall);
      print i,row,wall
    if row > 0 and row <= rows:
      send(i, row-1,r/shade,g/shade,b/shade,time,wall);
      print i,row-1,wall

  update()


c = 0

blank_walls()

while 1:
  for wall in range(wall_count):
    warp_ring(wall, c, tick)

  c += 1
  c = c % (rows + 2)

  time.sleep(tick)
  
  blank_walls()


