import sql,os,room,md5,user

class AuthClass():
	
	def __init__(self):
		self.userList = {}
		
		os.chdir('sql')
		self.conn = sql.SQLClass('users')
		os.chdir('..')
	
	def greetUser(self,id):
		self.userList[id] = user.UserClass(id)
	
	def renamePlayer(self,name,id):
		if id in self.parent.userList:
			x = self.conn.execute('update players set name = ? where id = ?', [name,self.parent.userList[id][1]])
			return 1
		return 0
	
	def userConnected(self,id,name,password):
		#id = hostID
		if id not in self.parent.userList:
			x = md5.new(password)
			password = x.hexdigest()
			info = self.conn.select('select id, name, playerID from users where name = ? and pass = ?',[name,password]).fetchone()
			if info!=None:
				pInfo = self.conn.select('select id, name from players where id = ?',[info[2]]).fetchone()
				if pInfo!=None:
					self.associateUser(id,info[0],info[1],pInfo[0],pInfo[1])
					self.parent.sendLine("Successfully logged in.",id)
					return 1
			self.parent.sendLine("Login failed. Wrong username/password.",id)
			return 1
		self.parent.sendLine("Already logged in.",id)		
		return 1

	def userRegister(self,id,name,password):
		#id = hostID
		if id not in self.parent.userList:
			x = md5.new(password)
			passwordMd5 = x.hexdigest()
			info = self.conn.select('select id, name, playerID from users where name = ? and pass = ?',[name,passwordMd5]).fetchone()
			if info==None:
				self.conn.execute('insert into users (name, pass) values(?,?)',[name,passwordMd5])
				self.conn.execute('insert into players (name) values(?)',[self.parent.getPlayer(id).name])
				x = self.conn.select('select id from players where name=?',[self.parent.getPlayer(id).name]).fetchone()
				self.conn.execute('update users set playerID = ? where name = ? and pass = ?',[x[0],name,passwordMd5])
				self.parent.sendLine("Successfully registered.",id)
				self.userConnected(id,name,password)
				return 1
			self.parent.sendLine("Register failed.",id)
			return 1
		self.parent.sendLine("Already logged in.",id)		
		return 1
	
	def associateUser(self,hostID,userID,userName,playerID,playerName):
		self.parent.userList[hostID]=[userID,playerID]
		self.parent.renamePlayer(playerName,hostID)
		print "Logged in user #"+str(userID)
		
