from person import Person
from room import Room
from util import Util

class AllocationApp(object):
	"""This is the entry point of the application"""

	default_rooms = [
	{'name':'Iroko','type':'L'},
	{'name':'Oaks','type':'L'},
	{'name':'Maple','type':'L'},
	{'name':'Pine','type':'L'},
	{'name':'Redcedar','type':'L'},
	{'name':'Sassafras','type':'L'},
	{'name':'Shadbush','type':'L'},
	{'name':'Spruce','type':'L'},
	{'name':'Sycamore','type':'L'},
	{'name':'Tulip','type':'L'},
	{'name':'Walnut','type':'O'},
	{'name':'Cashew','type':'O'},
	{'name':'Mango','type':'O'},
	{'name':'Orange','type':'O'},
	{'name':'Pear','type':'O'},
	{'name':'Willow','type':'O'},
	{'name':'Ash','type':'O'},
	{'name':'Aspen','type':'O'},
	{'name':'Cherry','type':'O'},
	{'name':'Elm','type':'O'}
	]
	rooms = [] #this will hold all available rooms
	people = [] #this will hold all available person

	def __init__(self,name):
		self.name = name
		self.populateRooms()
		self.loadPeople()


	def populateRooms(self):
		"""populates rooms"""
		for item in self.default_rooms:
			room = Room(item['name'],item['type'])
			self.rooms.append(room)


	def loadPeople(self):
		path = '../data/people.txt'
		if not Util.isfile(path):
			Util.printline('you do not have people.txt in the data folder')
			return False

		with open(path,'r') as file:
			for line in file:
				records = line.split()
				living_space = False
				name = records[0] + ' ' + records[1]
				person_type = records[2]
				if person_type == 'FELLOW':
					if(records[3] == 'Y'):
						living_space = True

				person = Person(name,person_type,living_space)
				self.people.append(person)
				self.allocatePerson(person)

	def allocatePerson(self,person):
		for room in self.rooms:
			if room.room_type == 'L':
				if room.is_filled == False:
					return room.allocate(person)

	def listpeople(self):
		for person in self.people:
			records =  person.name,person.person_type,person.living_space
			print records


app = AllocationApp('sunday')
app.listpeople()