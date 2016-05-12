from random import randint

from fellow import Fellow
from livingspace import LivingSpace
from migration import Migration
from office import Office
from staff import Staff
from util import Util


class Amity(object):
	"""
	This class holds all the methods executed from the commands, 
	run_command method is the entry point of all the commands.
	"""

	def __init__(self, command):
		Util.clear_screen()  # clears the terminal
		self.command = command
		self.util = Util()
		self.people = self.load_people_from_pickle()
		self.rooms = self.load_rooms()
		self.settings = self.load_settings()
		self.exception_room = ''
		


	def load_people_from_pickle(self):
		"""
		This method will populate people list from people.pkl file
		"""

		self.util.file_manager.set_file_location('people.pkl')
		people = self.util.file_manager.pickle_load()
		return people if people else []
		
	def load_settings(self):
		"""Loads settings from pickle file"""

		self.util.file_manager.set_file_location('config.pkl')
		settings = self.util.file_manager.pickle_load()
		return settings if settings else {'drop_db': False}
		
	def load_rooms(self):
		"""Loads rooms from pickle file"""

		self.util.file_manager.set_file_location('rooms.pkl')
		rooms = self.util.file_manager.pickle_load()
		return rooms if rooms else []
	
	def get_unallocated_rooms_by_type(self, room_type):
		"""
		This method will return a list of unallocated rooms base on room type
		"""

		return [room for room in self.rooms if room.room_type.lower() == room_type.lower() and not room.is_filled ]

	def get_unallocated_room_by_name(self,room_name):
		"""
		This method will return a list of unallocated rooms base on room name
		"""
		return [room for room in self.rooms if room.name.lower() == room_name.lower() and not room.is_filled ]

	def get_room_by_name(self,room_name):
		"""
		This method will return a room corresponding to the room name parameter
		"""
		return [room for room in self.rooms if room.name.lower() == room_name.lower()]

	def allocate(self, person, room_name=None, room_type="LivingSpace"):
		"""Allocates person to a room based on room_name, exception_room or random"""

		if person.is_fellow() and not person.living_space and room_type == 'LivingSpace':
			return False


		if len(self.rooms) == 0:
			Util.print_line('No room available')
			return False

		if room_name:
			selected_room = self.select_room_by_name(room_name)
			if self.exception_room:
				if selected_room.room_type != self.exception_room.room_type or selected_room.name == self.exception_room.name:
					Util.print_line(person.name() + ' cannot be allocated to ' + selected_room.name)
					return False
		else:
			room_type = "office" if person.is_staff() else room_type
			selected_room = self.select_random_room(room_type)

		if not selected_room:
			Util.print_line('Room is not available')
			return False

		if selected_room.allocate(person):
			Util.print_line(person.name() + ' allocated to '+ selected_room.name)
			return True
		else:
			Util.print_line('Unable to allocate '+ person.name() + ' to '+ selected_room.name)
			return False

	def select_room_by_name(self,room_name):
		"""
		This method will return unallocated room base on room name
		"""
		available_rooms = self.get_unallocated_room_by_name(room_name)
		try:
			return available_rooms[0]
		except:
			return False
		
	def select_random_room(self,room_type):
		"""
		This method will return a random unallocated rooms base on room type
		"""
		available_rooms = self.get_unallocated_rooms_by_type(room_type)
		try:
			random = randint(0,len(available_rooms) - 1)
			selected_room = available_rooms[random]
			if self.exception_room and selected_room.name == self.exception_room.name:
				available_rooms.pop(random)  # remove the selected room from available rooms
				random = randint(0,len(available_rooms) - 1)
				selected_room = available_rooms[random]
			return selected_room
		except:
			return False

	def save_state_to_pickle(self):
		"""Save current state to pickle file"""

		self.util.file_manager.set_file_location('people.pkl')
		self.util.file_manager.pickle_dump(self.people)
		self.util.file_manager.set_file_location('rooms.pkl')
		self.util.file_manager.pickle_dump(self.rooms)
		self.util.file_manager.set_file_location('config.pkl')
		self.util.file_manager.pickle_dump(self.settings)

	def drop_pickle_files(self):
		"""Removes all pickle file except config """

		self.util.file_manager.set_file_location('people.pkl')
		self.util.file_manager.remove()
		self.util.file_manager.set_file_location('rooms.pkl')
		self.util.file_manager.remove()
		self.people = []
		self.rooms = []
		 
	def run_command(self, args):
		"""Gets the required method and calls the method with the arguments passed as parameter"""

		method = getattr(self,self.command)
		method(args)	
		Util.print_divider()

	def add_person(self, args):
		"""
		Resolves the argument and creates the right person type, 
		adds the person to people list and allocates the person to a room. 
		This also saves the current state to pickle file
		"""

		firstname = args['<firstname>'].upper()
		lastname = args['<lastname>'].upper()
		if args['<person_type>'].upper() == 'FELLOW':
			person = Fellow(firstname,lastname,args['-w'])
	  	else:
	  		person = Staff(firstname,lastname,args['-w'])

	  	if self.person_exists(person):
	  		Util.print_line(person.name() + ' already exists')
	  	else:
	  		self.people.append(person)
	  		print person.name() + ' successfully created'
  			self.allocate(person,None,'OFFICE')
	  		if person.is_fellow():
	  			self.allocate(person)
	  	self.save_state_to_pickle()

	def list_people(self, args):
		"""Displays the list of available people based on options specified (-u or -a)"""

		print('LIST OF AVAILABLE PEOPLE')
		Util.print_divider()
		if len(self.people) == 0:
			Util.print_line('No person found')
			return False

		data = [Staff.headers()]
		for index,person in enumerate(self.people):
			if args['-u']:
				if person.is_allocated:
					continue

			if args['-a']:
				if not person.is_allocated:
					continue

			data.append([(index + 1)] + person.details_list())
		Util.tabulate(data)

	def list_rooms(self, args):
		"""Displays the list of available rooms"""

		print 'LIST OF AVAILABLE ROOMS'
		Util.print_divider()
		if len(self.rooms) == 0:
			Util.print_line('No room found')
			return False

		data = [['S/N','Room Name & Type','Total Allocation']]
		for index,room in enumerate(self.rooms):
			if args['-u']:
				if len(room.people) != 0:
					continue

			if args['-a']:
				if len(room.people) == 0:
					continue
			data.append([index + 1,room.nameplate(), str(len(room.people)) + ' people'])
		
		Util.tabulate(data)

	def print_allocations(self, args):
		"""
		Displays the list of current allocations.
		Exports allocations to file if file name is specified
		"""

		Util.print_line('LIST OF ALLOCATIONS')
		if len(self.rooms) == 0:
			Util.print_line('No room found')
			return False

		counter = 0
		if args['-o']:
			self.send_room_allocations_to_file(args['<file_name>'])
		else:
			for room in self.rooms:
				if len(room.people) != 0:
					counter += 1
					room.people_list_with_room_name()

			if counter > 0:
				Util.print_line(str(counter) + ' of ' + str(len(self.rooms)) + ' room(s) allocated')
			else:
				Util.print_line('No room has been allocated')

	def print_unallocated(self, args):
		""" 
		Calls print_unallocated_people method if no -r options.
		Calls print_unallocated_room if -r option is specified.
		"""

		if args['-r']:
			Util.print_line('LIST OF UNALLOCATED ROOMS')
			self.print_unallocated_room(args)
		else:
			Util.print_line('LIST OF UNALLOCATED PEOPLE')
			self.print_unallocated_people(args)

	def print_unallocated_room(self, args):
		"""
		Displays unallocated rooms.
		Exports list to file if file name is specified
		"""

		if len(self.rooms) == 0:
			Util.print_line('No room found')
			return False
		
		counter = 0	
		if args['-o']:
			self.send_room_allocations_to_file(args['<file_name>'],False)
		else:
			for room in self.rooms:
				if len(room.people) == 0:
					counter += 1
					room.people_list_with_room_name()

			if counter > 0:
				Util.print_line(str(counter) + ' unallocated room(s)')
			else:
				Util.print_line('No unallocated room')

	def print_unallocated_people(self, args):
		"""
		Displays unallocated people.
		exports list to file if file name is specified
		"""

		if len(self.people) == 0:
			Util.print_line('No person found')
			return False
		
		
		if args['-o']:
			self.send_people_allocations_to_file(args['<file_name>'],False)
		else:
			records = self.get_people_table()
			Util.tabulate(records)
			counter = len(records) - 1
			if counter > 0:
				Util.print_line(str(counter) + ' unallocated person')
			else:
				Util.print_line('No unallocated person')

	def get_people_table(self, allocated=True):
		""" Returns the list of people with headers as the first item in the list """

		records = [Staff.headers()]
		counter = 0	
		for person in self.people:
			if not person.is_allocated and not allocated:
				counter += 1
				records.append([counter] + person.details_list())
			else:
				counter += 1
				records.append([counter] + person.details_list())
		return records

	def print_room(self, args):
		"""Displays the room details and the list of allocated person"""

		room = self.get_room_by_name(args['<name_of_room>'])
		if room:
			room[0].people_list_with_room_name()
		else:
			Util.print_line(args['<name_of_room>'] + ' room not found')
			return False

	def send_room_allocations_to_file(self, file_name, allocated=True):
		"""Exports room allocations to specified file name"""

		title = "List of allocated rooms" if allocated else "List of unallocated rooms"
		records = title+'\n'
		records += Util.line() + '\n'
		for room in self.rooms:
			if room.people and allocated:
				records += room.people_list_with_room_name(False) + '\n'
			elif not allocated and not room.people:
				records += room.nameplate() + '\n'

		self.util.file_manager.set_file_location(file_name)
		self.util.file_manager.replace(records)
		Util.print_line('Records successfully exported to data/' + file_name)

	def send_people_allocations_to_file(self, file_name, allocated=True):
		"""Send people fulldetails based on allocation status to specified file name"""

		title = "List of allocated person" if allocated else "List of unallocated person"
		records = title+'\n'
		records += Util.line() + '\n'
		records += str(Util.get_table(self.get_people_table()))

		self.util.file_manager.set_file_location(file_name)
		self.util.file_manager.replace(records)
		Util.print_line('Records successfully exported to data/' + file_name)

	def create_room(self, args):
		"""Creates room(s) and save to pickle"""

		room_names = args['<room_name>']
		room_types = args['<room_type>']
		for name,room_type in zip(room_names,room_types):
			if room_type.upper() == 'OFFICE':
			  room = Office(name.upper())
			else:
			  room = LivingSpace(name.upper())

			if self.room_exists(room):
				Util.print_line(room.name + ' already exists')
			else:
				self.rooms.append(room)
				print room.name + ' successfully created'
		self.save_state_to_pickle()

	def room_exists(self, room):
		"""
		This method will return boolean based on availability of a given room object in the rooms list
		"""

		for old_room in self.rooms:
			if old_room.name == room.name:
				return True
		return False

	def person_exists(self, person):
		"""
		This method will return boolean based on availability of a given person object in the people list
		"""

		for old_person in self.people:
			if old_person.name() == person.name():
				return True
		return False

	def reallocate_person(self, args):
		"""Reallocate person from one room to another"""

		room_name = args['<new_room_name>'].upper()
		person_id = args['<person_id>'].upper()
		room_type = 'OFFICE' if not args['-l'] else 'LIVINGSPACE'
		person = self.get_person_by_uid(person_id)
		if not person:
			print 'No person with ID: ' + person_id
			return False

		if not person.is_allocated:
			Util.print_line(person.name() + ' has not been allocated to a room')
			answer = Util.prompt('Do you want to allocate ' + person.name() + ' to ' + room_name + '? Y/N: ')
			if answer == 'N':
				return False

		if room_name in person.assigned_room.values():
			Util.print_line('You cannot reallocate ' + person.name() + ' to the same room')
			return False

		
		room = self.remove_person_from_room(person, room_type)
		if not room:
			Util.print_line('Unable to find person in a room')
			return False

		person.living_space = True if room_type == 'LIVINGSPACE' else False
		if not self.allocate(person, room_name):
			msg = person.name() + ' cannot be allocated to '+ room_name 
			msg += '; Kindly verify that '+ room_name + ' is a/an ' + room_type
			Util.print_line(msg)
			if room:
				room.allocate(person)
				Util.print_line(person.name() + ' has been moved back to ' + room.name)

		self.save_state_to_pickle()

	def remove_person(self, args):
		"""
		This method will remove a person from a given room name without reallocating the person
		"""

		room_name = args['<current_room_name>'].upper()
		person_id = args['<person_id>'].upper()
		person = self.get_person_by_uid(person_id)
		if not person:
			print 'no person with ID: ' + person_id
			return False

		if not person.is_allocated:
			print person.name() + ' has not been allocated to a room'
			return False

		room = self.get_room_by_name(room_name)
		if room:
			if room[0].remove_person(person):
				Util.print_line(person.name() + ' has been removed from ' + room[0].name)
			else:
				Util.print_line('Unable to remove '+ person.name())
		else:
			Util.print_line(room_name + ' not found')

		self.save_state_to_pickle()

	def allocate_person(self, args):
		"""Allocate person to a room"""

		room_name = args['<new_room_name>'].upper()
		person_id = args['<person_id>'].upper()
		person = self.get_person_by_uid(person_id)
		if not person:
			print 'no person with ID: ' + person_id
			return False

		if person.is_allocated and len(person.assigned_room) > 1:
			print person.name() + ' has been allocated to ' + (' and '.join(person.assigned_room.keys()))
			return False

		room = self.get_room_by_name(room_name)
		if room:
			if args['-w'] and person.is_fellow():
				person.living_space = True

			if room[0].allocate(person):
				if room[0].room_type == 'OFFICE':
					self.allocate(person)
				Util.print_line(person.name() + ' has been allocated to ' + room[0].name)
			else:
				Util.print_line('Unable to allocate ' + person.name())
		else:
			Util.print_line(room_name + ' not found')

		self.save_state_to_pickle()

	def get_person_by_uid(self, uid):
		"""Return person instance with corresponding uid"""

		for person in self.people:
			if person.uid == uid:
				return person
		return False


	def remove_person_from_room(self, person,room_type):
		"""Remove person from a room"""

		room_name = person.assigned_room[room_type]
		room = self.get_room_by_name(room_name)
		if room:
			if room[0].remove_person(person):
				self.exception_room = room[0]
				return room[0]

		return False

	def load_people(self, args):
		"""Creates people from a specified file and allocates each person based on person type"""

		path = args['<file_location>']
		if not Util.is_file(path):
			Util.print_line('File location is invalid')
			return False

		with open(path,'r') as file:
			for line in file:
				records = line.split()
				living_space = False
				firstname = records[0]
				lastname = records[1]
				person_type = records[2]
				if person_type.upper() == 'FELLOW':
					if(records[3].upper() == 'Y'):
						living_space = True
					person = Fellow(firstname,lastname,living_space)
				else:
					person = Staff(firstname,lastname)

				self.people.append(person)
			  	Util.print_line(person.name() + ' succesfully created')
			  	self.allocate(person,None,'OFFICE')
	  			if person.is_fellow():
	  				self.allocate(person)
		  	self.save_state_to_pickle()

	def get_db_name(self, args):
		"""
		Return specified db name from arguments if available.
		Return amity if --db options is not specified
		"""

		db_name = 'amity'
		if args['--db']:
			db_name = args['--db']

		return db_name

	def save_state(self, args):
		"""
		Installs necessary tables if not created.
		Saves current state to specified sqlite db name
		"""

		db_name = self.get_db_name(args)
		migrate = Migration(db_name)
		if self.settings['drop_db']:
			migrate.drop()
			self.settings['drop_db'] = False
			self.util.file_manager.set_file_location('config.pkl')
			self.util.file_manager.pickle_dump(self.settings)

		migrate.install()
		self.save_room_state(db_name, args['-v'])
		self.save_people_state(db_name, args['-v'])
		Util.print_line('All records saved successfully')

	def save_room_state(self, db_name='amity', showLog = False):
		"""Saves current rooms state to sqlite and deletes rooms pickle file"""

		if len(self.rooms) == 0:
			Util.print_line('No room to save')
			return False

		for room in self.rooms:
			room.util.db.set_db(db_name)
			if room.save():
				if showLog:
					Util.print_line(room.name + ' save!')
			else:
				if showLog:
					Util.print_line(room.name + ' already exists')

		self.util.file_manager.set_file_location('rooms.pkl')
		self.util.file_manager.remove()

	def load_room_state(self, db_name='amity'):
		"""Loads room state from sqlite db"""

		self.util.db.table_name = 'room'
		rooms = self.util.db.find_all()
		if not rooms:
			Util.print_line('No rooms record found')
			return False
			
		for row in rooms:
			if row['type'] == 'OFFICE':
				room = Office(str(row['name']))
			else:
				room = LivingSpace(str(row['name']))

			if int(row['allocated']) > 0:
				self.util.db.table_name = 'person'
				people = self.util.db.execute('SELECT * FROM person WHERE assigned_room LIKE "%'+ room.name +'%"')
				for item in people:
					person = self.get_person(item)
					room.allocate(person,False)
			self.rooms.append(room)
		return True

	def get_person(self, row):
		"""Creates person instance based on person type"""

		living_space = False
		if row['living_space'] == 1:
			living_space = True

		if row['person_type'] == 'FELLOW':
			person = Fellow(str(row['firstname']),str(row['lastname']),living_space)
		else:
			person = Staff(str(row['firstname']),str(row['lastname']),living_space)


		if row['assigned_room']:
			key_value_pairs = row['assigned_room'].split('=')
			for i in xrange(len(key_value_pairs) - 1):
				keys = key_value_pairs[i].split(',')
				values = key_value_pairs[i + 1].split(',')
				for index in xrange(len(keys)):
					person.assigned_room[str(keys[index])] = str(values[index])

		person.date_time = row['date_time']
		return person

	def load_people_state(self, db_name='amity'):
		"""Loads people state from sqlite db"""

		self.util.db.table_name = 'person'
		people = self.util.db.find_all()
		if not people:
			Util.print_line('No people record found')
			return False

		for row in people:
			person = self.get_person(row)
			if row['allocated'] == 1:
				person.is_allocated = True

			self.people.append(person)
		return True

	def save_people_state(self, db_name='amity', showLog = False):
		"""Saves people state to sqlite db"""

		if len(self.people) == 0:
			Util.print_line('No person to save')
			return False
			
		for person in self.people:
			person.util.db.set_db(db_name)
			if person.save():
				if showLog:
					Util.print_line(person.name() + ' save!')
			else:
				if showLog:
					Util.print_line(person.name() + ' already exists')

		self.util.file_manager.set_file_location('people.pkl')
		self.util.file_manager.remove()

	def load_state(self, args):
		"""Loads people and room records from sqlite database and save it to a pickle file"""

		db_name = self.get_db_name(args)
		if self.people or self.rooms:
			Util.print_line('You have unsaved changes')
			answer = Util.prompt('do you wish to discard? Y/N ')
			if answer.upper() == 'N':
				return False

		self.drop_pickle_files()
		if self.load_room_state(db_name) and self.load_people_state(db_name):
			self.settings['drop_db'] = True
			self.save_state_to_pickle()
			Util.print_line('Data loaded')
		
	def clear(self, args):
		"""Removes the rooms and people pickle files"""

		self.drop_pickle_files()
		Util.print_line('Data Cleared')
		
		





	  

