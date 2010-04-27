import sql,os,room

class MapClass():
	
	def __init__(self):
		self.roomList = {}
		
		os.chdir('sql')
		self.conn = sql.SQLClass('map')
		os.chdir('..')
		self.createRooms()
	
	def createRooms(self):
		c = self.conn.select('select id,name,desc from rooms order by id')
		for row in c:
			self.roomList[row[0]] = room.RoomClass(row[0],row[1],row[2])
			self.roomList[row[0]].map = self
	
	def checkLink(self,id,name):
		x = self.conn.select('select src, dest, name, desc from exits where src = ? and name = ?',[id,name])
		x = x.fetchone()
		if x!=None:
			return [x[1],x[3]]
		return 0
		
	def getExits(self,id):
		x = self.conn.select('select name from exits where src=? and obvious=1',[id])
		exitList = [ ]
		for exit in x.fetchall():
			exitList.append(exit[0])
		return exitList

	def getRooms(self):
		return self.roomList
	
	def getRoom(self,id):
		return self.roomList[id]
	
	def hasRoom(self,id):
		if id in self.roomList:
			return 1
		else: 
			return 0
	
	
	
