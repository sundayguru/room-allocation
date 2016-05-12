import unittest
import sqlite3
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.db import Db
from src.migration import Migration


class TestDb(unittest.TestCase):
	"""Test cases for Db class"""

	def setUp(self):
		migrate = Migration('amity_test')
		migrate.drop()
		migrate.install()
		self.db = Db('amity_test')
		self.data = {
		'firstname':'sunday',
		'lastname':'Nwuguru',
		'allocated':1,
		'living_space':1
		}
		self.db.table_name = 'person'


	def test_db_find_returns_false_when_invalid_table(self):
		self.db.table_name = ''
		data = self.db.find(0)
		self.assertEqual(data, False)

	def test_db_prepareinsert(self):
		res = self.db.prepare_insert(self.data)
		self.assertEqual(res['column'], 'lastname,allocated,living_space,firstname')


	def test_db_create(self):
		self.db.create(self.data)
		self.assertEqual(self.db.error_message, '')

	def test_db_find(self):
		self.db.create(self.data)
		id = self.db.last_id()
		res = self.db.find(id)
		self.assertEqual(self.db.error_message, '')
		self.assertEqual(res['firstname'], 'sunday')

	def test_db_findall(self):
		self.db.create(self.data)
		res = self.db.find_all()
		self.assertEqual(self.db.error_message, '')
		self.assertNotEqual(len(res), 0)
	
	def test_db_findbyattr(self):
		self.db.create(self.data)
		res = self.db.find_by_attr({'firstname':'sunday','allocated':1},'AND')
		self.assertEqual(self.db.error_message, '')
		self.assertNotEqual(len(res), 0)

	def test_db_set_attr(self):
		self.db.create(self.data)
		res = self.db.find(1)
		self.assertEqual(self.db.error_message, '')
		self.assertEqual(self.db.firstname, self.data['firstname'])

	def test_db_prepare_update(self):
		res = self.db.prepare_update(self.data)
		self.assertEqual(res, 'lastname = :lastname,allocated = :allocated,living_space = :living_space,firstname = :firstname')

	def test_db_prepare_attr(self):
		res = self.db.prepare_attr(self.data,'AND')
		self.assertEqual(res, 'lastname = :lastname AND allocated = :allocated AND living_space = :living_space AND firstname = :firstname')

	def test_db_validate_id(self):
		res = self.db.validate_id(None)
		self.assertEqual(res, False)

	def test_db_update_without_id(self):
		self.assertRaises(ValueError, self.db.update, self.data)

	def test_db_update_with_id_from_find(self):
		self.db.create(self.data)
		id = self.db.last_id()
		self.db.find(id)
		self.data['firstname'] = 'david'
		self.db.update(self.data)
		self.assertEqual(self.db.error_message, '')
		self.db.find(id)
		self.assertEqual(self.db.firstname, 'david')

	def test_db_update_with_id_known(self):
		self.db.create(self.data)
		id = self.db.last_id()
		self.data['firstname'] = 'david'
		self.db.update(self.data,id)
		self.assertEqual(self.db.error_message, '')
		self.db.find(id)
		self.assertEqual(self.db.firstname, 'david')

	


		

if __name__ == '__main__':
    unittest.main()
