import acabsl
import pygame
#import r0ket_input
from pygame.locals import *
from threading import Thread
from random import randint
from time import sleep,time

width = 16
height = 6

cover_time = 1
uncover_time = 0.2
mark_time = 0.2
unmark_time = 0.2
hide_time = 0.2

minimumsleep = 0.05

covered = (33,33,33)
background = (0,0,0)
defaulthidecolor = background
defaultuncover = (0,255,0)
marked = (0,0,255)

def send(pos,rgb,fadet=0):
	acabsl.send(pos[0],pos[1],*rgb,t=fadet)
	acabsl.update()

def reset():
	acabsl.update()
	for i in xrange(width):
		for j in xrange(height):
			acabsl.send(i,j,*background)
	acabsl.update()

class Field:
	def __init__(self,masterAnimation,position,vanish = True):
		self.masterAnimation = masterAnimation
		self.position = position
		self.vanish = vanish
		self.covered = True
		self.random = 0
		self.duration = 0

		self.hideColor = defaulthidecolor
		self.uncoverColor = defaultuncover

		self.changedpositions = []

	def restUncover(self):
		for i in self.changedpositions:
			self.masterAnimation.player.updateSingle(i)
		self.changedpositions = []
		self.masterAnimation.player.updateSingle(self)

	def restUncoverColor(self):
		self.adjustedSend(self.position,self.uncoverColor,uncover_time)

	def uncover(self):
		self.covered = False
		self.random = 0
		self.changedpositions = []
		self.duration = time()
		self.loadAnimation()
		self.duration = time()-self.duration

	def cover(self):
		self.adjustedSend(self.position,covered,cover_time)
		self.covered = True

	def hide(self):
		self.adjustedSend(self.position,self.hideColor,hide_time)

	def checkMatching(self):
		return self.masterAnimation.checkMatching()

	def loadAnimation(self):
		pass

	def send(self,position=None,rgb=None,fadet=0):
		self.adjustedSend(position if position else self.position,rgb if rgb else background,fadet)

	def adjustedSend(self,position,rgb,fadet=0):
		if self.position != self.masterAnimation.player.marked or self.masterAnimation.player.fieldclicked:
			if position != self.position:
				self.changedpositions.append(position)
			self.masterAnimation.player.adjustedSend(position,rgb,fadet)

	def virtualWidth(self):
		return self.masterAnimation.player.virtualWidth

	def virtualHeight(self):
		return self.masterAnimation.player.virtualHeight

	def p(self,x,y):
		return self.getPosition(x,y)

	def getPosition(self,x,y):
		return [(self.position[0]+x)%(self.virtualWidth()),(self.position[1]+y)%(self.virtualHeight())]

	def randint(self,start,stop):
		if len(self.masterAnimation.random) > self.random:
			self.random += 1
			return self.masterAnimation.random[self.random-1]
		self.masterAnimation.random.append(randint(start,stop))
		self.random += 1
		return self.masterAnimation.random[self.random-1]

	def convertVirtualPosition(self,position):
		return self.masterAnimation.player.convertVirtualPosition(position)

class DoAsThread(Thread):
	def __init__(self,func,*args,**kwargs):
		Thread.__init__(self)
		self.func = func
		self.args = args
		self.kwargs = kwargs
		self.start()

	def run(self):
		try:
			self.func(*self.args,**self.kwargs)
		except KeyboardInterrupt:
			exit(2)

class Animation:
	def __init__(self,player,positions,field,fieldargs=[],vanish=True):
		self.fields = [field(self,positions[i],vanish,*fieldargs) for i in xrange(len(positions))]
		self.random = []
		self.player = player
		self.active = True

	def continueAnimations(self):
		while self.active:
			duration = 0
			for i in self.fields:
				duration = i.duration if i.duration > duration else duration
				DoAsThread(i.loadAnimation)
			sleep(duration)
			sleep(minimumsleep)

	def checkMatching(self):
		for i in self.fields:
			if i.covered:
				return False
		if not self.fields[0].vanish:
			DoAsThread(self.continueAnimations)
		else:
			for i in self.fields:
				DoAsThread(i.hide)
		return True

