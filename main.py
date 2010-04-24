from twisted.internet.protocol import ServerFactory, Protocol
from twisted.conch.telnet import StatefulTelnetProtocol
from twisted.internet import reactor

from time import sleep

# factory - protocol class
# protocol/factory -> network class
# network -> game class
# Requests and callbacks go down in the list.
# 

class NetworkClass():
	def __init__(self):
		print "Starting up network server.."
		self.child = ServerFactory()
		self.child.protocol = MyProtocol
		self.protocol = self.child.protocol
		self.child.id = 1
		self.child.clList = { }
		self.child.parent = self
		self.clList = self.child.clList
		print "Factory, protocol and class initialisation done."
	def disconnect(self,id):
		self.clList[id].transport.loseConnection()
	def sendLine(self,line,id):
		self.clList[id].sendLine(line)
	def lineReceived(self,line,id):
		if line != "exit":
			if line[0]!="@":
				self.clList[id].sendLine("local: " + line)
			else:
				for cl in self.clList:
					if cl != id:
						self.clList[cl].sendLine("GLOBAL( "+id+" ): " + line)	
		else:
			self.clList[id].sendLine("Killed.")
			print "Client killed."
			self.disconnect(id)

class MyProtocol(StatefulTelnetProtocol):
	def connectionMade(self):
		print "Connection made."
		self.sendLine("Welcome.")
		self.sendLine("Do '@message' to output message to all connected clients.")
		self.sendLine("'exit' to quit.")
		self.clearLineBuffer()
		self.id = self.factory.id
		self.factory.id+=1
		self.factory.clList[self.id] = self
		self.parent = self.factory.parent
	def lineReceived(self,line):
		print "Message received: " + line
		print self.id
		self.parent.lineReceived(line.strip(),self.id)
		self.clearLineBuffer()
	def connectionLost(self,reason):
		print "Connection lost."


if __name__=="__main__":
	net = NetworkClass()
	fact = net.child
	reactor.listenTCP(8023,fact)
	reactor.run()
