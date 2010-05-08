from twisted.internet.protocol import ServerFactory, Protocol
from twisted.conch.telnet import StatefulTelnetProtocol, TelnetTransport

import client, player

# factory - protocol class
# protocol/factory -> network class
# network -> game class
# Requests and callbacks go down in the list. 

class NetworkClass():
	
	def __init__(self):
		print "Starting up network server.."
		#self.protocol is the TYPE of protocol which gets created
		#it's only the function which gets called, not the actual protocol
		self.parent = 0
		self.child = ServerFactory()
		self.child.protocol = lambda: TelnetTransport(MyProtocol)
		self.protocol = self.child.protocol
		self.child.id = 1
		self.child.clList = { }
		self.child.parent = self
		self.clList = self.child.clList
		print "Factory, protocol and class initialisation done."
	
	#adaptations
	def getClient(self,id):
		return self.access.getClient(id)


	def newConnection(self,id):
		self.access.auth.plList[id] = player.PlayerClass(self.clList[id],"Agent00"+str(id))
		self.parent.greet(id)
	def disconnect(self,id):
		self.clList[id].transport.loseConnection()
	def sendLine(self,line,id=0):
		if id>0:
			self.clList[id].sendLine(line)
		else:
			for cl in self.clList:
				self.clList[cl].sendLine(line)
	def sendData(self,data,id):
		self.clList[id].transport.write(data)
	def lineReceived(self,line,id):
		self.getClient(id).active()
		err = self.parent.processChat(line,id)
		if err<0:
			self.sendLine("Please file a report with the admin. Fatal error.",id)
			self.sendLine("Err number: "+str(err))
		elif err==0:
			self.sendLine("No such command. Try 'help'?",id)
		self.sendData("> ",id)

class MyProtocol(StatefulTelnetProtocol):
	def connectionMade(self):
		print "Connection made to "+str(self.transport.getPeer()) +". "
		self.id = self.factory.id
		self.parent = self.factory.parent
		self.factory.id+=1
		self.factory.clList[self.id] = client.ClientClass(self)
		self.parent.newConnection(self.id)
	def lineReceived(self,line):
		print "Message received ("+str(self.id)+"): " + line
		self.parent.lineReceived(line.strip(),self.id)
		self.clearLineBuffer()
	def connectionLost(self,reason):
		print "Connection lost."
		del self.factory.clList[self.id]
	
	def enableRemote(self, option):
		return False
	def disableRemote(self, option):
		return False
	def enableLocal(self,option):
		return False
	def disableLocal(self,option):
		return False
