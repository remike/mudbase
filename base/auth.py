import sql,os,room,md5,user

class AuthClass():
	
	# NOTE:
	# userList = users registered and logged-in in THIS auth instance
	# playerList = players connected (from a user)
	# userInfo = list of hostID = [userID,playerID]
	#
	
	def __init__(self):
		self.userList = {}
		self.userInfo = {}
		
		os.chdir('sql')
		self.conn = sql.SQLClass('users')
		os.chdir('..')

	#adaptations
	def getUser(self,id):
		return self.access.getUser(id)
	def getUsers(self):
		return self.access.getUsers()
	def getUserInfo(self,id):
		return self.access.getUserInfo(id)
	def getPlayer(self,id):
		return self.access.getPlayer(id)
	def sendLine(self,line,id):
		self.access.sendLine(line,id)

	def plantPlayer(self,id):
		list = self.conn.select('select room from players where id = ?',[self.getUserInfo(id)[1]]).fetchone()
		if self.parent.map.hasRoom(list[0]):
			self.getPlayer(id).movePlayer(list[0],'You feel yourself fading out, then back in.')
		else:
			self.getPlayer(id).movePlayer(1,'You feel yourself fading out, then back in.')
	
	def greetUser(self,id):
		self.userList[id] = user.UserClass(id)
		self.getPlayer(id).parent = self
		self.plantPlayer(id)
	
	def renamePlayer(self,name,id):
		if self.getPlayer(id).name != name:
			if id in self.getUsers():
				x = self.conn.execute('update players set name = ? where id = ?', [name,self.getUserInfo(id)[1]])
				if x:
					self.sendLine(self.getPlayer(id).name + " is now known as " + name + ".",-1)
					self.getPlayer(id).rename(name)
					return 1
		self.sendLine("Rename failed. Login first?",id)	
		return 0
	
	def userConnected(self,id,name,password):
		#id = hostID
		if id not in self.getUsers():
			x = md5.new(password)
			password = x.hexdigest()
			info = self.conn.select('select id, name, playerID from users where name = ? and pass = ?',[name,password]).fetchone()
			if info!=None:
				pInfo = self.conn.select('select id, name from players where id = ?',[info[2]]).fetchone()
				if pInfo!=None:
					self.associateUser(id,info[0],info[1],pInfo[0],pInfo[1])
					self.sendLine("Successfully logged in.",id)
					return 1
			self.sendLine("Login failed. Wrong username/password.",id)
			return 1
		self.sendLine("Already logged in.",id)		
		return 1

	def userRegister(self,id,name,password):
		#id = hostID
		if id not in self.getUsers():
			x = md5.new(password)
			passwordMd5 = x.hexdigest()
			info = self.conn.select('select id, name, playerID from users where name = ? and pass = ?',[name,passwordMd5]).fetchone()
			if info==None:
				self.conn.execute('insert into users (name, pass) values(?,?)',[name,passwordMd5])
				self.conn.execute('insert into players (name) values(?)',[self.getPlayer(id).name])
				x = self.conn.select('select id from players where name=?',[self.getPlayer(id).name]).fetchone()
				self.conn.execute('update users set playerID = ? where name = ? and pass = ?',[x[0],name,passwordMd5])
				self.sendLine("Successfully registered.",id)
				self.userConnected(id,name,password)
				return 1
			self.sendLine("Register failed.",id)
			return 1
		self.sendLine("Already logged in.",id)		
		return 1
	
	def associateUser(self,hostID,userID,userName,playerID,playerName):
		self.userInfo[hostID]=[userID,playerID]
		self.renamePlayer(playerName,hostID)
		self.greetUser(hostID)
		print "Logged in user #"+str(userID)
	
	def checkUser(self,id):
		if id not in self.getUsers():
			return 0
		else:
			return 1
		
