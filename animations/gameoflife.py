from acabsl import send
from acabsl import update
import acabsl

import colorsys
import random
import time

tick = .5
maxX = acabsl.WALLSIZEX
maxY = acabsl.WALLSIZEY
aliveC = [0,255,0]
deadC = [255,0,0]


class cell(object):
    def __init__(self, x, y, state):
        """
        track status of cell
        state is either:
        0 = dead
        1 = alive
        """
        self.curr_state = state
        self.pos = [x, y]


    def getState(self):
        """
        returns current state of cell
        """
        return self.curr_state

    def setState(self, state):
        """
        manually set the state of a cell
        state is either
        0 = dead or
        1 = alive
        """
        self.curr_state = state

    def updateState(self,universe):
        """
        updates the state of a cell
        take a list of the 8 neighbors states as argument
        """
        #determine neighborhood sum
        x = self.pos[0]
        y = self.pos[1]
        prev_state = self.curr_state
        neighborStates=[]
        for i in range(x-1 , x+2):
            for j in range(y-1 , y+2):
                neighborStates.append( universe[i % maxX][j % maxY].getState() )

        n = sum(neighborStates) - prev_state

        #cell is alive
        if (prev_state == 1 ) :
            #less than 2 or more than 3 neighbors: die
            if ( n < 2 or n > 3 ):
                self.curr_state = 0
        #cell is dead
        else :
            #3 neighnors: become alive
            if ( n == 3):
                self.curr_state = 1

def randomUniverse():
    """
    populates a universe with random state cells
    returns following datastructure:
    [
    [cell_object@0,0 , cell_object@1,0, cell_object@2,0, cell_object@3,0 ...]
    [cell_object@0,1 , cell_object@1,1, cell_object@2,1, cell_object@3,1,...]
    [cell_object@0,2 , cell_object@1,2, cell_object@2,2, cell_object@3,2 ...]
    ]
    """
    universe = []
    for x in range ( 0 , maxX ):
        universe.append( [] )
        for y in range ( 0 , maxY + 1 ):
            universe[x].append( cell( x , y , random.randint(0,1) ))
    return universe


u = randomUniverse()
h_dead = 0
update()
while 1:
    h_dead += random.gauss(0.02,0.05)
    h_dead = h_dead% 1
    h_alive = (h_dead + 0.5)%1
    rd, gd, bd = colorsys.hsv_to_rgb(h_dead,.3, .2)
    ra, ga, ba = colorsys.hsv_to_rgb(h_alive,1., 1.) 

    for i in range (0, maxX ):
        for j in range (0, maxY):
            if ( u[i][j].getState() == 0 ):
                send(i , j , rd*255, gd*255, bd*255 , tick*0.5)
            else:
                send(i , j , ra*255, ba*255, ba*255 , tick*0.5)
            u[i][j].updateState(u)
    update()
    time.sleep(tick)

