import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.room import Room
from src.person import Person
from src.allocationapp import AllocationApp

class TestAllocationApp(unittest.TestCase):
	"""Test cases for AllocationApp"""

	def setUp(self):
		self.app = AllocationApp('Sunday')

	def test_app_init_populates_rooms(self):
		self.assertNotEqual(self.app.rooms, [])
		self.assertEqual(type(self.app.rooms[0]), Room)

	def test_app_init_loads_people_from_file(self):
		self.assertNotEqual(self.app.people, [])
		self.assertEqual(type(self.app.people[0]), Person)


if __name__ == '__main__':
    unittest.main()
