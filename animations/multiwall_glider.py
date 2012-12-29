import acabsl

import time
import math

from functools import partial

acabsl.update()

WALLS = 2
LINES = 6
COLS  = 8

DIM = (WALLS, COLS, LINES)
acabsl.update()

def fill(dimensions, color, ftime, draw = True):
    walls, cols, lines = dimensions
    r, g, b            = color
  
    for w in range(walls):
        for col in range(cols):
            for l in range(lines):
                acabsl.send(w, col, l, r, g, b, ftime)

    if draw:
        acabsl.update()
        time.sleep(ftime)

def vline(dimensions, col, color, ftime, draw = True):
    walls, cols, lines = dimensions

    pixels = []
    for l in range(lines):
        pixels.append((0, l, color))

    pattern(dimensions, col, 0, color, ftime, pixels, draw)

def hline(dimensions, line, color, ftime, draw = True):
    walls, cols, lines = dimensions

    pixels = []
    for c in range(cols * walls):
        pixels.append((c, 0, color))

    pattern(dimensions, 0, line, color, ftime, pixels, draw)

def hpscan(dim, direction, bgcolor, delay, ftime, pat, cl = True):
    walls, cols, lines = dim

    all_cols = range(-1 * cols, 1 + cols * walls)

    rev = 0 > direction
    d   = -1 if rev else 1

    for col in reversed(all_cols) if rev else all_cols:

        if cl:
            fill(dim, bgcolor, 0, False)
        
        pat(dimensions=dim, x=col, ftime=ftime, draw=False)
        
        acabsl.update()
        time.sleep(ftime + delay)

def hlscan(dimensions, direction, fgcolor, bgcolor, delay, ftime, cl = False):
    walls, cols, lines = dimensions

    rev = 0 > direction
    d   = -1 if rev else 1

    for col in reversed(range(cols * walls))  if rev else range(cols * walls):

        if cl:
            fill(dimensions, bgcolor, ftime, False)
        
        vline(dimensions, max(-1, col + d), fgcolor, ftime, False)
        vline(dimensions, col, bgcolor, ftime, False)
        
        acabsl.update()
        time.sleep(ftime + delay)

def vlscan(dimensions, direction, fgcolor, bgcolor, delay, ftime, cl = False):
    walls, cols, lines = dimensions

    rev = 0 > direction
    d   = -1 if rev else 1

    for line in reversed(range(lines)) if rev else range(lines):
    
        if cl:
            fill(dimensions, bgcolor, ftime, False)

        hline(dimensions, max(-1, line + d), fgcolor, ftime, False)
        hline(dimensions, line, bgcolor, ftime, False)
    
        acabsl.update()
        time.sleep(ftime + delay)

def lifeform(dimensions, x, y, color, ftime, draw = True):

    pixels = [ (0, 2, color), (1, 2, color), (2, 2, color), \
               (2, 1, color), (1, 0, color) ]

    return pattern(dimensions, x, y, color, ftime, pixels, draw = True)

def pattern(dimensions, x, y, color, ftime, pixels, draw = True):
    walls, cols, lines = dimensions

    def map_pixel(dimensions, x, y, pixel):
        walls, cols, lines = dimensions
        px, py, pcolor     = pixel

        return int((x + px) / cols), (x + px) % cols, y + py, pcolor


    for p in pixels:
        w, c, l, (r, g, b) = map_pixel(dimensions, x, y, p)

        if w>-1 and c>-1 and l>-1 and w<walls and c<cols and l<lines:
            acabsl.send(w, c, l, r, g, b, ftime)


    if draw:
        acabsl.update()
        time.sleep(ftime)

fill(DIM, (0, 0, 0), 0)
hlscan(DIM, 1, (255, 0, 0), (0, 255, 0), 0.1, 0)

lifeform(DIM, 1, 2, (255, 0, 0), 1)
fill(DIM, (0, 0, 0), 1)

vlscan(DIM, 1, (255, 0, 0), (0, 0, 255), 0.2, 0)
vlscan(DIM, -1, (0, 255, 0), (0, 0, 0), 0.2, 0)

hpscan(DIM, 1, (0, 0, 0), 0.1, 0, partial(lifeform, y=2, color=(255, 255, 0)))

fill(DIM, (0, 0, 255), 3)
fill(DIM, (0, 255, 255), 2)
fill(DIM, (0, 255, 0), 1)

hlscan(DIM, 1, (255, 0, 0), (0, 255, 0), 0.1, 0)
hlscan(DIM, -1, (255, 0, 0), (0, 128, 128), 0.1, 0)
hlscan(DIM, 1, (255, 0, 0), (64, 0, 128), 0.1, 0)
hlscan(DIM, 1, (255, 0, 0), (0, 0, 0), 0.2, 0.3)

fill(DIM, (0, 255, 0), 3)
fill(DIM, (0, 0, 0), 3)

hlscan(DIM, 1, (255, 0, 0), (0, 0, 0), 0, 0.5)
hlscan(DIM, -1, (255, 0, 0), (0, 255, 0), 0, 0.5, True)

fill(DIM, (0, 0, 0), 5)

hpscan(DIM, 1, (255, 0, 0), 0.1, 0, partial(lifeform, y=2, color=(255, 255, 0)))
hpscan(DIM, 1, (0, 0, 0), 0.1, 0, partial(lifeform, y=1, color=(0, 255, 0)))
hpscan(DIM, 1, (0, 0, 255), 0.1, 0, partial(lifeform, y=3, color=(255, 255, 0)))
hpscan(DIM, 1, (0, 0, 0), 0.1, 0, partial(lifeform, y=2, color=(255, 255, 0)))

fill(DIM, (0, 0, 0), 5)
