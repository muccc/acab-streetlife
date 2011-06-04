# 209
import lib_sl
import random
import time

cs = [[255,255,000,000,000,255],[000,255,255,255,000,000],[000,000,000,255,255,255]]

def rc():
  return random.randint(0,5)

def rid():
    return [random.randint(0,8),random.randint(0,6)]


while 1:
    lib_sl.send(0,0,171,205,239)
    lib_sl.send(0,1,171,205,239)
    lib_sl.send(0,2,171,205,239)
    lib_sl.send(0,3,171,205,239)
    lib_sl.send(0,4,171,205,239)
    lib_sl.send(0,5,171,205,239)
    lib_sl.send(0,6,171,205,239)
    lib_sl.send(0,7,171,205,239)
    lib_sl.send(1,0,171,205,239)
    lib_sl.send(1,1,171,205,239)
    lib_sl.send(1,2,171,205,239)
    lib_sl.send(1,3,171,205,239)
    lib_sl.send(1,4,171,205,239)
    lib_sl.send(1,5,171,205,239)
    lib_sl.send(1,6,171,205,239)
    lib_sl.send(1,7,171,205,239)
    lib_sl.send(2,0,171,205,239)
    lib_sl.send(2,1,171,205,239)
    lib_sl.send(2,2,171,205,239)
    lib_sl.send(2,3,171,205,239)
    lib_sl.send(2,4,171,205,239)
    lib_sl.send(2,5,171,205,239)
    lib_sl.send(1,6,171,205,239)
    lib_sl.send(1,7,171,205,239)
    lib_sl.send(3,0,171,205,239)
    lib_sl.send(3,1,171,205,239)
    lib_sl.send(3,2,171,205,239)
    lib_sl.send(3,3,171,205,239)
    lib_sl.send(3,4,171,205,239)
    lib_sl.send(3,5,171,205,239)
    lib_sl.send(1,6,171,205,239)
    lib_sl.send(1,7,171,205,239)
    lib_sl.send(4,0,171,205,239)
    lib_sl.send(4,1,171,205,239)
    lib_sl.send(4,2,171,205,239)
    lib_sl.send(4,3,171,205,239)
    lib_sl.send(4,4,171,205,239)
    lib_sl.send(4,5,171,205,239)
    lib_sl.send(1,6,171,205,239)
    lib_sl.send(1,7,171,205,239)
    lib_sl.send(5,0,171,205,239)
    lib_sl.send(5,1,171,205,239)
    lib_sl.send(5,2,171,205,239)
    lib_sl.send(5,3,171,205,239)
    lib_sl.send(5,4,171,205,239)
    lib_sl.send(5,5,171,205,239)
    lib_sl.send(5,6,171,205,239)
    lib_sl.send(5,7,171,205,239)
    time.sleep(50.0)
