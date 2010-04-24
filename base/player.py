class PlayerClass():
	
	def __init__(self,client,name):
		self.client = client
		self.name = name
		self.id = self.client.id
	
	def getName(self):
		return self.name

	def rename(self,name):
		self.name = name

	def disconnect(self,reason):
		self.client.disconnect(reason)		
	
	def sendLine(self,line):
		self.client.sendLine(line)
	
	
	
