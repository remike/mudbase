import item

class InventoryClass():

	curID = 1
	
	def __init__(self):
		self.itemList = { }
	
	def addItem(self,name,desc,weight):
		self.itemList[self.curID] = item.ItemClass(self.curID,name,desc,weight)
		self.curID += 1
		return self.curID-1
	
	def getItem(self,id):
		return self.itemList[id]
