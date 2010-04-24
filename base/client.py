import time

class ClientClass():
	
	def __init__(self,protocol):
		self.connection = protocol
		self.transport = self.connection.transport
		self.factory = self.connection.factory
		self.id = self.connection.id
		self.ip = self.transport.getPeer().host
		self.idleTime = time.time()

	def active(self):
		self.idleTime = time.time()	

	def idleOut(self):
		if time.time() - self.idleTime > 300:
			self.disconnect("Idled out.")

	def disconnect(self,reason):
		self.sendLine("Disconnected: "+reason)	
		self.parent.disconnect(id)	
	
	def sendLine(self,line):
		self.connection.sendLine(line)
	
	
	
