import unittest
import sqlite3
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.db import Db

class TestDb(unittest.TestCase):
	"""Test cases for Db class"""

	def setUp(self):
		self.db = Db()

	def test_db_init_opens_connection(self):
		self.assertEqual(type(self.db.connection), sqlite3.Connection)

	def test_db_find_returns_false_when_invalid_table(self):
		data = self.db.find(1)
		self.assertEqual(data, False)


	def test_db_prepare(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru',
		'allocation':1
		}
		res = self.db.prepare(data)
		self.assertEqual(res, {'column': 'allocation,lastname,firstname', 'value': "'1','Nwuguru','sunday'"})


	def test_db_create(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru',
		'allocation':1
		}
		self.db.table_name = 'fellow'
		self.db.create(data)
		self.assertEqual(self.db.errormessage, '')


if __name__ == '__main__':
    unittest.main()
