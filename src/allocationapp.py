from src.person import Person
from src.room import Room

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


	def populateRooms(self):
		"""populates rooms"""
		for item in self.default_rooms:
			room = Room(item['name'],item['type'])
			self.rooms.append(room)


	def loadPeople(self):
		pass

	def allocatePeople(self):
		pass
