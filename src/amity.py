from src.fellow import Fellow
from src.staff import Staff
from src.office import Office
from src.livingspace import LivingSpace
from src.fileman import FileMan
from src.util import Util
from src.migration import Migration
from src.db import Db

class Amity(FileMan):
	"""This is the entry point of the application"""

	rooms = [] #this will hold all available rooms
	people = [] #this will hold all available person
	exception_room = ''
	setting = {'drop_db':False}

	def __init__(self, command):
		Util.clear_screen() #clears the terminal
		self.command = command
		self.load_people_from_pickle()
		self.load_rooms()
		self.load_settings()

	def load_people_from_pickle(self):
		"""loads people from pickle file"""
		
		self.set_file_location('people.pkl')
		people = self.pickle_load()
		if not people:
			people = []
		self.people = people
		
	def load_settings(self):
		"""loads settings from pickle file"""
		self.set_file_location('config.pkl')
		settings = self.pickle_load()
		if not settings:
			settings = {'drop_db':False}
		self.settings = settings
		
	def load_rooms(self):
		"""loads rooms from pickle file"""

		self.set_file_location('rooms.pkl')
		rooms = self.pickle_load()
		if not rooms:
			rooms = []
		self.rooms = rooms
	
	def allocate(self,person,room_name = None):
		"""allocates person to a room based on room_name, exception_room or random"""

		if person.person_type == 'FELLOW' and person.living_space == False:
			return False

		if len(self.rooms) == 0:
			print 'No room available'
			return False
		for room in self.rooms:
			if room.name == self.exception_room:
				continue

			if room_name != None:
				if room.name.lower() != room_name.lower():
					continue

			if room.allocate(person):
				person.is_allocated = True
				person.assigned_room = room.name
				print person.name() + ' allocated to '+ room.name
				return True 
		else:
			print room_name + ' room is not available'
			return False
	
	def save_state_to_pickle(self):
		"""save current state to pickle file"""
		self.set_file_location('people.pkl')
		self.pickle_dump(self.people)
		self.set_file_location('rooms.pkl')
		self.pickle_dump(self.rooms)
		self.set_file_location('config.pkl')
		self.pickle_dump(self.settings)

	def drop_pickle_files(self):
		"""removes all pickle file except config """
		self.set_file_location('people.pkl')
		self.remove()
		self.set_file_location('rooms.pkl')
		self.remove()
		self.people = []
		self.rooms = []
		 
	def run_command(self,args):
		"""gets the required method and calls the method with the arguments passed as parameter"""
		method = getattr(self,self.command)
		method(args)	

	def add_person(self,args):
		"""resolves the argument and creates the right person type, 
		adds the person to people list and allocates the person to a room. 
		This also saves the current state to pickle file"""
		firstname = args['<firstname>'].upper()
		lastname = args['<lastname>'].upper()
		if args['<person_type>'].upper() == 'FELLOW':
			person = Fellow(firstname,lastname,args['-w'])
	  	else:
	  		person = Staff(firstname,lastname,args['-w'])

	  	self.people.append(person)
	  	print person.name() + ' successfully created'
	  	self.allocate(person)
	  	self.save_state_to_pickle()
	  	self.list_people()

	def list_people(self,args):
		"""displays the list of available people based on options specified (-u or -a)"""
		Util.print_two_line('LIST OF AVAILABLE PEOPLE')
		if len(self.people) == 0:
			Util.print_line('No person found')
			return False

		Util.print_two_line('S/N -> ID -> Firstname -> Lastname -> Type -> Living Space -> Allocated -> datetime')
		for index,person in enumerate(self.people):
			if args['-u']:
				if len(person.assigned_room) != 0:
					continue

			if args['-a']:
				if len(person.assigned_room) == 0:
					continue

			print (index + 1),person.uid,person.full_details()
			Util.print_divider()

	def list_rooms(self,args = {}):
		"""displays the list of available rooms"""
		Util.print_two_line('LIST OF AVAILABLE ROOMS')
		if len(self.rooms) == 0:
			Util.print_line('No room found')
			return False

		for index,room in enumerate(self.rooms):
			print index,room.nameplate()
			Util.print_divider()

	def print_allocations(self,args):
		"""displays the list of current allocations.
		exports allocations to file if file name is specified"""
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

	def print_unallocated(self,args):
		""" calls print_unallocated_people method if no -r options.
		 calls print_unallocated_room if -r option is specified."""
		if args['-r']:
			Util.print_line('LIST OF UNALLOCATED ROOMS')
			self.print_unallocated_room(args)
		else:
			Util.print_line('LIST OF UNALLOCATED PEOPLE')
			self.print_unallocated_people(args)

	def print_unallocated_room(self,args):
		"""displays unallocated rooms.
		exports list to file if file name is specified"""
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

	def print_unallocated_people(self,args):
		"""displays unallocated people.
		exports list to file if file name is specified"""
		if len(self.people) == 0:
			Util.print_line('No person found')
			return False
		
		counter = 0	
		if args['-o']:
			self.send_people_allocations_to_file(args['<file_name>'],False)
		else:
			for person in self.people:
				if len(person.assigned_room) == 0:
					counter += 1
					Util.print_line(person.full_details())

			if counter > 0:
				Util.print_line(str(counter) + ' unallocated person')
			else:
				Util.print_line('No unallocated person')

	def print_room(self,args):
		"""displays the room details and the list of allocated person"""
		for room in self.rooms:
			if room.name.lower() == args['<name_of_room>'].lower():
				room.people_list_with_room_name()
				break
		else:
			Util.print_line(args['<name_of_room>'] + ' room not found')

	def send_room_allocations_to_file(self,file_name,allocated = True):
		"""exports room allocations to specified file name"""
		records = ''
		for room in self.rooms:
			if len(room.people) != 0 and allocated:
				records += room.people_list_with_room_name(False)
			elif not allocated and len(room.people) == 0:
				records += room.nameplate() + '\n'

		self.set_file_location(file_name)
		self.replace(records)
		Util.print_line('records successfully exported to data/' + file_name)

	def send_people_allocations_to_file(self,file_name,allocated = True):
		"""send people fulldetails based on allocation status to specified file name"""
		records = ''
		for person in self.people:
			if len(person.assigned_room) != 0 and allocated:
				records += person.full_details() + '\n'
			elif not allocated and len(person.assigned_room) == 0:
				records += person.full_details() + '\n'

		self.set_file_location(file_name)
		self.replace(records)
		Util.print_line('records successfully exported to data/' + file_name)

	def create_room(self,args):
		"""Creates room(s) and save to pickle"""
		room_names = args['<room_name>']
		room_types = args['<room_type>']
		for name,room_type in zip(room_names,room_types):
			if room_type.upper() == 'OFFICE':
			  room = Office(name.upper())
			else:
			  room = LivingSpace(name.upper())
			self.rooms.append(room)
			print room.name + ' successful created'
		self.save_state_to_pickle()
		self.list_rooms()

	def reallocate_person(self,args):
		"""reallocate person from one room to another"""
		room_name = args['<new_room_name>'].upper()
		person_id = args['<person_id>'].upper()
		person = self.get_person_by_uid(person_id)
		if not person:
			print 'no person with ID: ' + person_id
			self.list_people()
			return False

		if not person.is_allocated:
			print person.name() + ' has not been allocated to a room'
			answer = Util.prompt('Do you want to allocate ' + person.name() + ' to ' + room_name + '? Y/N: ')
			if answer == 'N':
				return False

		if person.assigned_room == room_name:
			Util.print_line('You cannot reallocate ' + person.name() + ' to the same room')
			return False

		room = self.remove_person_from_room(person)
		if not self.allocate(person,room_name):
			if room != False:
				room.allocate(person)

		self.save_state_to_pickle()

	def allocate_person(self,args):
		"""allocate person to a room"""
		room_name = args['<new_room_name>'].upper()
		person_id = args['<person_id>'].upper()
		person = self.get_person_by_uid(person_id)
		if not person:
			print 'no person with ID: ' + person_id
			self.list_people()
			return False

		if person.is_allocated:
			print person.name() + ' has been allocated to a room'
			return False

		if args['-w']:
			person.living_space = True

		if not self.allocate(person,room_name):
			Util.print_two_line('Unable to allocate ' + person.name())

		self.save_state_to_pickle()

	def get_person_by_uid(self,uid):
		"""return person instance with corresponding uid"""
		for person in self.people:
			if person.uid == uid:
				return person
		return False

	def remove_person_from_room(self,person):
		"""remove person from a room"""

		for room in self.rooms:
		  	if len(room.people) == 0:
		  		continue

		  	#check if the user exists in the room and remove it
		  	for index,room_person in enumerate(room.people):
		  		if room_person.uid == person.uid:
		  			room.people.pop(index)
		  			self.exception_room = room.name
		  			print person.name() + ' has been removed from ' +room.name
		  			return room

		return False

	def load_people(self,args):
		"""creates people from a specified file and allocates each person based on person type"""
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
			  	print 'person created'
			  	self.allocate(person)
		  	self.save_state_to_pickle()
		  	self.list_people()

	def get_db_name(self,args):
		"""return specified db name from arguments if available.
		return amity if --db options is not specified"""
		db_name = 'amity'
		if args['--db']:
			db_name = args['--db']

		return db_name

	def save_state(self,args):
		"""installs necessary tables if not created.
		saves current state to specified sqlite db name"""
		db_name = self.get_db_name(args)
		migrate = Migration(db_name)
		if self.settings['drop_db']:
			migrate.drop()
			self.settings['drop_db'] = False
			self.set_file_location('config.pkl')
			self.pickle_dump(self.settings)

		migrate.install()
		self.save_room_state(db_name)
		self.save_people_state(db_name)

	def save_room_state(self,db_name = 'amity'):
		"""saves current rooms state to sqlite and deletes rooms pickle file"""
		if len(self.rooms) == 0:
			Util.print_line('No room to save')
			return False

		for room in self.rooms:
			room.set_db(db_name)
			if room.save():
				Util.print_line(room.name + ' save!')

		self.set_file_location('rooms.pkl')
		self.remove()

	def load_room_state(self,db_name = 'amity'):
		"""loads room state from sqlite db"""
		db = Db(db_name,'room')
		rooms = db.find_all()
		if not rooms:
			Util.print_line('No rooms record found')
			return False
			
		for row in rooms:
			if row['type'] == 'OFFICE':
				room = Office(str(row['name']))
			else:
				room = LivingSpace(str(row['name']))

			if int(row['allocated']) > 0:
				db.table_name = 'person'
				people = db.find_by_attr({'assigned_room':room.name})
				for item in people:
					person = self.get_person(item)
					room.allocate(person)
			self.rooms.append(room)

		self.list_rooms()

	def get_person(self,row):
		"""creates person instance based on person type"""
		living_space = False
		if row['living_space'] == 1:
			living_space = True

		if row['person_type'] == 'FELLOW':
			person = Fellow(str(row['firstname']),str(row['lastname']),living_space)
		else:
			person = Staff(str(row['firstname']),str(row['lastname']),living_space)

		person.assigned_room = row['assigned_room']
		person.date_time = row['date_time']
		return person

	def load_people_state(self,db_name = 'amity'):
		"""loads people state from sqlite db"""
		db = Db(db_name,'person')
		people = db.find_all()
		if not people:
			Util.print_line('No people record found')
			return False

		for row in people:
			person = self.get_person(row)
			if row['allocated'] == 1:
				person.is_allocated = True

			self.people.append(person)

		self.list_people()

	def save_people_state(self,db_name = 'amity'):
		"""saves people state to sqlite db"""
		if len(self.people) == 0:
			Util.print_line('No person to save')
			return False
			
		for person in self.people:
			person.set_db(db_name)
			if person.save():
				Util.print_line(person.name() + ' save!')

		self.set_file_location('people.pkl')
		self.remove()

	def load_state(self,args):
		"""loads people and room records from sqlite database and save it to a pickle file"""
		db_name = self.get_db_name(args)
		if len(self.people) != 0 or len(self.rooms) != 0:
			Util.print_line('You have unsaved changes')
			answer = Util.prompt('do you wish to discard? Y/N ')
			if answer.upper() == 'N':
				return False

		self.drop_pickle_files()
		self.load_room_state(db_name)
		self.load_people_state(db_name)
		self.settings['drop_db'] = True
		self.save_state_to_pickle()





	  

