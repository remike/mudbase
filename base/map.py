import sql,os,room

class MapClass():
	
	def __init__(self):
		self.roomList = {}
		
		os.chdir('sql')
		self.conn = sql.SQLClass('map')
		os.chdir('..')
		self.createRooms()
	
	def createRooms(self):
		c = self.conn.select('select * from rooms order by id')
		for row in c:
			self.roomList[row[0]] = room.RoomClass(row[0],row[1],row[2])
			

	def getRooms(self):
		return self.roomList
	
	def getRoom(self,id):
		return self.roomList[id]
	
	
	
