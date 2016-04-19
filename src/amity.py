from src.fellow import Fellow
from src.staff import Staff
from src.office import Office
from src.livingspace import LivingSpace
from src.fileman import FileMan

class Amity(FileMan):
	"""This is the entry point of the application"""

	rooms = [] #this will hold all available rooms
	people = [] #this will hold all available person

	def __init__(self, command):
		self.command = command
		self.load_people()
		self.load_rooms()

	def load_people(self):
		self.setfilelocation('people.pkl')
		people = self.pickleload()
		if not people:
			people = []
		self.people = people
		
	def load_rooms(self):
		self.setfilelocation('rooms.pkl')
		rooms = self.pickleload()
		if not rooms:
			rooms = []
		self.rooms = rooms
	
	def allocate(self,person):
		if person.person_type == 'FELLOW' and person.living_space == False:
			return False

		if len(self.rooms) == 0:
			print 'No room available'
			return False
		for room in self.rooms:
			if room.allocate(person):
				print 'Person allocated to '+ room.name
				return True
		else:
			print 'No room available'
			return False
	

	def save_state_to_pickle(self):
		self.setfilelocation('people.pkl')
		self.pickledump(self.people)
		self.setfilelocation('rooms.pkl')
		self.pickledump(self.rooms)


	def run_command(self,args):
		method = getattr(self,self.command)
		method(args)

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
			print index,person.fulldetails()

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

	def reallocate_person(args):
	  room_id = args['<room_id>']
	  person_id = args['<person_id>']
	  print person_id,room_id

