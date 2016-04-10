import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.person import Person

class TestPerson(unittest.TestCase):
	"""Test cases for Person class"""

	def test_person_init_sets_the_name_and_type(self):
		person = Person('sunday','FELLOW')
		self.assertEqual(person.name, 'sunday')
		self.assertEqual(person.person_type, 'FELLOW')
		self.assertNotEqual(person.living_space, True)

	def test_person_init_sets_the_living_space_when_passed(self):
		person = Person('sunday','FELLOW',True)
		self.assertEqual(person.living_space, True)

	"""Edge cases for init method"""
	def test_person_init_accept_only_string_for_name_and_type(self):
		self.assertRaises(ValueError, Person, 'Nandaa', 'STAFF','True')
		self.assertRaises(ValueError, Person, 'Nandaa', 'ELSE',True)

	def test_person_init_accept_only_boolean_for_living_space(self):
		self.assertRaises(ValueError, Person, True, 2)

	def test_person_init_accept_only_string_for_name(self):
		self.assertRaises(ValueError, Person, 1, 'FELLOW')

	def test_room_init_accept_only_string_for_type(self):
		self.assertRaises(ValueError, Person, 'sunday', 2)

	def test_room_init_accept_only_FELLOW_and_STAFF_for_type(self):
		self.assertRaises(ValueError, Person, 'sunday', 'success')

if __name__ == '__main__':
    unittest.main()
