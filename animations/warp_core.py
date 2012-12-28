#!/usr/bin/python

from acabsl import send
from acabsl import update
import colorsys
import random
import time

tick = 0.5

wall_count=2
rows=6
cols=8

r = 0
g = 180
b = 250
shade = 3

def blank_walls():
  for col in range(cols):
    for row in range(rows):
      for wall in range(wall_count):
        send(wall,col,row,0,0,0,0);
  update()

def warp_ring(wall, row, time):
  for i in range(cols):
    if row < rows - 1: 
      send(wall,i,row+1,r/shade,g/shade,b/shade,time);
    if row <= rows - 1:
      send(wall,i,row,r,g,b,time);
    if row > 0 and row <= rows:
      send(wall,i, row-1,r/shade,g/shade,b/shade,time);

  update()


c = 0

blank_walls()

while 1:
  warp_ring(0, c, tick)
  warp_ring(1, c, tick)

  c += 1
  c = c % (rows + 2)

  time.sleep(tick)
  
  blank_walls()


