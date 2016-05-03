import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.amity import Amity
from src.room import Room
from src.fellow import Fellow
from src.staff import Staff
from src.office import Office
from src.livingspace import LivingSpace

class TestAmity(unittest.TestCase):
	"""Test cases for Amity"""

	def add_person(self, living_space=True):
		amity = Amity('add_person')
		args = {
		'<firstname>':'test',
		'<lastname>':'user',
		'<person_type>':'fellow',
		'-w':living_space,
		}
		amity.people = []  # make sure the people list is empty
		amity.run_command(args)
		return amity


	def create_room(self):
		amity = Amity('create_room')
		args = {
		'<room_name>':['testRoom 1','testRoom 2','testRoom 3'],
		'<room_type>':['living','office','living'],
		}
		amity.rooms = []  # make sure the rooms list is empty
		amity.run_command(args)
		return amity

	def test_0_amity_init_sets_command(self):
		amity = Amity('list_people')
		self.assertEqual(amity.command, 'list_people')

	def test_1_amity_create_room(self):
		amity = self.create_room()
		self.assertEqual(len(amity.rooms), 3)
		self.assertEqual(amity.rooms[0].name, 'TESTROOM 1')

		
	def test_2_amity_add_person(self):
		amity = self.add_person()
		self.assertEqual(len(amity.people), 1)
		self.assertEqual(amity.people[0].name(), 'TEST USER')
		
	def test_3_amity_reallocate_person(self):
		amity = Amity('reallocate_person')
		person = amity.people[0]
		new_room = "TESTROOM 3" if person.assigned_room['LIVINGSPACE'] == 'TESTROOM 1' else "TESTROOM 1"
		args = {
		'<person_id>':person.uid,
		'<new_room_name>':new_room,
		'-l':True,
		}
		amity.run_command(args)
		self.assertEqual(amity.people[0].assigned_room['LIVINGSPACE'], new_room)
		
	def test_4_amity_allocate_person(self):
		self.add_person(False)
		amity = Amity('allocate_person')
		person = amity.people[-1] # Select the last added
		args = {
		'<person_id>':person.uid,
		'<new_room_name>':'testRoom 1',
		'-w':True,
		}
		amity.run_command(args)
		self.assertEqual(amity.people[-1].assigned_room['LIVINGSPACE'], 'TESTROOM 1')
		self.assertEqual(amity.people[-1].is_allocated, True)
		
	def test_5_amity_remove_person(self):
		self.create_room()
		self.add_person()
		amity = Amity('remove_person')
		person = amity.people[-1] # Select the last added
		args = {
		'<person_id>':person.uid,
		'<current_room_name>':person.assigned_room['LIVINGSPACE'],
		}
		amity.run_command(args)
		room = [room for room in amity.rooms if room.name == 'TESTROOM 1']
		if room:
			old_person = [p for p in room[0].people if p.name() == person.name()]
		self.assertEqual(old_person, [])
		
	def test_6_amity_load_person(self):
		self.create_room()
		amity = Amity('load_people')
		amity.people = []
		args = {
		'<file_location>':'data/people_test.txt',
		}
		amity.run_command(args)
		self.assertEqual(len(amity.people), 2)

if __name__ == '__main__':
    unittest.main()
