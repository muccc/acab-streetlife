import pygame
from pygame.locals import *
import sys
import threading

import bottle
from bottle import route, run, request

bottle.debug(True)

def handle_events():
    while 1:
        for event in pygame.event.get():
            if event.type in (QUIT, QUIT):
                import os
                os.kill(os.getpid(), 9)

        pygame.display.update()
        pygame.time.delay(100)

pygame.init()

screen = pygame.display.set_mode((240, 120))
screen.fill((255, 255, 255))

updatethread = threading.Thread(target=handle_events)
updatethread.start()

@route('/:x/:y/:r/:g/:b/:t')
def fade(**kwargs):
    args = dict(map(lambda tp: (tp[0], int(tp[1])),
        kwargs.iteritems()))
    surf = pygame.Surface((30,20))
    x = args['x']
    y = args['y']
    r = args['r']
    g = args['g']
    b = args['b']
    surf.fill(tuple(map(int, (r, g, b))))
    screen.blit(surf, (x*30, y*20))
    return '(%s/%s) @ (%s, %s, %s) -> %s' % (x, y, r, g, b, 0)

run(host='localhost', port=8080)


