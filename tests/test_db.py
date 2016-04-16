import unittest
import sqlite3
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.db import Db

class TestDb(unittest.TestCase):
	"""Test cases for Db class"""

	def test_db_init_opens_connection(self):
		db = Db()
		self.assertEqual(type(db.connection), sqlite3.Connection)
		db.find()

if __name__ == '__main__':
    unittest.main()
