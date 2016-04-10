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


if __name__ == '__main__':
    unittest.main()
