import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.room import Room

class TestRoom(unittest.TestCase):
	"""Test cases for Room"""

	def test_room_init_sets_the_name_and_type(self):
		room = Room('timber','L')
		self.assertEqual(room.name, 'timber')
		self.assertEqual(room.room_type, 'L')


	def test_room_sets_capacity_based_on_type(self):
		living_room = Room('timber','L')
		self.assertEqual(living_room.capacity, 4)
		office_space = Room('Rock','O')
		self.assertEqual(office_space.capacity, 6)

	"""Edge cases for init method"""
	def test_room_init_accept_only_string(self):
		self.assertRaises(ValueError, Room, 1, 2)

	def test_room_init_accept_only_string_for_name(self):
		self.assertRaises(ValueError, Room, 1, 'L')

	def test_room_init_accept_only_string_for_type(self):
		self.assertRaises(ValueError, Room, 'Iroko', 2)

	def test_room_init_accept_only_L_or_T_for_type(self):
		self.assertRaises(ValueError, Room, 'Iroko', 'P')



if __name__ == '__main__':
    unittest.main()
