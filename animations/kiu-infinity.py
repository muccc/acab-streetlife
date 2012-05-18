import acabsl
import random
import time

seq = 	[
	    [2,1,0,0,1,2,3,4,5,6,7,7,6,5,4,3],
	    [1,1,2,3,4,4,3,2,1,1,2,3,4,4,3,2],
	]

l = 1
s = 0.1

acabsl.update()
for c in range(0,16):
    for r in range(0,6):
	acabsl.send(c,r,0,0,255, 0.5)
acabsl.update()

time.sleep(0.5)

i = 0

while 1:
    acabsl.send(4+seq[0][i],seq[1][i],255,255,255, 0.5)

    if i - l < 0:
	r = 16 + i - l
    else :
	r = i - l

    acabsl.send(4+seq[0][r],seq[1][r],0,0,255, 0.5)

    i = i + 1
    if i > 15:
	i = 0
	l = l + 1

	if l > 15:
	    l = 1
    acabsl.update()
    time.sleep(s)

