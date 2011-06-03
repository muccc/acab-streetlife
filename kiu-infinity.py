import lib_sl
import random
import time

seq = 	[
	    [2,1,0,0,1,2,3,4,5,6,7,7,6,5,4,3],
	    [1,1,2,3,4,4,3,2,1,1,2,3,4,4,3,2],
	]

l = 1
s = 0.1

for c in range(0,8):
    for r in range(0,6):
	lib_sl.send(c,r,0,0,255, 500)

time.sleep(0.5)

i = 0


while 1:
    lib_sl.send(seq[0][i],seq[1][i],255,255,255, 500)

    if i - l < 0:
	r = 16 + i - l
    else :
	r = i - l

    lib_sl.send(seq[0][r],seq[1][r],0,0,255, 500)

    i = i + 1
    if i > 15:
	i = 0
	l = l + 1

	if l > 15:
	    l = 1

    time.sleep(s)

