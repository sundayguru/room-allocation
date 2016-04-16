import sqlite3
from os import path
from datetime import datetime

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
		#this will allow us to access the query result via the column name
		self.connection.row_factory = sqlite3.Row


	def execute(self, sql, params = {}, commit = False):
		"""executes sql and return the query result if successful or bool if failed"""
		try:
			result =  self.connection.execute(sql,params)
			if commit:
				self.connection.commit()
			return result
		except sqlite3.OperationalError, message:
			self.errormessage = message
			return False

	def find(self,id):
		result =  self.execute("SELECT *  from " + self.table_name + ' WHERE id = ' + str(id))
		if result:
			return result.fetchone()[0]
		else:
			return False

	def findall(self):
		result = self.execute("SELECT *  from " + self.table_name)
		if result:
			return result.fetchall()
		else:
			return False

	def findbyattr(self,attributes):
		pass

	def create(self,data):
		data['date_time'] = datetime.now()
		resolved = self.prepare(data)
		sql = 'INSERT INTO '+self.table_name+' ('+resolved['column']+') VALUES ('+resolved['place_holders']+')'
		return self.execute(sql,data,True)
		
      

	def prepare(self,data):
		columns = ''
		place_holders = '';
		columnvalue = {}
		for key,value in data.items():
			columns += key + ','
			place_holders += ":" + str(key) + ","
		columnvalue['column'] = columns[:-1]
		columnvalue['place_holders'] = place_holders[:-1]
		return columnvalue

	def update(self,data):
		pass
