import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.room import Room
from src.person import Person
from src.allocationapp import AllocationApp

class TestAllocationApp(unittest.TestCase):
	"""Test cases for AllocationApp"""

	def test_app_init_populates_rooms(self):
		app = AllocationApp('Sunday')
		self.assertEqual(len(app.rooms), 20)
		self.assertEqual(type(app.rooms[0]), Room)


if __name__ == '__main__':
    unittest.main()
