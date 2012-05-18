# 74
import lib_sl
import random
import time

cs = [[255,255,000,000,000,255],[000,255,255,255,000,000],[000,000,000,255,255,255]]

def rc():
  return random.randint(0,5)

def rid():
    return [random.randint(0,8),random.randint(0,6)]


while 1:
    lib_sl.send(0,0,170,170,170)
    lib_sl.send(0,1,170,170,170)
    lib_sl.send(0,2,170,170,170)
    lib_sl.send(0,3,170,170,170)
    lib_sl.send(0,4,170,170,170)
    lib_sl.send(0,5,170,170,170)
    lib_sl.send(1,0,170,170,170)
    lib_sl.send(1,1,170,170,170)
    lib_sl.send(1,2,170,170,170)
    lib_sl.send(1,3,170,170,170)
    lib_sl.send(1,4,170,170,170)
    lib_sl.send(1,5,170,170,170)
    lib_sl.send(2,0,170,170,170)
    lib_sl.send(2,1,170,170,170)
    lib_sl.send(2,2,170,170,170)
    lib_sl.send(2,3,170,170,170)
    lib_sl.send(2,4,170,170,170)
    lib_sl.send(2,5,170,170,170)
    lib_sl.send(3,0,170,170,170)
    lib_sl.send(3,1,170,170,170)
    lib_sl.send(3,2,170,170,170)
    lib_sl.send(3,3,170,170,170)
    lib_sl.send(3,4,170,170,170)
    lib_sl.send(3,5,170,170,170)
    lib_sl.send(4,0,170,170,170)
    lib_sl.send(4,1,170,170,170)
    lib_sl.send(4,2,170,170,170)
    lib_sl.send(4,3,170,170,170)
    lib_sl.send(4,4,170,170,170)
    lib_sl.send(4,5,170,170,170)
    lib_sl.send(5,0,170,170,170)
    lib_sl.send(5,1,170,170,170)
    lib_sl.send(5,2,170,170,170)
    lib_sl.send(5,3,170,170,170)
    lib_sl.send(5,4,170,170,170)
    lib_sl.send(5,5,170,170,170)
    lib_sl.send(6,0,170,170,170)
    lib_sl.send(6,1,170,170,170)
    lib_sl.send(6,2,170,170,170)
    lib_sl.send(6,3,170,170,170)
    lib_sl.send(6,4,170,170,170)
    lib_sl.send(6,5,170,170,170)
    lib_sl.send(7,0,170,170,170)
    lib_sl.send(7,1,170,170,170)
    lib_sl.send(7,2,170,170,170)
    lib_sl.send(7,3,170,170,170)
    lib_sl.send(7,4,170,170,170)
    lib_sl.send(7,5,170,170,170)
    time.sleep(8.0)
