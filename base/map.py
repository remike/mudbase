import sql,os,room

class MapClass():
	
	def __init__(self):
		self.roomList = {}
		self.linkList = {}
		
		os.chdir('sql')
		self.conn = sql.SQLClass('map')
		os.chdir('..')
		self.createRooms()

	#adaptations
	def getRooms(self):
		return self.access.getRooms()
	def getRoom(self,id):
		return self.access.getRoom(id)
	
	def createRooms(self):
		c = self.conn.select('select id,name,desc from rooms order by id')
		self.roomList = {}
		for row in c:
			self.roomList[row[0]] = room.RoomClass(row[0],row[1],row[2])
			self.roomList[row[0]].map = self
	
	def createLinks(self):
		#FIXME need to add link class
		c = self.conn.select('select id,src,dest,name,desc,obvious from exits order by id')
		self.linkList = {}
		for row in c:
			self.linkList[row[0]] = [id,src,dest,name,desc,obvious]

	#FIXME v this
	def createRoom(self,origin,name,desc,exitName,exitDesc,exitObvious,twoWay):
		self.conn.execute('insert into rooms (name,desc) values (?,?)',[name,desc])
		self.createRooms()
		self.createLink(origin,len(self.roomList)-1,exitName,exitDesc,exitObvious,twoWay)
		
	def createLink(self,src,dest,name,desc,obvious,twoWay):
		self.conn.execute('insert into exits (src,dest,name,desc,obvious) values(?,?,?,?,?)',
			[src,dest,name,desc,obvious])
		if twoWay:
			self.conn.execute('insert into exits (src,dest,name,desc,obvious) values(?,?,?,?,?)',
			[dest,src,name,desc,obvious])

	def removeRoom(self,roomID):
		self.conn.execute("delete from rooms where id = ?",[roomID])
		self.conn.execute("delete from exits where src = ? or dest = ?",[roomID,roomID])
		players = self.map.auth.conn.select("select id from players where room = ?",[roomID])
		for row in players.fetchall():
			self.access.auth.plantPlayer(row[0])
		print "Room deleted."
	#FIXME ^ this
					
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
	
	def hasRoom(self,id):
		if id in self.getRooms():
			return 1
		else: 
			return 0
	
	
	
