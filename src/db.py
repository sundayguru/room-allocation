from datetime import datetime
from os import path
import sqlite3


class Db(object):
	"""This class contain several methods for manipulating Sqlite3 database."""

	def __init__(self, db_name='amity', table_name='table_name'):
		self.name = db_name
		self.table_name = table_name
		self.error_message = ''
		self.set_db(db_name)
		
	def set_db(self, name='amity'):
		""" Sets db location with the supplied db name """

		root = path.dirname(path.dirname(path.abspath(__file__)))
		self.db_location = root+'/'+name+'.db'

	def __db_open(self):
		"""Creates sqlite database connection."""

		self.connection = sqlite3.connect(self.db_location)
		#this will allow us to access the query result via the column name
		self.connection.row_factory = sqlite3.Row

	def __db_close(self):
		"""Closes sqlite database connection."""

		self.connection.close()

	def execute(self, sql, params={}, commit=False):
		"""Executes sql and return the query result if successful or bool if failed."""

		try:
			self.__db_open()
			result =  self.connection.execute(sql,params)
			if commit:
				self.connection.commit()
			return result
		except sqlite3.OperationalError, message:
			self.error_message = message
			return False

	def find(self, id):
		"""Returns a row in a given table if the id exists."""

		cursor =  self.execute("SELECT *  from " + self.table_name + ' WHERE id = ' + str(id))
		if cursor:
			result = cursor.fetchone()
			self.__db_set_attr(result)	
		else:
			result =  False
		self.__db_close()
		return result

	def find_all(self):
		"""Returns all records in a given table."""

		cursor = self.execute("SELECT *  from " + self.table_name)
		if cursor:
			result = cursor.fetchall()
		else:
			result = False
		self.__db_close()
		return result

	def find_by_attr(self, attributes, logic='AND'):
		"""Returns matching results based on."""

		where_clause = self.prepare_attr(attributes,logic)
		cursor = self.execute("SELECT *  from " + self.table_name + " WHERE " + where_clause,attributes)
		if cursor:
			result = cursor.fetchall()
		else:
			result = False
		self.__db_close()
		return result

	def create(self, data):
		"""Adds new row to the database based on table_name."""

		data['date_time'] = datetime.now()
		resolved = self.prepare_insert(data)
		sql = 'INSERT INTO ' + self.table_name + ' (' + resolved['column'] + ') VALUES (' + resolved['place_holders'] + ')'
		return self.execute(sql,data,True)
		

	def prepare_insert(self, data):
		"""Returns dict of columns separated in comma and value place holders separated with comma."""

		columns = ''
		place_holders = '';
		column_value = {}
		for key in data:
			columns += key + ','
			place_holders += ":" + str(key) + ","
		column_value['column'] = columns[:-1]
		column_value['place_holders'] = place_holders[:-1]
		return column_value

	def prepare_attr(self, data, logic):
		"""Returns a condition statement to be used in querying database."""

		where_clause = '';
		for key in data:
			where_clause += key + ' = :' + str(key) + " " + logic + ' '
		return where_clause[:-(len(logic) + 2)]

	def prepare_update(self, data):
		"""Returns combination of keys and place holder values for update method."""

		set_data = '';
		for key in data:
			if key == 'id':
				continue
			set_data += key + ' = :' + str(key) + "," 
		
		return set_data[:-1]  # -1 removes the last comma

	def __db_set_attr(self, result):
		"""Dynamic sets properties based on returned result."""

		if not result:
			return False

		for key in result.keys():
			self.__dict__[key] = result[key]

	def update(self, data, id=None):
		"""Updates a row in the database using given id or loaded id."""

		if not self.validate_id(id):
			raise ValueError

		resolved = self.prepare_update(data)
		sql = 'UPDATE ' + self.table_name + ' set ' + resolved + ' where id = :id'
		data['id'] = self.id
		return self.execute(sql,data,True)

	def validate_id(self, id):
		"""
		Checks if id is supplied and loads the data if id is not supplied, 
		it checks if there is id property already set and returns bool.
		"""

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

	def delete(self, id=None):
		"""Delets a row in the database using given id or loaded id."""

		if not self.validate_id(id):
			raise ValueError

		sql = 'DELETE FROM ' + self.table_name + ' WHERE id = ' + str(id) + ';'
		return self.execute(sql)

	def last_id(self):
		"""Returns the id of the last record in a table."""
		
		allrows  = self.find_all()
		print allrows[len(allrows) - 1]['id']
		return allrows[len(allrows) - 1]['id']




