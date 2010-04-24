from twisted.internet import reactor, task
import network

class GameClass():
	
	plList = {}
	commands = ["help", "exit", "go north", "hosts", "players", "rename" ]

	def __init__(self):
		print "- Core init start."
		print "- Network init."
		self.network = network.NetworkClass()
		self.network.parent = self
		fact = self.network.child
		print "- Done."
		print "---- Core init done."
		reactor.listenTCP(8023,fact)
		self.schedule = task.LoopingCall(self.idleTest)
		self.schedule.start(60.0)
		reactor.run()
	
	def idleTest(self):
		for id in self.plList:
			self.getClient(id).idleOut()
	
	def getPlayer(self,id):
		return self.plList[id]
	
	def getClient(self,id):
		return self.plList[id].client
	
	def getTransport(self,id):
		return self.getClient(id).transport
	
	def processChat(self,line,id=-1):
		if line.startswith("@"):
			self.globalChat(line[1:],id)
			return 1
		else:
			return self.checkCommand(line,id)
	
	def checkCommand(self,line,id=-1,run=1):
		#FIXME remove this hacky fix
		l = ["a","a"]
		if line.count(" ")>0:
			l = line.split(" ",1)
		if line in self.commands or l[0] in self.commands:
			if run:
				return self.doCommand(line,id)
			else:
				return 0
		else:
			return 0	
	
	def doCommand(self,line,id):
		if line == "help":
			self.sendLine("Welcome.",id)
			self.sendLine("'@message' will broadcast 'message' globally to all connected clients.",id)
			self.sendLine("Use 'rename New Name Here' to rename yourself.",id)
			self.sendLine("The command 'hosts' will list all connected clients and their ips.",id)
			self.sendLine("The command 'players' will only list the player names.",id)
			self.sendLine("You can quit with 'exit'",id)
		elif line == "exit":
			self.sendLine("Goodbye.",id)
			self.disconnect(id)
		elif line == "hosts":
			self.printHosts(id)
		elif line == "players":
			self.printPlayers(id)
		elif line.startswith("rename"):
			self.renamePlayer(line,id)

		elif line == "go north":
			self.sendLine("You're in a room full of passages, all alike.",id)
		return 1
	
	def printPrompt(self,id):
		self.network.sendData("> ",id)
	
	def sendLine(self,line,id):
		self.network.sendLine(line,id)
		
	def disconnect(self,id):
		#cleanup here TODO
		self.sendLine("User #"+str(id)+" ("+self.getPlayer(id).name+") has disconnected.",0)
		del self.plList[id]
		self.network.disconnect(id)
	
	def renamePlayer(self,line,id):
		if line.count(" ")>0:
			l = line.split(" ",1)
			self.sendLine(self.getPlayer(id).name + " is now known as " + l[1] + ".",-1)
			self.getPlayer(id).rename(l[1])
	
	def printHosts(self,id=-1):
		if id!=-1:
			for pl in self.plList:
				x = str(pl) + " - "
				x = self.getPlayer(pl).name + " - "
				x += self.getClient(pl).ip
				self.sendLine(x,id)
			self.sendLine("----",id)
		else:
			for cl in self.clList:
				print str(cl) + " - " + self.getClient(cl).ip
			print "----"

	def printPlayers(self,id=-1):
		self.sendLine("There are "+str(len(self.plList))+" players online at the moment.",id)
		for pl in self.plList:
			self.sendLine("  "+self.getPlayer(pl).name,id)
		self.sendLine("----",id)

	
	def globalChat(self,line,id):
		prcLine = "Global message from "+self.getPlayer(id).getName()+": "+line
		self.sendLine(prcLine,-1)
	
	def greet(self,id):
		self.doCommand("help",id)
		self.sendLine("Everyone, please welcome user #"+str(id)+".",0)
		self.printPrompt(id)

