#!/usr/bin/python
#
#	Version: 0.2
#	Author: digit (markus)
#	Git: king-wee-wee
#

import acabsl
from random import randint
import pygame
from pygame.locals import *
import time
from threading import Thread

width = 16
height = 6
wait = 0.33

class posOutOfMapError(Exception):
	def __init__(self):
		Exception.__init__(self)

class posInTailError(Exception):
	def __init__(self):
		Exception.__init__(self)

class Direction:
	def __init__(self,x,y):
		self.direction = (x,y)

	def getNewPos(self,pos):
		return self.checkPos([pos[0]+self.direction[0],pos[1]+self.direction[1]])
	
	def alarm(self):
		raise posOutOfMapError

	def checkPos(self,pos):
		return (pos if pos[0]>=0 and pos[0]<width and pos[1]>=0 and pos[1]<height else self.alarm())

south = Direction(0,1)
north = Direction(0,-1)
east = Direction(1,0)
west = Direction(-1,0)
directions = [south,west,north,east]
tail = (122,122,122)
head = (0,0,255)
foodposition = []
foodcolor = (255,255,255)

class Player(Thread):
	def __init__(self,x=width/2,y=height/2-1):
		Thread.__init__(self)
		self.position = [x,y]
		self.tail = []
		self.deltail = []
		self.running = False
		self.direction = south
		self.error = False

	def run(self):
		redrawAll(self)
		seefood = 0
		while 1:
			seefood += 1
			drawMap(self,seefood%(2))
			time.sleep(wait)
			try:
				self.goForward()
			except posInTailError,posOutOfMapError:
				self.error = True
				break
			except Exception:
				self.error = True
				break

	#<unused>
	def changeRight(self):
		self.changeBoth(+1)

	def changeLeft(self):
		self.changeBoth(-1)

	def changeBoth(self,direction):
		self.direction = (0 if self.direction >= len(directions)-1 else (len(directions)-1 if self.direction <= 0 else self.direction+direction))
	#</unused>

	def changeDirection(self,direction):
		if direction.getNewPos(self.position) not in self.tail:
			self.direction = direction

	def goForward(self):
		global wait
		self.tail = [self.position]+self.tail
		if self.position != foodposition:
			self.deltail = self.tail[-1]
			del self.tail[-1]
		else:
			newFoodPosition(self)
			redrawAll(player)
			wait /= 1.1
		acabsl.send(self.position[0],self.position[1],*tail,t=wait)
		self.position = self.direction.getNewPos(self.position)
		for i in self.tail:
			if self.position == i:
				raise posInTailError
		"""if self.position != foodposition:
			self.deltail = self.tail[-1]
			del self.tail[-1]
		else:
			newFoodPosition(self)
			redrawAll(player)
			wait /= 1.1"""

def redrawAll(player,seefood=True):
	acabsl.update()
	for i in xrange(width):
		for j in xrange(height):
			acabsl.send(i,j,0,0,0)
	acabsl.update()
	for i in player.tail:
		acabsl.send(i[0],i[1],*tail)
	acabsl.send(player.position[0],player.position[1],*head)
	if seefood:
		acabsl.send(foodposition[0],foodposition[1],*foodcolor,t=wait)

def drawMap(player,seefood):
	acabsl.send(player.position[0],player.position[1],*head)
	if player.deltail:
		acabsl.send(player.deltail[0],player.deltail[1],0,0,0)
	if seefood:
		acabsl.send(foodposition[0],foodposition[1],*foodcolor,t=wait)
	else:
		acabsl.send(foodposition[0],foodposition[1],0,0,0,wait)

def newFoodPosition(player):
	global foodposition
	while not foodposition or foodposition in player.position or foodposition in player.tail:
		foodposition = [randint(0,width-1),randint(0,height-1)]

player = Player()
newFoodPosition(player)
pygame.init()
screen = pygame.display.set_mode((10,10))
pygame.display.set_caption("Pygame Caption")
pygame.mouse.set_visible(0)
go = False
redrawAll(player)
while not go:
	for event in pygame.event.get():
		if event.type==KEYDOWN:
			if event.key == K_DOWN:
				go = True
player.start()
while 1:
	if player.error:
		print "Game Over"
		print "Tail length: %d" % len(player.tail)
		break
	c = ""
	#temporary
	for event in pygame.event.get():
		if event.type==KEYDOWN:
			if event.key == K_LEFT:
				c = "l"
			elif event.key == K_RIGHT:
				c = "r"
			elif event.key == K_UP:
				c = "u"
			elif event.key == K_DOWN:
				c = "d"
	if c:
		if c == "u":
			player.changeDirection(north)
		elif c == "r":
			player.changeDirection(east)
		elif c == "l":
			player.changeDirection(west)
		elif c == "d":
			player.changeDirection(south)
	else:
		pass
	time.sleep(wait/10)
