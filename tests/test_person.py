import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.person import Person

class TestPerson(unittest.TestCase):
	"""Test cases for Person class"""

	def test_person_init_sets_the_name_and_type(self):
		person = Person('sunday','nwuguru')
		self.assertEqual(person.name(), 'sunday nwuguru')
		self.assertNotEqual(person.living_space, True)

	def test_person_init_sets_the_living_space_when_passed(self):
		person = Person('sunday','nwuguru',True)
		self.assertEqual(person.living_space, True)

	def test_person_get_state_dict(self):
		person = Person('sunday','nwuguru',True)
		self.assertEqual(person.get_state_dict(3),'NO')

	def test_person_init_accept_only_string_for_name_and_type(self):
		"""Edge cases for init method"""

		self.assertRaises(ValueError, Person, 'Nandaa', 'Anthony','True')

	def test_person_init_accept_only_boolean_for_living_space(self):
		self.assertRaises(ValueError, Person, 'sunday','nwuguru', 2)

	def test_person_init_accept_only_string_for_name(self):
		self.assertRaises(ValueError, Person, 1, 'nwuguru')

if __name__ == '__main__':
    unittest.main()
