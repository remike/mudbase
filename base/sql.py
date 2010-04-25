import sqlite3

class SQLClass():
	
	def __init__(self,path):
		self.conn = sqlite3.connect(path)
		self.conn.text_factory = str
		self.cur = self.conn.cursor()

	def execute(self,line,var):
		self.cur.execute(line,var)
		self.conn.commit()
	
	def select(self,line,var=0):
		if var:
			self.cur.execute(line,var)
		else:
			self.cur.execute(line)
		return self.cur
	
	
	
