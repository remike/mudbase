import network,map,auth,parser

class AccessClass():
	
	def __init__(self,parent):
		self.game = parent
		self.parent = parent
		print "--- Network init."
		self.network = network.NetworkClass()
		self.network.parent = self.parent
		self.network.access = self
		print "--- Done."
		print "--- Map init."
		self.map = map.MapClass()
		self.map.parent = self.parent
		self.map.access = self
		
		print "--- Done."
		print "--- Auth init."
		self.auth = auth.AuthClass()
		self.auth.parent = self.parent
		self.auth.access = self
		print "--- Done."
		print "--- Parser init."
		self.parser = parser.ParserClass()
		self.parser.parent = self.parent
		self.parser.access = self
		print "--- Done."

	#game.py
	def getPlayer(self,id):
		return self.parent.plList[id]
	def getClient(self,id):
		return self.parent.plList[id].client
	def getTransport(self,id):
		return self.parent.plList[id].client.transport
	def sendLine(self,line,id):
		self.network.sendLine(line,id)

	#auth.py
	def getUserInfo(self,id):
		return self.auth.userInfo[id]
	def getUser(self,id):
		return self.auth.userList[id]
	def getUsers(self):
		return self.auth.userList
	def renamePlayer(self,name,id):
		self.auth.renamePlayer(name,id)

	
