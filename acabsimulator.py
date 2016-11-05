#!/usr/bin/env python2

import pygame
from pygame.locals import *
import sys
import threading
import socket
import thread
import time
import Queue
import sys
from string import atof
import acabsl

UDP_IP="0.0.0.0"
UDP_PORT=int(sys.argv[2])
q = Queue.Queue(100)

try: f = atof(sys.argv[3])
except:
    f = 1

xsize = int(60*f)
ysize = int(40*f)

xpixels = acabsl.WALLSIZEX
ypixels = acabsl.WALLSIZEY

acab = [[[0,0,0,0,0,0,0,0,0] for col in range(ypixels)] for row in range(xpixels)]

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
                counts   = acab[x][y][6:9]
                
                new = [0, 0, 0]
                for i in range(3):
                    new[i] = max((0,min((current[i] + diff[i],255))))
                    counts[i] = counts[i] - 1
                    if counts[i] == 0:
                        diff[i] = 0
                
                surf.fill(tuple(map(int, new)))
                screen.blit(surf, (x*xsize, y*ysize))
                
                acab[x][y][0:3] = new
                acab[x][y][3:6] = diff
                acab[x][y][6:9] = counts
        pygame.display.update()
        pygame.time.delay(33)

pygame.init()

screen = pygame.display.set_mode((xpixels*xsize, ypixels*ysize))
screen.fill((255, 255, 255))
sleep(3)
screen.fill((255, 0, 0))
sleep(3)
screen.fill((0, 255, 0))
sleep(3)
screen.fill((0, 0, 255))
sleep(3)
screen.fill((255, 255, 255))


pygame.display.set_caption(sys.argv[1])
updatethread = threading.Thread(target=handle_events)
updatethread.start()


def writer():
    while 1:
        data = q.get()
        try:
            x = ord(data[0])
            y = ord(data[1])
            cmd = data[2]
            r = ord(data[3])
            g = ord(data[4])
            b = ord(data[5])
            msh = ord(data[6])
            msl = ord(data[7])
            ms = (msh<<8) + msl;
            if cmd == 'C':
                time = ms
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

                data[6:9] = [steps, steps, steps]
                acab[x][y] = data

            elif cmd == 'F':
                speed = ms / 58.7
                data = acab[x][y]
                current = data[0:3]
                target = [r,g,b]
                diff = [target[i] - current[i] for i in range(3)]
                
                data[3:6] = [speed, speed, speed]
                data[6:9] = [d/speed for d in diff]

                for i in range(3):
                    if diff[i] < 0:
                        data[3+i] = -data[3+i]
                        data[6+i] = -data[6+i]
                print(data)
                acab[x][y] = data

            elif cmd == 'U':
                pass
        except Exception as e:
            import traceback
            traceback.print_exc()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))
thread.start_new_thread(writer,())

while True:
    data = sock.recv(1024)
    if not q.full():
        q.put(data)
    else:
        print('ignoring data')


