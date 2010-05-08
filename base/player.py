class PlayerClass():
	
	def __init__(self,client,name):
		self.parent = 0
		self.room = 0
		self.client = client
		self.name = name
		self.id = self.client.id

	#adaptations
	def sendLine(self,line,id):
		self.parent.sendLine(line,id)
	def getUserInfo(self,id):
		return self.parent.getUserInfo(id)
	
	def getName(self):
		return self.name

	def status(self):
		self.sendLine("You remember you're called "+self.name+".",self.id)
		self.look()

	def look(self):
		self.sendLine("     "+self.room.name,self.id)
		self.sendLine(self.room.desc,self.id)
		exitList = self.room.getExits()
		if exitList != []:
			self.sendLine("You see the following exits: " + ', '.join(exitList),self.id)

	def tryMove(self,name):
		#x[0] = id of the dest room
		#x[1] = description of road
		x = self.room.checkLink(name)
		if x:
			self.movePlayer(x[0],x[1])
			return 1		
		return 0	

	def movePlayer(self,destID,text=0):
		self.room.removePlayer(self.id)
		self.parent.access.map.getRoom(destID).addPlayer(self)
		self.room = self.parent.access.map.getRoom(destID)
		if text:
			self.sendLine(text,self.id)
		if destID != 0:
			self.parent.access.auth.conn.execute('update players set room = ? where id = ?',[destID,self.getUserInfo(self.id)[1]])
		self.look()

	def rename(self,name):
		self.name = name

	def disconnect(self,reason):
		self.access.auth.conn.execute('update players set room = ? where id = ?',
			[self.room.id,self.getUserInfo(self.id)[1]])
		self.client.disconnect(reason)		
	
