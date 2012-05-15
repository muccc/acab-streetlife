import pygame
from pygame.locals import *
import sys
import threading

import bottle
from bottle import route, run, request

#bottle.debug(True)

xsize = 60
ysize = 40

xpixels = 16
ypixels = 6

acab = [[[0,0,0,0,0,0,0] for col in range(ypixels)] for row in range(xpixels)]

def handle_events():
    surf = pygame.Surface((xsize,ysize))
    while 1:
        for event in pygame.event.get():
            if event.type in (QUIT, QUIT):
                import os
                os.kill(os.getpid(), 9)
        for y in range(0,ypixels):
            for x in range (0,xpixels):
                current = acab[x][y][0:3]
                diff    = acab[x][y][3:6]
                count   = acab[x][y][6]

                new = [max((0,min((current[i] + diff[i],255)))) for i in range(3)]
                count -= 1
                if count == 0:
                    diff = [0,0,0]
                
                surf.fill(tuple(map(int, new)))
                screen.blit(surf, (x*xsize, y*ysize))
                
                acab[x][y][0:3] = new
                acab[x][y][3:6] = diff
                acab[x][y][6]   = count
        pygame.display.update()
        pygame.time.delay(33)

pygame.init()

screen = pygame.display.set_mode((xpixels*xsize, ypixels*ysize))
screen.fill((255, 255, 255))

updatethread = threading.Thread(target=handle_events)
updatethread.start()

@route('/:x/:y/:r/:g/:b/:t')
def fade(**kwargs):
    args = dict(map(lambda tp: (tp[0], int(tp[1])),
        kwargs.iteritems()))
    x = args['x']
    y = args['y']
    r = args['r']
    g = args['g']
    b = args['b']
    time = args['t']
    
    data = acab[x][y]
    current = data[0:3]
    target = [r,g,b]
    diff = [target[i] - current[i] for i in range(3)]
    steps = time/33
    if steps == 0:
        data[0:3] = target
        data[3:6] = [0,0,0]
    else:
        data[3:6] = [ d/float(steps) for d in diff]

    data[6] = steps
    acab[x][y] = data
    return '(%s/%s) @ (%s, %s, %s) -> %s' % (x, y, r, g, b, 0)

run(host='localhost', port=8080)


