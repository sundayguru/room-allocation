import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.room import Room
from src.person import Person

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

	def test_room_allocate_fellow(self):
		room = Room('Iroko','L')
		person = Person('Sunday','FELLOW',True)
		room.allocate(person)
		self.assertNotEqual(room.people, [])
		self.assertEqual(type(person), type(room.people[0]))

	def test_room_allocate_staff(self):
		room = Room('Iroko','O')
		person = Person('Nandaa','STAFF')
		room.allocate(person)
		self.assertNotEqual(room.people, [])
		self.assertEqual(type(person), type(room.people[0]))


	def test_room_allocate_fails_when_is_filled(self):
		room = Room('Iroko','O')
		name = 'Nandaa'
		person = Person(name,'STAFF')
		room.is_filled = True
		self.assertEqual(room.allocate(person),False)

	"""Edge cases for init method"""
	def test_room_init_accept_only_string(self):
		self.assertRaises(ValueError, Room, 1, 2)

	def test_room_init_accept_only_string_for_name(self):
		self.assertRaises(ValueError, Room, 1, 'L')

	def test_room_init_accept_only_string_for_type(self):
		self.assertRaises(ValueError, Room, 'Iroko', 2)

	def test_room_init_accept_only_L_or_T_for_type(self):
		self.assertRaises(ValueError, Room, 'Iroko', 'P')


	"""Edge cases for allocate method"""
	def test_room_allocate_fails_when_person_living_space_is_false(self):
		room = Room('Iroko','L')
		person = Person('Sunday','FELLOW')
		self.assertEqual(room.allocate(person), False)
		self.assertEqual(room.people, [])
		
	def test_room_allocate_fails_when_person_type_is_fellow_and_room_type_is_O(self):
		room = Room('Iroko','O')
		person = Person('Sunday','FELLOW',True)
		self.assertEqual(room.allocate(person), False)
		self.assertEqual(room.people, [])
		
	def test_room_allocate_fails_when_person_type_is_staff_and_room_type_is_L(self):
		room = Room('Iroko','L')
		person = Person('Nandaa','STAFF',True)
		self.assertEqual(room.allocate(person), False)
		self.assertEqual(room.people, [])
		
	def test_room_allocate_only_person_instance(self):
		room = Room('Iroko','O')
		person = {}
		self.assertRaises(ValueError, room.allocate, person)
		


if __name__ == '__main__':
    unittest.main()
