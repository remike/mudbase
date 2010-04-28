class RoomClass():
	
	def __init__(self,id,name,desc):
		self.id = id
		self.name = name
		self.desc = desc
		self.plList = {}
		self.itemList = {}

	def checkLink(self,name):
		return self.map.checkLink(self.id,name)
	
	def addItem(self,item):
		self.itemList[item.id] = item
		self.map.addItem(item,self.id)

	def emptyItems(self):
		self.itemList = { }

	def getItems(self):
		i = ""
		for id in self.itemList:
			i += self.itemList[id].name + ", "
		return i
	
	def getExits(self):
		return self.map.getExits(self.id)
	
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
	
	
	
