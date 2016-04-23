import sqlite3
from os import path
from datetime import datetime

class Db(object):
	"""Sqlite3 database manipulation"""

	name = 'amity'
	table_name = 'table_name'
	error_message = ''

	def __init__(self,db_name = 'amity',table_name = 'table_name'):
		self.name = db_name
		self.table_name = table_name
		self.set_db(db_name)
		
	def set_db(self,name = 'amity'):
		root = path.dirname(path.dirname(path.abspath(__file__)))
		self.db_location = root+'/'+name+'.db'

	def __db_open(self):
		"""creates sqlite database connection"""
		self.connection = sqlite3.connect(self.db_location)
		#this will allow us to access the query result via the column name
		self.connection.row_factory = sqlite3.Row

	def __db_close(self):
		"""closes sqlite database connection"""
		self.connection.close()

	def execute(self, sql, params = {}, commit = False):
		"""executes sql and return the query result if successful or bool if failed"""
		try:
			self.__db_open()
			result =  self.connection.execute(sql,params)
			if commit:
				self.connection.commit()
			return result
		except sqlite3.OperationalError, message:
			self.error_message = message
			return False

	def find(self,id):
		"""returns a row in a given table if the id exists"""
		cursor =  self.execute("SELECT *  from " + self.table_name + ' WHERE id = ' + str(id))
		if cursor:
			result = cursor.fetchone()
			self.__db_set_attr(result)	
		else:
			result =  False
		self.__db_close()
		return result

	def find_all(self):
		"""returns all records in a given table"""
		cursor = self.execute("SELECT *  from " + self.table_name)
		if cursor:
			result = cursor.fetchall()
		else:
			result = False
		self.__db_close()
		return result

	def find_by_attr(self,attributes,logic = 'AND'):
		"""returns matching results based on """
		where_clause = self.prepare_attr(attributes,logic)
		cursor = self.execute("SELECT *  from " + self.table_name + " WHERE " + where_clause,attributes)
		if cursor:
			result = cursor.fetchall()
		else:
			result = False
		self.__db_close()
		return result

	def create(self,data):
		"""adds new row to the database based on table_name"""
		data['date_time'] = datetime.now()
		resolved = self.prepare_insert(data)
		sql = 'INSERT INTO ' + self.table_name + ' (' + resolved['column'] + ') VALUES (' + resolved['place_holders'] + ')'
		return self.execute(sql,data,True)
		

	def prepare_insert(self,data):
		"""returns dict of columns separated in comma and value place holders separated with comma"""
		columns = ''
		place_holders = '';
		column_value = {}
		for key in data:
			columns += key + ','
			place_holders += ":" + str(key) + ","
		column_value['column'] = columns[:-1]
		column_value['place_holders'] = place_holders[:-1]
		return column_value

	def prepare_attr(self,data,logic):
		"""returns a condition statement to be used in querying database"""
		where_clause = '';
		for key in data:
			where_clause += key + ' = :' + str(key) + " " + logic + ' '
		return where_clause[:-(len(logic) + 2)]

	def prepare_update(self,data):
		"""returns combination of keys and place holder values for update method"""
		set_data = '';
		for key in data:
			if key == 'id':
				continue
			set_data += key + ' = :' + str(key) + "," 
		# -1 removes the last comma
		return set_data[:-1]

	def __db_set_attr(self,result):
		"""dynamic sets properties based on returned result"""
		for key in result.keys():
			self.__dict__[key] = result[key]

	def update(self,data,id = None):
		"""updates a row in the database using given id or loaded id"""
		if not self.validate_id(id):
			raise ValueError

		resolved = self.prepare_update(data)
		sql = 'UPDATE ' + self.table_name + ' set ' + resolved + ' where id = :id'
		data['id'] = self.id
		return self.execute(sql,data,True)

	def validate_id(self,id):
		"""checks if id is supplied and loads the data
		if id is not supplied, it checks if there is id property already set and returns bool """
		if id:
			self.find(id)
			return self.error_message == ''
		else:
			try:
				if not self.id:
					return False
				return True
			except:
				return False

	def delete(self,id = None):
		"""delets a row in the database using given id or loaded id"""
		if not self.validate_id(id):
			raise ValueError

		sql = 'DELETE FROM ' + self.table_name + ' WHERE id = ' + str(id) + ';'
		return self.execute(sql)

	def last_id(self):
		"""returns the id of the last record in a table"""
		allrows  = self.find_all()
		return allrows[len(allrows) - 1]['id']