class Player:
	def __init__(self,width,height,xoffset,yoffset,fieldtypes=[],matching=2):
		self.matrix = [[None for x in xrange(height)] for y in xrange(width)]
		self.animations = []
		self.fieldtypes = fieldtypes #[fieldClass,[fieldargs],vanish]
		self.markedFields = []
		self.virtualWidth = width
		self.virtualHeight = height
		self.matching = matching
		self.marked = [0,0]
		self.fieldclicked = False
		self.xoffset = xoffset
		self.yoffset = yoffset

	def addFieldType(self,*fieldtypes):
		for i in fieldtypes:
			self.fieldtypes.append(i)

	def generateMemory(self):
		if not self.fieldtypes:
			raise ValueError("No Fieldtypes Given")
		fieldNumber = self.virtualWidth*self.virtualHeight/self.matching
		fields = [[x,y] for y in xrange(self.virtualHeight) for x in xrange(self.virtualWidth)]
		for i in xrange(fieldNumber):
			positions = []
			for j in xrange(self.matching):
				field = fields[randint(0,len(fields)-1)]
				fields.remove(field)
				positions.append(field)
			fieldtype = self.fieldtypes[randint(0,len(self.fieldtypes)-1)]
			self.animations.append(Animation(self,positions,fieldtype[0],fieldtype[1],fieldtype[2]))
			for j in self.animations[-1].fields:
				self.matrix[j.position[0]][j.position[1]] = j
		for i in xrange(len(self.matrix)):
			for j in xrange(len(self.matrix[i])):
				if not self.matrix[i][j]:
					self.matrix[i][j] = Field(None,None)
					self.matrix[i][j].covered = False

	def move(self,direction):
		self.changePosition(*{"up":(0,1),"down":(0,-1),"left":(-1,0),"right":(1,0)}[direction])

	def changePosition(self,x=0,y=0):
		self.setPosition([(self.marked[0]+x)%self.virtualWidth,(self.marked[1]+y)%self.virtualHeight])

	def uncover(self):
		self.markedFields.append(self.matrix[self.marked[0]][self.marked[1]])
		self.markedFields[-1].uncover()
		"""if len(self.markedFields) == self.matching:
			for i in self.markedFields:
				if i.checkMatching():
					self.markedFields = []
					break"""

	def action(self,act):
		if act == "click":
			self.click()
		elif act in ("up","down","left","right"):
			self.move(act)

	def click(self):
		if self.matrix[self.marked[0]][self.marked[1]].covered:
			self.fieldclicked = True
			self.uncover()
			done = True
			for i in self.matrix:
				for j in i:
					if j.covered:
						done = False
			if done:
				print "You Won!"

	def updateSingle(self,fition):
		if type(fition) == list:
			field = self.matrix[fition[0]][fition[1]]
		else:
			field = fition
		if field not in self.markedFields:
			if field.covered:
				field.cover()
			else:
				if field.vanish:
					field.hide()
				else:
					field.restUncoverColor()
		else:
			field.restUncoverColor()
		

	def initialPaint(self):
		for i in self.matrix:
			for j in i:
				j.cover()
				j.cover()

	def setPosition(self,position):
		#self.adjustedSend(self.marked,background,unmark_time)
		if len(self.markedFields) == self.matching:
			for i in self.markedFields:
				if i.checkMatching():
					break
				if i == self.markedFields[-1]:
					for i in self.markedFields:
						i.restUncover()
						i.cover()
			self.markedFields = []
		previous = self.matrix[self.marked[0]][self.marked[1]]
		self.marked = position
		self.adjustedSend(self.marked,marked,mark_time)
		#self.updateSingle(previous)
		previous.restUncover()

	def adjustedSend(self,position,rgb,fadet=0):
		send(self.convertVirtualPosition(position),rgb,fadet)

	def convertVirtualPosition(self,position):
		return [position[0]+self.xoffset,position[1]+self.yoffset]

class Handler:
	def __init__(self,playercount,width,height,fieldtypes=[],matching=2):
		self.players = []
		self.playercount = playercount
		self.matching = matching
		self.width = width
		self.height = height
		self.fieldtypes = fieldtypes
	
	def addFieldtypes(self,*fieldtypes):
		self.fieldtypes += fieldtypes

	def createPlayers(self):
		for i in xrange(self.playercount):
			self.players.append(Player(self.width/self.playercount,self.height,i*(self.width/self.playercount),0,self.fieldtypes,self.matching))

	def generateMemories(self):
		for i in self.players:
			i.generateMemory()

	def initialPaint(self):
		for i in self.players:
			i.initialPaint()

	def initiate(self):
		self.createPlayers()
		self.generateMemories()
		self.initialPaint()

	def somethingHappened(self,something,origin=0):
		self.players[origin].action(something)

def pygameInputHandler(handler):
	dic = {K_LEFT:"left",K_RIGHT:"right",K_UP:"up",K_DOWN:"down",K_RSHIFT:"click"}
	pygame.init()
	screen = pygame.display.set_mode((10,10))
	pygame.display.set_caption("Pygame Caption")
	pygame.mouse.set_visible(0)
	while 1:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key in dic:
					handler.somethingHappened(dic[event.key],1)
		sleep(0.05)

class SimpleMemoryField(Field):
	def __init__(self,masterAnimation,position,vanish=True):
		Field.__init__(self,masterAnimation,position,vanish)

	def loadAnimation(self):
		self.uncoverColor = [self.randint(0,255) for x in xrange(3)]
		self.adjustedSend(self.position,self.uncoverColor)

class AdvancedMemoryField(Field):
	def __init__(self,masterAnimation,position,vanish=True):
		Field.__init__(self,masterAnimation,position,vanish)

	def loadAnimation(self):
		for i in xrange(-1,2):
			for j in xrange(-1,2):
				self.adjustedSend(self.p(i,j),[self.randint(0,255) for x in xrange(3)])

class SimpleAnimationField(Field):
	def __init__(self,masterAnimation,position,vanish=True):
		Field.__init__(self,masterAnimation,position,vanish)

	def loadAnimation(self):
		for i in xrange(3):
			t = self.randint(0,2)
			self.adjustedSend(self.position,[self.randint(0,255) for x in xrange(3)],t)
			sleep(t)

if __name__ == "__main__":
	reset()
	simpleMemoryField = [SimpleMemoryField,[],True]
	advancedMemoryField = [AdvancedMemoryField,[],True]
	simpleAnimationField = [SimpleAnimationField,[],False]
	#handler = Handler(1,width/4,height,[[SimpleMemoryField,[],True]],2)
	handler = Handler(2,width,height,[simpleMemoryField,advancedMemoryField],2)
	#handler = Handler(1,width/2,height,[simpleAnimationField],2)
	#handler = Handler(1,width/2,height,[advancedMemoryField],2)
	handler.initiate()
	pygameInputHandler(handler)
	#r0ket_input.RoketInput(handler)
