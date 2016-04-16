import sqlite3
from os import path

class Db(object):
	"""Database manipulation"""

	name = 'amity'
	table_name = 'table_name'
	errormessage = ''

	def __init__(self,dbname = 'amity',table_name = 'table_name'):
		self.name = dbname
		self.table_name = table_name
		root = path.dirname(path.dirname(path.abspath(__file__)))
		db_location = root+'/'+self.name+'.db'
		self.connection = sqlite3.connect(db_location)


	def execute(self,sql,commit = False):
		"""executes sql and return the query result if successful or bool if failed"""
		try:
			result =  self.connection.execute(sql)
			if commit:
				self.connection.commit()
			return result
		except sqlite3.OperationalError, message:
			self.errormessage = message
			return False

	def find(self,id):
		try:
			return self.execute("SELECT *  from "+table_name+' WHERE id = '+id)
		except:
			return False

	def findall(self):
		try:
			return self.execute("SELECT *  from "+table_name)
		except:
			return False

	def findbyattr(self,attributes):
		pass

	def create(self,data):
		resolved = self.prepare(data)
		sql = 'INSERT INTO '+self.table_name+' ('+resolved['column']+') VALUES ('+resolved['value']+')'
		return self.execute(sql,True)
		
      

	def prepare(self,data):
		columns = ''
		values = ''
		columnvalue = {}
		for key,value in data.items():
			columns += key + ','
			values += "'" + str(value) + "',"
		columnvalue['column'] = columns[:-1]
		columnvalue['value'] = values[:-1]
		return columnvalue

	def update(self,data):
		pass
