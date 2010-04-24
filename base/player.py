class PlayerClass():
	
	def __init__(self,client,name):
		self.parent = 0
		self.room = 0
		self.client = client
		self.name = name
		self.id = self.client.id
	
	def getName(self):
		return self.name

	def look(self):
		self.parent.sendLine("You remember you're called "+self.name+".",self.id)
		self.parent.sendLine("     "+self.room.name,self.id)
		self.parent.sendLine(self.room.desc,self.id)
		

	def rename(self,name):
		self.name = name

	def disconnect(self,reason):
		self.client.disconnect(reason)		
	
	def sendLine(self,line):
		self.client.sendLine(line)
	
	
	
