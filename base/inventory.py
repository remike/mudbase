import item

class InventoryClass():
	
	def __init__(self):
		self.itemList = { }
	
	def addItem(self,item):
		self.itemList[item.id] = item.Item(
