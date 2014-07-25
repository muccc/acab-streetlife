#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:expandtab sw=4 ts=4

import acabsl
import time
import colorsys
import random
import math

class Particle:
    def __init__(self, sx, sy):
        self.x = acabsl.WALLSIZEX/2.
        self.y = acabsl.WALLSIZEY/2.

        self.sx = sx
        self.sy = sy

    def inc(self):
        self.x += self.sx
        self.y += self.sy

        if self.x <= 0:
            self.sx = abs(self.sx)
        if self.x >= acabsl.WALLSIZEX-1:
            self.sx = -abs(self.sx)

        if self.y <= 0:
            self.sy = abs(self.sy)
        if self.y >= acabsl.WALLSIZEY-1:
            self.sy = -abs(self.sy)

    def light(self, x, y):
        c = 1.

        dx = abs(x - self.x)
        if dx > 1.:
            c = 0.
        else:
            c *= 1. - dx

        dy = abs(y - self.y)
        if dy > 1.:
            c = 0.
        else:
            c *= 1. - dy

        return c

t = .5
s = .2

pl = []
I = 20
for i in xrange(I):

    d = random.random()
    xs = s * math.cos(2.*math.pi*d)
    ys = s * math.sin(2.*math.pi*d)

    pl.append(Particle(xs, ys))

acabsl.update()

for x in range(acabsl.WALLSIZEX):
    for y in range(acabsl.WALLSIZEY):
        acabsl.send(x,y,0,0,0,1)
acabsl.update()

time.sleep(t)

l = 0.
ls = s

bu0 = None
while True:

    bu = [False] * (acabsl.WALLSIZEX * acabsl.WALLSIZEY)

    for x in range(acabsl.WALLSIZEX):
        for y in range(acabsl.WALLSIZEY):

            a = sum(p.light(x,y) for p in pl)

            xl =(x + l*ls) % acabsl.WALLSIZEX
            r0, g0, b0 = colorsys.hsv_to_rgb(float(xl)/acabsl.WALLSIZEX, 1., 1.)

            r = min(255, int(r0*a*255*1.4+max(0., a-1.)*255))
            g = min(255, int(g0*a*255*1.4+max(0., a-1.)*255))
            b = min(255, int(b0*a*255*1.4+max(0., a-1.)*255))

            i = y*acabsl.WALLSIZEX+x
            if r > 0 or g > 0 or b > 0:
                bu[i] = True
                acabsl.send(x,y,r,g,b,t)
            else:
                if bu0 is not None and bu0[i]:
                    acabsl.send(x,y,0,0,0,t)

    bu0 = bu

    acabsl.update()
    time.sleep(t)

    for p in pl:
        p.inc()

    l += 1
