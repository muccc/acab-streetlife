import acabsl
import random
import time

cs =	[
	    [255,255,000,000,000,255],
	    [000,255,255,255,000,000],
	    [000,000,000,255,255,255],
	]
tfade = 0.3
tick = 0.1

def drawa(c,r,c1):

    acabsl.send(c,r,cs[0][c1],cs[1][c1],cs[2][c1],tfade)
    for x in range(1,c):
	acabsl.send(x,r,cs[0][c1],cs[1][c1],cs[2][c1],tfade)

    for y in range(0,r):
	acabsl.send(c,y,cs[0][c1],cs[1][c1],cs[2][c1],tfade)
    acabsl.update()

def drawb(c,r,c1):

    acabsl.send(c,r,cs[0][c1],cs[1][c1],cs[2][c1],tfade)
    for x in range(c,7):
	acabsl.send(x,r,cs[0][c1],cs[1][c1],cs[2][c1],tfade)

    for y in range(0,r):
	acabsl.send(c,y,cs[0][c1],cs[1][c1],cs[2][c1],tfade)
    acabsl.update()

def drawc(c,r,c1):

    acabsl.send(c,r,cs[0][c1],cs[1][c1],cs[2][c1],tfade)
    for x in range(c,7):
	acabsl.send(x,r,cs[0][c1],cs[1][c1],cs[2][c1],tfade)

    for y in range(r,6):
	acabsl.send(c,y,cs[0][c1],cs[1][c1],cs[2][c1],tfade)
    acabsl.update()

def drawd(c,r,c1):

    acabsl.send(c,r,cs[0][c1],cs[1][c1],cs[2][c1],tfade)
    for x in range(1,c):
	acabsl.send(x,r,cs[0][c1],cs[1][c1],cs[2][c1],tfade)

    for y in range(r,6):
	acabsl.send(c,y,cs[0][c1],cs[1][c1],cs[2][c1],tfade)
    acabsl.update()



acabsl.update()
for c in range(0,16):
    for r in range(0,6):
        acabsl.send(c,r,0,0,0, 0.5)
acabsl.update()
time.sleep(0.5)

x = 1
y = 0
lastc = 0
c = 0
mode = 0
lastm = 0

while 1:

    while c == lastc:
	c = random.randint(0,5)
    lastc = c

    if mode != lastm:
	time.sleep(tick * 6)
	lastm = mode
    
    if mode == 0:    
	drawa(x,y,c)

	x = x + 1
	y = y + 1
	if x > 6:
	    x = 6
	    y = 0
	    mode = 1

    if mode == 1:
	drawb(x,y,c)

	x = x - 1
	y = y + 1
	if x < 1:
	    x = 6
	    y = 5
	    mode = 2

    if mode == 2:
	drawc(x,y,c)

	x = x - 1
	y = y - 1
	if x < 1:
	    x = 1
	    y = 5
	    mode = 3

    if mode == 3:
	drawd(x,y,c)

	x = x + 1
	y = y - 1
	if x > 6:
	    x = 1
	    y = 0
	    mode = 0
	
    time.sleep(tick)

