from twisted.internet import reactor, task
import network,map,auth,parser

class GameClass():
	
	plList = {}
	userList = {}

	def __init__(self):
		print "- Core init start."
		print "- Network init."
		self.network = network.NetworkClass()
		self.network.parent = self
		fact = self.network.child
		print "- Done."
		print "- Map init."
		self.map = map.MapClass()
		self.map.parent = self
		print "- Done."
		print "- Auth init."
		self.auth = auth.AuthClass()
		self.auth.parent = self
		print "- Done."
		print "- Parser init."
		self.parser = parser.ParserClass()
		self.parser.parent = self
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
		success = self.getPlayer(id).tryMove(line)
		if not success:
			return self.checkCommand(line,id)
		return 1
	
	def checkCommand(self,line,id=-1,run=1):
		line = self.parser.processLine(line)
		if line:
			verb = line[0]
			modifiers = line[1]
			return self.doCommand(verb,modifiers,id)
		else:
			return 0
	
	def doCommand(self,verb,modifiers,id):
		#FIXME eventually need to rewrite this

		if self.auth.checkUser(id) == 1:
			if verb == "hosts":
				self.printHosts(id)
			elif verb == "players":
				self.printPlayers(id)
			elif verb == "rename":
				self.renamePlayer(" ".join(modifiers),id)
			elif verb == "status":
				self.getPlayer(id).status()
			elif verb == "say":
				self.globalChat(" ".join(modifiers),id)	
			elif verb == "exit":
				self.disconnect(id)
			elif verb == "help":
				self.printHelp(id)
			elif verb == "look":
				self.getPlayer(id).look()

			#FIXME v this
			#wizard create room here Room1 Room1desc LinkName LinkDescription 1 1
			elif verb == "wizard" and modifiers[0] == "create" and modifiers[1] == "room":
				#self.map.createRoom(origin,name,desc,exitName,exitDesc,exitObvious,twoWay
				if modifiers[2] == "here":
					origin = self.getPlayer(id).room.id
				else:
					origin = modifiers[2]
				self.map.createRoom(origin,modifiers[3],modifiers[4],modifiers[5],
					modifiers[6],modifiers[7],modifiers[8])
				return 1
			elif verb == "wizard" and modifier[0] == "delete" and modifiers[1] == "room":
				self.map.deleteRoom(int(modifiers[2]))
			#FIXME ^ this
		else:
			if verb == "help":
				self.printHelp(id)
			elif verb == "exit":
				self.disconnect(id)
			elif verb == "auth":
				return self.auth.userConnected(id,modifiers[0],modifiers[1])
			elif verb == "register":
				return self.auth.userRegister(id,modifiers[0],modifiers[1])
			elif verb == "look":
				self.getPlayer(id).look()
			else:
				self.sendLine("You must be registered to use this command.",id)
		return 1


	def printHelp(self,id):
		self.sendLine("Welcome.",id)
		self.sendLine("'say message' will broadcast 'message' globally to all connected clients.",id)
		self.sendLine("'auth username password' to log in.",id)
		self.sendLine("'register username password' to register an account.",id)
		self.sendLine("Use 'rename New Name Here' to rename yourself after logging in or registering.",id)
		self.sendLine("The command 'hosts' will list all connected clients and their ips. Registered users only.",id)
		self.sendLine("The command 'players' will only list the player names. Registered users only.",id)
		self.sendLine("You can quit with 'exit'.",id)	
		self.sendLine("wizard create room here Room1 Room1desc LinkName LinkDescription 1 1",id)

	def printPrompt(self,id):
		self.network.sendData("> ",id)
	
	def sendLine(self,line,id):
		self.network.sendLine(line,id)
		
	def disconnect(self,id):
		#cleanup here TODO
		self.sendLine("Goodbye.",id)
		self.sendLine("User #"+str(id)+" ("+self.getPlayer(id).name+") has disconnected.",0)
		del self.plList[id]
		if id in self.userList:
			del self.userList[id]
		self.network.disconnect(id)
	
	def renamePlayer(self,line,id):
		if self.getPlayer(id).name != line:
			x = self.auth.renamePlayer(line,id)
			if x:
				self.sendLine(self.getPlayer(id).name + " is now known as " + line + ".",-1)
				self.getPlayer(id).rename(line)
				return 1
			self.sendLine("Rename failed. Login first?",id)
	
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
		self.getPlayer(id).parent = self
		self.map.getRoom(0).addPlayer(self.getPlayer(id))
		self.getPlayer(id).room = self.map.getRoom(0)
		self.doCommand("help",[],id)
		self.sendLine("Everyone, please welcome user #"+str(id)+".",0)
		self.getPlayer(id).look()
		self.printPrompt(id)

