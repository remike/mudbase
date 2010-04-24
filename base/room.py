class RoomClass():
	
	def __init__(self,id,name,desc):
		self.id = id
		self.name = name
		self.desc = desc
		self.plList = {}
	
	def getName(self):
		return self.name

	def addPlayer(self,pl):
		self.plList[pl.id] = pl
	
	def removePlayer(self,id):
		del self.plList[id]

	def getPlayer(self,id):
		return self.plList[id]

	def getPlayers(self):
		return self.plList
	
	def getDescription(self):
		#TODO	add other stuff in descriptions
		return self.desc
	
	
	
