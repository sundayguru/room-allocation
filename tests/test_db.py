import unittest
import sqlite3
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.db import Db

class TestDb(unittest.TestCase):
	"""Test cases for Db class"""

	def setUp(self):
		self.db = Db('amity_test')

	def test_db_find_returns_false_when_invalid_table(self):
		data = self.db.find(1)
		self.assertEqual(data, False)


	def test_db_prepareinsert(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru',
		'allocation':1
		}
		res = self.db.prepare_insert(data)
		self.assertEqual(res, {'column': 'allocation,lastname,firstname', 'place_holders':':allocation,:lastname,:firstname'})


	def test_db_create(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru',
		'allocation':1
		}
		self.db.table_name = 'fellow'
		self.db.create(data)
		self.assertEqual(self.db.error_message, '')
		id = self.db.last_id()
		self.db.find(id)
		self.assertEqual(self.db.firstname, 'sunday')

	def test_db_find(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru',
		'allocation':1
		}
		self.db.table_name = 'fellow'
		self.db.create(data)
		id = self.db.last_id()
		res = self.db.find(id)
		self.assertEqual(self.db.error_message, '')
		self.assertEqual(res['firstname'], 'sunday')

	def test_db_findall(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru',
		'allocation':1
		}
		self.db.table_name = 'fellow'
		self.db.create(data)
		res = self.db.find_all()
		self.assertEqual(self.db.error_message, '')
		self.assertNotEqual(len(res), 0)


	def test_db_findbyattr(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru',
		'allocation':1
		}
		self.db.table_name = 'fellow'
		self.db.create(data)
		res = self.db.find_by_attr({'firstname':'sunday','allocation':1},'AND')
		self.assertEqual(self.db.error_message, '')
		self.assertNotEqual(len(res), 0)

	def test_db_set_attr(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru',
		'allocation':1
		}
		self.db.table_name = 'fellow'
		self.db.create(data)
		res = self.db.find(1)
		self.assertEqual(self.db.error_message, '')
		self.assertEqual(self.db.firstname, data['firstname'])

	def test_db_prepare_update(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru'
		}
		res = self.db.prepare_update(data)
		self.assertEqual(res, 'lastname = :lastname,firstname = :firstname')

	def test_db_prepare_attr(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru'
		}
		res = self.db.prepare_attr(data,'AND')
		self.assertEqual(res, 'lastname = :lastname AND firstname = :firstname')


	def test_db_validate_id(self):
		res = self.db.validate_id(None)
		self.assertEqual(res, False)

	def test_db_update_without_id(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru'
		}
		self.assertRaises(ValueError, self.db.update, data)


	def test_db_update_with_id_from_find(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru',
		'allocation':1
		}

		self.db.table_name = 'fellow'
		self.db.create(data)
		id = self.db.last_id()
		self.db.find(id)
		data['firstname'] = 'david'
		self.db.update(data)
		self.assertEqual(self.db.error_message, '')
		self.db.find(id)
		self.assertEqual(self.db.firstname, 'david')


	def test_db_update_with_id_known(self):
		data = {
		'firstname':'sunday',
		'lastname':'Nwuguru',
		'allocation':1
		}

		self.db.table_name = 'fellow'
		self.db.create(data)
		id = self.db.last_id()
		data['firstname'] = 'david'
		self.db.update(data,id)
		self.assertEqual(self.db.error_message, '')
		self.db.find(id)
		self.assertEqual(self.db.firstname, 'david')

	


if __name__ == '__main__':
    unittest.main()
