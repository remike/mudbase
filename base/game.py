from twisted.internet import reactor
import network

class GameClass():
	
	clList = {}
	commands = ["help", "exit", "go north", "hosts" ]

	def __init__(self):
		print "- Core init start."
		print "- Network init."
		self.network = network.NetworkClass()
		self.network.parent = self
		self.clList = self.network.clList
		fact = self.network.child
		print "- Done."
		print "---- Core init done."
		reactor.listenTCP(8023,fact)
		reactor.run()

	
	def getClient(self,id):
		return self.clList[id]
	
	def getTransport(self,id):
		return self.clList[id].transport
	
	def processChat(self,line,id=-1):
		if line.startswith("@"):
			self.globalChat(line[1:],id)
			return 1
		else:
			return self.checkCommand(line,id)
	
	def checkCommand(self,line,id=-1,run=1):
		if line in self.commands:
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
			self.sendLine("The command 'hosts' will list all connected clients and their ips.",id)
			self.sendLine("You can quit with 'exit'",id)
		elif line == "exit":
			self.sendLine("Goodbye.",id)
			self.disconnect(id)
		elif line == "hosts":
			self.printHosts(id)
		elif line == "go north":
			self.sendLine("Soon, young padawan.",id)
		return 1
	
	def printPrompt(self,id):
		self.network.sendData("> ",id)
	
	def sendLine(self,line,id):
		self.network.sendLine(line,id)
		
	def disconnect(self,id):
		#cleanup here TODO
		self.sendLine("User #"+str(id)+" has disconnected.",0)
		self.network.disconnect(id)
	
	def printHosts(self,id=-1):
		if id!=-1:
			for cl in self.clList:
				x = str(cl) + " - "
				x += str(self.getTransport(id).getPeer())
				self.sendLine(x,id)
			self.sendLine("----",id)
		else:
			for cl in self.clList:
				print str(cl) + " - " + str(self.getTransport(cl).getPeer())
			print "----"
	
	def globalChat(self,line,id):
		prcLine = "Global message from ("+str(id)+"): "+line
		self.sendLine(prcLine,-1)
	
	def greet(self,id):
		self.doCommand("help",id)
		self.sendLine("Everyone, please welcome user #"+str(id)+".",0)
		self.printPrompt(id)

