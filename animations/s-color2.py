from acabsl import send
import colorsys
import random
import time
import math

tick = 0.5

def setcol(col, r, g, b, time):
    for i in range(0,6):
    	send(col,i,r,g,b,time);

h = 0
col = 0

midcol = 8
midrow = 2
maxdist = 0
for row in range(0,6):
  for col in range(0,15):
    dc = col - midcol
    dr = row - midrow
    dist = math.sqrt(dc**2+dr**2)
    if dist > maxdist:
      maxdist = dist

hoffset = 0
while 1:
  #hoffset += random.gauss(0.01,0.02)
  hoffset += 0.1
  hoffset = hoffset % 1.

  for row in range(0,6):
    for col in range(0,16):
      dc = col - midcol
      dr = row - midrow
      dist = math.sqrt(dc**2+dr**2)/maxdist
      h = (math.atan2(dc, dr) + math.pi/2)/math.pi
      h = (h+hoffset) % 1.
      r,g,b = colorsys.hsv_to_rgb(h, dist, 1.)
      send(col, row, r*255, g*255, b*255, tick)
  time.sleep(tick)
    

