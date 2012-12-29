import r0ketrem0te.game
from time import sleep

class Player:
	def __init__(self,rem,func):
		self.rem = rem
		self.rem.bridge.registerCallback(self.receivedPacket)
		self.player = None
		self.func = func

	def reveivedPacket(self,packet):
		if self.player == None:
			return None
		if packet.id == self.player.id:
			if isinstance(packet, r0ketrem0te.packets.Button):
				self.func(packet.button,self)

class RoketInput:
	def __init__(self,handler):
		self.handler = handler
		self.remote = r0ketrem0te.game.Game('/dev/ttyACM0',"memory",83,87,[ord(x) for x in 'REMOT'],2,True)
		self.remote.registerPlayerCallback(self.playercallback)
		self.players = []
		self.active = True
		self.getInput()

	def playercallback(self,action,player):
		if action == 'added':
			if len(self.players) < 2:
				self.players.append(Player(self.remote,self.playerInput))
				self.players[-1].player = player
			if len(self.players) == 2:
				self.getInput()
		elif action == "removed":
			for i in self.players:
				if i.player == player:
					self.players.remove(i)
					break

	def getInput(self):
		while self.active:
			try:
				print "blub"
				sleep(0.5)
			except KeyboardInterrupt:
				break

	def playerInput(self,button,player):
		dic = {0:"left",1:"right",2:"up",3:"down",4:"click"}
		self.handler.somethinghappened(dic[button],self.players.index(player))
