from src.fellow import Fellow
from src.staff import Staff
from src.office import Office
from src.livingspace import LivingSpace
from src.fileman import FileMan

class Amity(FileMan):
	"""This is the entry point of the application"""

	rooms = [] #this will hold all available rooms
	people = [] #this will hold all available person
	exception_room = ''

	def __init__(self, command):
		self.command = command
		self.load_people()
		self.load_rooms()

	def load_people(self):
		"""loads people from pickle file"""
		self.setfilelocation('people.pkl')
		people = self.pickleload()
		if not people:
			people = []
		self.people = people
		
	def load_rooms(self):
		"""loads rooms from pickle file"""

		self.setfilelocation('rooms.pkl')
		rooms = self.pickleload()
		if not rooms:
			rooms = []
		self.rooms = rooms
	
	def allocate(self,person,room_name = None):
		"""allocates person to a room based room_name, exception_room or random"""

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
				print 'Person allocated to '+ room.name
				return True
		else:
			print 'No room available'
			return False
	

	def save_state_to_pickle(self):
		"""save current state to pickle file"""
		self.setfilelocation('people.pkl')
		self.pickledump(self.people)
		self.setfilelocation('rooms.pkl')
		self.pickledump(self.rooms)


	def run_command(self,args):
		method = getattr(self,self.command)
		try:
			method(args)
		except:
			print 'method not implemented'

	def add_person(self,args):
		if args['<person_type>'].upper() == 'FELLOW':
			person = Fellow(args['<firstname>'],args['<lastname>'],args['-w'])
	  	else:
	  		person = Staff(args['<firstname>'],args['<lastname>'],args['-w'])

	  	self.people.append(person)
	  	print 'person created'
	  	self.allocate(person)
	  	self.save_state_to_pickle()
	  	self.list_people()

	def list_people(self):
		for index,person in enumerate(self.people):
			print (index + 1),person.uid,person.fulldetails()

	def list_rooms(self):
		for index,room in enumerate(self.rooms):
			print index,room.nameplate()

	def create_room(self,args):
	  room_names = args['<room_name>']
	  room_types = args['<room_type>']
	  for name,room_type in zip(room_names,room_types):
	    if room_type.upper() == 'OFFICE':
	      room = Office(name)
	    else:
	      room = LivingSpace(name)
	    self.rooms.append(room)
	    print room.name + ' successful created'
	  self.save_state_to_pickle()
	  self.list_rooms()

	def reallocate_person(self,args):
		"""reallocate person from one room to another"""
		room_name = args['<room_name>']
		person_id = args['<person_id>']
		person = self.get_person_by_uid(person_id)
		if not person:
			print 'no person with ID: '+person_id
			return False

		if not person.is_allocated:
			print person.name() + ' has not been allocated to a room'
			return False

		self.remove_person_from_room(person)
		self.allocate(person,room_name)
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
		  			print person.name() + 'has been removed from ' +room.name
		  			return True

		return False



	  
