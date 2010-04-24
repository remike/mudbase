from twisted.internet.protocol import ServerFactory, Protocol
from twisted.conch.telnet import StatefulTelnetProtocol, TelnetTransport
from twisted.internet import reactor
from twisted.application.internet import TCPServer
from twisted.application.service import Application

from time import sleep


# factory - protocol class
# protocol/factory -> network class
# network -> game class
# Requests and callbacks go down in the list. 

class NetworkClass():

	
	commands = ["help", "exit", "go north", "hosts" ]

	def __init__(self):
		print "Starting up network server.."
		#self.protocol is the TYPE of protocol which gets created
		#it's only the function which gets called, not the actual protocol
		self.child = ServerFactory()
		self.child.protocol = lambda: TelnetTransport(MyProtocol)
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
	def sendData(self,data,id):
		self.clList[id].transport.write(data)
	def lineReceived(self,line,id):
		if line not in self.commands:
			if line.startswith("@") == False:
				self.clList[id].sendLine("Unrecognised command. Try 'help'?")
			else:
				for cl in self.clList:
					if cl != id:
						self.clList[cl].sendLine("GLOBAL( "+str(id)+" ): " + line[1:])	
			self.sendData("> ",id)
		else:
			if line == "exit":
				self.clList[id].sendLine("Killed.")
				print "Client killed."
				self.disconnect(id)
			elif line == "help":
				self.sendLine("Welcome.",id)
				self.sendLine("'@message' will broadcast 'message' globally to all connected clients.",id)
				self.sendLine("The command 'hosts' will list all connected clients and their ips.",id)
				self.sendLine("You can quit with 'exit'",id)
			elif line == "hosts":
				for cl in self.clList:
					x = str(cl) + " - "
					x += str(self.clList[cl].transport.getPeer())
					self.sendLine(x,id)
				self.sendLine("----",id)
			elif line == "go north":
				self.sendLine("Sorry, not yet. ;)",id)
			self.sendData("> ",id)

class MyProtocol(StatefulTelnetProtocol):
	def connectionMade(self):
		print "Connection made."
		self.sendLine("Welcome.")
		self.sendLine("Do '@message' to output message to all connected clients.")
		self.sendLine("'exit' to quit.")
		self.transport.write("> ")
		self.clearLineBuffer()
		self.id = self.factory.id
		self.factory.id+=1
		self.factory.clList[self.id] = self
		self.parent = self.factory.parent
	def lineReceived(self,line):
		print "Message received: " + line
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



if __name__=="__main__":
	net = NetworkClass()
	fact = net.child
	reactor.listenTCP(8023,fact)
	reactor.run()
