import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.room import Room
from src.fellow import Fellow
from src.staff import Staff
from src.office import Office
from src.livingspace import LivingSpace

class TestRoom(unittest.TestCase):
	"""Test cases for Room"""

	def test_room_init_sets_the_name(self):
		room = Room('timber')
		self.assertEqual(room.name, 'timber')

	def test_room_allocate_fellow(self):
		room = LivingSpace('Iroko')
		person = Fellow('Sunday','nwuguru',True)
		room.allocate(person)
		self.assertNotEqual(room.people, [])
		self.assertEqual(type(person), type(room.people[0]))

	def test_room_allocate_staff(self):
		room = Office('Iroko')
		person = Staff('Anthony','Nandaa')
		room.allocate(person)
		self.assertNotEqual(room.people, [])
		self.assertEqual(type(person), type(room.people[0]))


	def test_room_allocate_fails_when_is_filled(self):
		room = Office('Iroko')
		person = Staff('Anthiny','Nandaa')
		room.capacity = 0
		self.assertEqual(room.allocate(person),False)

	def test_room_remove_person(self):
		room = Office('Iroko')
		person = Staff('Anthiny','Nandaa')
		room.allocate(person)
		self.assertNotEqual(room.people,[])
		room.remove_person(person)
		self.assertEqual(room.people,[])
		self.assertEqual(room.remove_person(person),False)


	def test_room_people_list_with_room_name(self):
		room = Office('Iroko')
		person = Staff('Anthiny','Nandaa')
		room.allocate(person)
		data = room.people_list_with_room_name(False)
		self.assertNotEqual(data,[])

	def test_room_allocate_able(self):
		room = Office('Iroko')
		person = Staff('Anthiny','Nandaa')
		room.allocate(person)
		self.assertEqual(room.allocate_able(person),False)


	def test_room_init_accept_only_string(self):
		"""Edge cases for init method"""

		self.assertRaises(ValueError, Room, 1)

	def test_room_allocate_fails_when_person_living_space_is_false(self):
		"""Edge cases for allocate method"""

		room = LivingSpace('Iroko')
		person = Fellow('Sunday','nwuguru')
		self.assertEqual(room.allocate(person), False)
		self.assertEqual(room.people, [])
		
	def test_room_allocate_returns_true_for_fellow_and_room_type_is_O(self):
		room = Office('Iroko')
		person = Fellow('Sunday','nwuguru',True)
		self.assertEqual(room.allocate(person), True)
		
	def test_room_allocate_fails_when_person_type_is_staff_and_room_type_is_L(self):
		room = LivingSpace('Iroko')
		person = Staff('Anthony','Nandaa')
		self.assertEqual(room.allocate(person), False)
		self.assertEqual(room.people, [])
		
if __name__ == '__main__':
    unittest.main()
