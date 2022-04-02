#!/usr/bin/env python

# Base class for implementing "point-style" animations using curve functions.

import acabsl
import time
import random
import colorsys

brightness = 1

def hsv_hue_colour(hue):
    colour = colorsys.hsv_to_rgb(hue, 1., brightness)
    return (colour[0]*255, colour[1]*255, colour[2]*255)

def random_colour():
    return hsv_hue_colour(random.randint(0,360)/360.)

class CurvePoint(object):
    def __init__(self, curve_function, colour = None, tail = 0):
        self.curve_function = curve_function
        self.tail = tail
        self.last_drawn = []

        if not colour:
            self.colour = random_colour()
        else:
            self.colour = colour

    def fade_out(self, fade):
        if not self.last_drawn:
            return False
        self.draw_single(self.last_drawn[0], (0,0,0), fade)
        del self.last_drawn[0]
        return True

    def draw(self, t, fade=0):
        if len(self.last_drawn) > self.tail:
            self.draw_single(self.last_drawn[0], (0,0,0), fade)
            del self.last_drawn[0]
        new_pos = self.curve_function(t)
        self.draw_single(new_pos, self.colour, fade)
        self.last_drawn.append(new_pos)

    def draw_single(self, pos, colour, fade=0):
        acabsl.send(pos[0], pos[1], *colour, t=fade)

class RainbowCurvePoint(CurvePoint):
    def __init__(self, *args, **kwargs):
        CurvePoint.__init__(self, *args, **kwargs)
        self.h = 0
        self.colour = hsv_hue_colour(self.h)
        self.spectrum_size = 5

    def recolour_end(self):
        self.h = 0
        self.colour = hsv_hue_colour(self.h)

    def draw(self, t, fade=0):
        super(RainbowCurvePoint, self).draw(t, fade)
        self.recolour_step(0)

    def recolour_step(self, t):
        self.h = (self.h + 1./self.spectrum_size) % 1.
        self.colour = hsv_hue_colour(self.h)

def roundtrip_cw(t, width = 12, height = 2):
    # only supports height = 2 /o\
    if (t / width) % 2 == 0:
        return (t % width, 0)
    return (width - 1 - (t % width), 1)

if __name__ == "__main__":
    for x in range(acabsl.WALLSIZEX):
        for y in range(acabsl.WALLSIZEY):
            acabsl.send(x, y, 0, 0, 0)
    acabsl.update()

    sleep_time = 0.07
    t = 0
    point = RainbowCurvePoint(roundtrip_cw, tail = 5)
    while True:
        point.draw(t, fade = sleep_time)
        acabsl.update()
        time.sleep(sleep_time)
        t += 1
