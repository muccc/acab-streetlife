#choose random pixels and fade them to a random color in random time
#

import time
import random
import lib_sl

matrix = lib_sl.matrix()

def rcolor():
  return int(random.random()*255)

while "True":
  chosen = []
  i=0
  while ( i < 10):
   chosen.append(random.choice(matrix))
   i=i+1
  r=rcolor()
  b=rcolor()
  g=rcolor()
  t=1+(random.random()*5)
#  print chosen
#  print r, b, g, t
  for p in chosen:
     lib_sl.send( int(p[0]), int(p[1]), r, b, g, t)
     time.sleep(t/10) 
  time.sleep(t/10)


