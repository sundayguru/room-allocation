import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.amity import Amity
from src.room import Room
from src.fellow import Fellow
from src.staff import Staff
from src.office import Office
from src.livingspace import LivingSpace
from src.migration import Migration

class TestAmity(unittest.TestCase):
	"""Test cases for Amity"""

	def add_person(self, living_space=True, reset=True):
		amity = Amity('add_person')
		args = {
		'<firstname>':'test',
		'<lastname>':'user',
		'<person_type>':'fellow',
		'-w':living_space,
		}
		if reset:
			amity.people = []  # make sure the people list is empty
		amity.run_command(args)
		return amity


	def create_room(self):
		amity = Amity('create_room')
		args = {
		'<room_name>':['testRoom 1','testRoom 2','testRoom 3','testRoom 1'],
		'<room_type>':['living','office','living'	],
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
		self.create_room()
		self.add_person()
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
		self.create_room()
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
	
	def test_7_amity_allocate_returns_false_for_empty_room(self):
		amity = Amity('list_people')
		amity.rooms = []
		person = Fellow('Sunday','nwuguru',True)
		self.assertEqual(amity.allocate(person), False)
	
	def test_8_amity_allocate_returns_false_when_allocating_to_same_room(self):
		amity = self.create_room()
		amity.exception_room = amity.rooms[0]
		person = Fellow('Sunday','nwuguru',True)
		self.assertEqual(amity.allocate(person,'testRoom 1'), False)

	def test_9_amity_allocate_returns_false_when_allocating_to_invalid_room_name(self):
		amity = self.create_room()
		person = Fellow('Sunday','nwuguru',True)
		self.assertEqual(amity.allocate(person,'testRoom 5'), False)

	def test_10_amity_allocate_returns_false_when_room_allocation_fails(self):
		amity = self.create_room()
		person = Fellow('Sunday','nwuguru',True)
		room = amity.rooms[0]
		room.capacity = 0
		self.assertEqual(amity.allocate(person,room.name), False)

	def test_11_amity_select_random_room(self):
		amity = self.create_room()
		amity.exception_room = amity.rooms[0]
		room = amity.select_random_room('livingspace')
		self.assertEqual(room.name, 'TESTROOM 3')
		self.assertEqual(amity.select_random_room('unknown'), False)

	def test_12_amity_drop_pickle_files(self):
		amity = self.create_room()
		self.assertNotEqual(amity.rooms, [])
		amity.drop_pickle_files()
		self.assertEqual(amity.rooms, [])

	def test_13_amity_list_people(self):
		self.create_room()
		amity = Amity('list_people')
		amity.people = []
		self.assertEqual(amity.list_people({}), False)
		self.add_person(False,False)
		amity = self.add_person(True,False)
		self.assertEqual(amity.list_people({'-u':True,'-a':False}), None)
		self.assertEqual(amity.list_people({'-u':False,'-a':True}), None)

	def test_14_amity_list_rooms(self):
		amity = Amity('list_room')
		amity.rooms = []
		self.assertEqual(amity.list_rooms({}), False)
		amity = self.create_room()
		self.assertEqual(amity.list_rooms({'-u':True,'-a':False}), None)
		self.assertEqual(amity.list_rooms({'-u':False,'-a':True}), None)


	def test_15_amity_print_allocations(self):
		amity = Amity('print_allocations')
		amity.rooms = []
		self.assertEqual(amity.print_allocations({}), False)
		self.create_room()
		amity = self.add_person()
		self.assertEqual(amity.print_allocations({'-o':False}), None)
		self.assertEqual(amity.print_allocations({'-o':True,'<file_name>':'tt.txt'}), None)


	def test_16_amity_print_unallocated(self):
		amity = Amity('print_unallocated')
		self.assertEqual(amity.print_unallocated({'-r':True,'-o':True,'<file_name>':'tt.txt'}), None)
		self.assertEqual(amity.print_unallocated({'-r':True,'-o':False,'<file_name>':'tt.txt'}), None)
		self.assertEqual(amity.print_unallocated({'-r':False,'-o':False,'<file_name>':'tt.txt'}), None)
		self.assertEqual(amity.print_unallocated({'-r':False,'-o':True,'<file_name>':'tt.txt'}), None)

	def test_17_amity_print_unallocated_room(self):
		amity = self.create_room()
		self.assertEqual(amity.print_unallocated_room({'-o':True,'<file_name>':'tt.txt'}), None)
		self.assertEqual(amity.print_unallocated_room({'-o':False,'<file_name>':'tt.txt'}), None)
		amity.rooms = []
		self.assertEqual(amity.print_unallocated_room({'-o':False,'<file_name>':'tt.txt'}), False)

	def test_18_amity_print_unallocated_people(self):
		amity = self.create_room()
		self.assertEqual(amity.print_unallocated_people({'-o':True,'<file_name>':'tt.txt'}), None)
		self.assertEqual(amity.print_unallocated_people({'-o':False,'<file_name>':'tt.txt'}), None)
		amity.people = []
		self.assertEqual(amity.print_unallocated_people({'-o':False,'<file_name>':'tt.txt'}), False)

	def test_19_amity_print_room(self):
		self.create_room()
		amity = self.add_person()
		self.assertEqual(amity.print_room({'<name_of_room>':'testRoom 1'}), None)
		self.assertEqual(amity.print_room({'<name_of_room>':'unkown'}), False)

	def test_20_amity_save_state(self):
		self.create_room()
		self.add_person()
		amity = Amity('save_state')
		amity.run_command({'--db':False})
		amity = Amity('save_state')
		self.assertEqual(amity.rooms, [])

	def test_21_amity_load_state(self):
		amity = Amity('load_state')
		amity.run_command({'--db':False})
		self.assertNotEqual(amity.rooms, [])

	def test_22_amity_save_people_state(self):
		amity = Amity('save_state')
		amity.people = []
		self.assertEqual(amity.save_people_state(), False)

	def test_22_amity_load_people_state(self):
		migrate = Migration()
		migrate.drop()
		migrate.install()
		amity = Amity('load_state')
		self.assertEqual(amity.load_people_state(), False)

if __name__ == '__main__':
    unittest.main()
