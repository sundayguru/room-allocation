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
		Util.clearscreen()
		self.command = command
		self.load_people_from_pickle()
		self.load_rooms()
		self.load_settings()
		print Util.getbasepath()

	def load_people_from_pickle(self):
		"""loads people from pickle file"""
		
		self.setfilelocation('people.pkl')
		people = self.pickleload()
		if not people:
			people = []
		self.people = people
		
	def load_settings(self):
		"""loads settings from pickle file"""
		self.setfilelocation('config.pkl')
		settings = self.pickleload()
		if not settings:
			settings = {'drop_db':False}
		self.settings = settings
		
	def load_rooms(self):
		"""loads rooms from pickle file"""

		self.setfilelocation('rooms.pkl')
		rooms = self.pickleload()
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
		self.setfilelocation('people.pkl')
		self.pickledump(self.people)
		self.setfilelocation('rooms.pkl')
		self.pickledump(self.rooms)
		self.setfilelocation('config.pkl')
		self.pickledump(self.settings)

	def drop_pickle_files(self):
		"""removes all pickle file except config """
		self.setfilelocation('people.pkl')
		self.remove()
		self.setfilelocation('rooms.pkl')
		self.remove()
		self.people = []
		self.rooms = []
		 
	def run_command(self,args):
		method = getattr(self,self.command)
		method(args)	

	def add_person(self,args):
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

	def list_people(self,args = {}):
		Util.printtwoline('LIST OF AVAILABLE PEOPLE')
		if len(self.people) == 0:
			Util.printline('No person found')
			return False

		Util.printtwoline('S/N -> ID -> Firstname -> Lastname -> Type -> Living Space -> Allocated')
		for index,person in enumerate(self.people):
			print (index + 1),person.uid,person.fulldetails()
			Util.printdivider()

	def list_rooms(self,args = {}):
		Util.printtwoline('LIST OF AVAILABLE ROOMS')
		if len(self.rooms) == 0:
			Util.printline('No room found')
			return False

		for index,room in enumerate(self.rooms):
			print index,room.nameplate()
			Util.printdivider()

	def print_allocations(self,args):
		Util.printline('LIST OF ALLOCATIONS')
		if len(self.rooms) == 0:
			Util.printline('No room found')
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
				Util.printline(str(counter) + ' of ' + str(len(self.rooms)) + ' room(s) allocated')
			else:
				Util.printline('No room has been allocated')

	def print_unallocated(self,args):
		if args['-r']:
			Util.printline('LIST OF UNALLOCATED ROOMS')
			self.print_unallocated_room(args)
		else:
			Util.printline('LIST OF UNALLOCATED PEOPLE')
			self.print_unallocated_people(args)

	def print_unallocated_room(self,args):
		if len(self.rooms) == 0:
			Util.printline('No room found')
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
				Util.printline(str(counter) + ' unallocated room(s)')
			else:
				Util.printline('No unallocated room')

	def print_unallocated_people(self,args):
		if len(self.people) == 0:
			Util.printline('No person found')
			return False
		
		counter = 0	
		if args['-o']:
			self.send_people_allocations_to_file(args['<file_name>'],False)
		else:
			for person in self.people:
				if len(person.assigned_room) == 0:
					counter += 1
					Util.printline(person.fulldetails())

			if counter > 0:
				Util.printline(str(counter) + ' unallocated person')
			else:
				Util.printline('No unallocated person')

	def print_room(self,args):
		for room in self.rooms:
			if room.name.lower() == args['<name_of_room>'].lower():
				room.people_list_with_room_name()
				break
		else:
			Util.printline(args['<name_of_room>'] + ' room not found')

	def send_room_allocations_to_file(self,file_name,allocated = True):
		records = ''
		for room in self.rooms:
			if len(room.people) != 0 and allocated:
				records += room.people_list_with_room_name(False)
			elif not allocated and len(room.people) == 0:
				records += room.nameplate() + '\n'

		self.setfilelocation(file_name)
		self.replace(records)
		Util.printline('records successfully exported to data/' + file_name)

	def send_people_allocations_to_file(self,file_name,allocated = True):
		records = ''
		for person in self.people:
			if len(person.assigned_room) != 0 and allocated:
				records += person.fulldetails() + '\n'
			elif not allocated and len(person.assigned_room) == 0:
				records += person.fulldetails() + '\n'

		self.setfilelocation(file_name)
		self.replace(records)
		Util.printline('records successfully exported to data/' + file_name)

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
			Util.printline('You cannot reallocate ' + person.name() + ' to the same room')
			return False

		room = self.remove_person_from_room(person)
		if not self.allocate(person,room_name):
			if room != False:
				room.allocate(person)

		self.save_state_to_pickle()
		self.list_people()

	def get_person_by_uid(self,uid):
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
		path = args['<file_location>']
		if not Util.isfile(path):
			Util.printline('File location is invalid')
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
		db_name = 'amity'
		if args['--db']:
			db_name = args['--db']

		return db_name

	def save_state(self,args):
		db_name = self.get_db_name(args)
		migrate = Migration(db_name)
		if self.settings['drop_db']:
			migrate.drop()
			self.settings['drop_db'] = False
			self.setfilelocation('config.pkl')
			self.pickledump(self.settings)

		migrate.install()
		self.save_room_state(db_name)
		self.save_people_state(db_name)

	def save_room_state(self,db_name = 'amity'):
		if len(self.rooms) == 0:
			Util.printline('No room to save')
			return False

		for room in self.rooms:
			room.set_db(db_name)
			if room.save():
				Util.printline(room.name + ' save!')

		self.setfilelocation('rooms.pkl')
		self.remove()

	def load_room_state(self,db_name = 'amity'):
		db = Db(db_name,'room')
		rooms = db.findall()
		if not rooms:
			Util.printline('No rooms record found')
			return False
			
		for row in rooms:
			if row['type'] == 'OFFICE':
				room = Office(str(row['name']))
			else:
				room = LivingSpace(str(row['name']))

			if int(row['allocated']) > 0:
				db.table_name = 'person'
				people = db.findbyattr({'assigned_room':room.name})
				for item in people:
					person = self.get_person(item)
					room.allocate(person)
			self.rooms.append(room)

		self.list_rooms()

	def get_person(self,row):
		living_space = False
		if row['living_space'] == 1:
			living_space = True

		if row['person_type'] == 'FELLOW':
			person = Fellow(str(row['firstname']),str(row['lastname']),living_space)
		else:
			person = Staff(str(row['firstname']),str(row['lastname']),living_space)

		person.assigned_room = row['assigned_room']
		return person

	def load_people_state(self,db_name = 'amity'):
		db = Db(db_name,'person')
		people = db.findall()
		if not people:
			Util.printline('No people record found')
			return False

		for row in people:
			person = self.get_person(row)
			if row['allocated'] == 1:
				person.is_allocated = True

			self.people.append(person)

		self.list_people()

	def save_people_state(self,db_name = 'amity'):
		if len(self.people) == 0:
			Util.printline('No person to save')
			return False
			
		for person in self.people:
			person.set_db(db_name)
			if person.save():
				Util.printline(person.name() + ' save!')

		self.setfilelocation('people.pkl')
		self.remove()

	def load_state(self,args):
		"""loads people and room records from sqlite database and save it to a pickle file"""
		db_name = self.get_db_name(args)
		if len(self.people) != 0 or len(self.rooms) != 0:
			Util.printline('You have unsaved changes')
			answer = Util.prompt('do you wish to discard? Y/N ')
			if answer.upper() == 'N':
				return False

		self.drop_pickle_files()
		self.load_room_state(db_name)
		self.load_people_state(db_name)
		self.settings['drop_db'] = True
		self.save_state_to_pickle()





	  

