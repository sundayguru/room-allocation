import sqlite3

class Db(object):
	"""Database manipulation"""
	name = 'amity'
	table_name = 'table_name'

	def __init__(self,dbname = 'amity',table_name = 'table_name'):
		self.name = dbname
		self.table_name = table_name
		self.connection = sqlite3.connect(self.name+'.db')


	def execute(self,sql):
		return self.connection.execute(sql)

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

