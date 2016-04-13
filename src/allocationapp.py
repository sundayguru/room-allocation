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
	commands = {
	'LP':{'method':'listpeople','param_type':bool},
	'LR':{'method':'listallocation','param_type':bool},
	'Q':{'method':'exit','param_type':None},
	}
	rooms = [] #this will hold all available rooms
	people = [] #this will hold all available person

	def __init__(self,name):
		self.name = name
		self.populateRooms()
		self.loadPeople()

	def startapp(self):
		"""this will kick start the application"""
		Util.clearscreen()
		name = Util.prompt('Your name: ')
		while len(name) == 0:
			Util.printline('name is required to use this application')
			name = Util.prompt('Your name: ')
		else:
			self.name = name

		Util.showstarttips()
		self.getcommand()


	def getcommand(self):
		"""prompt for user input and run the command issued"""
		command = Util.starttipscommandlistener()
		self.runcommand(command)

	def runcommand(self,command):
		"""resolve inputs from prompt and execute the right method"""
		Util.clearscreen()
		args = command.split()
		if(len(args) != 0):
			if(args[0] in self.commands):
				command_params = self.commands[args[0]]
				method = getattr(self,command_params['method'])
				try:
					param = args[1]
					if command_params['param_type'] == bool:
						if param == '-A':
							param = True
						elif param == '-U':
							param = False
						else:
							Util.printtwoline('Invalid parameter ('+param+') for command type ('+args[0]+')')
							self.getcommand()
							return False

					method(param)
				except:
					method()
					
				if(args[0] != 'Q'):
					self.getcommand()
			else:
				Util.printtwoline('Invalid command type ('+command+')')
				self.getcommand()
		else:
			"""edge case, this may not happen"""
			Util.printtwoline('Unknown Input error')
			self.getcommand()


	def populateRooms(self):
		"""populates rooms"""
		for item in self.default_rooms:
			room = Room(item['name'],item['type'])
			self.rooms.append(room)


	def loadPeople(self):
		path = 'data/people.txt'
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
				if self.allocatePerson(person):
					person.is_allocated = True

	def allocatePerson(self,person):
		for room in self.rooms:
			if room.room_type == 'L':
				if room.is_filled == False:
					return room.allocate(person)

	def listpeople(self,allocated = None):
		Util.printline('Name   -> Type   -> Living Space  -> Allocated')
		for person in self.people:
			if allocated == None:
				Util.printline(person.fulldetails())
			else:
				if person.is_allocated == allocated:
					Util.printline(person.fulldetails())
		Util.printdivider()

	def listallocation(self,allocated = None):
		for room in self.rooms:
			if allocated == True:
				if room.people == []:
					continue

			print room.nameplate()
			if len(room.people) > 0 :
				for person in room.people:
					print person.name + ', ',
				print '\n'
			else:
				Util.printline('not allocated')

	def roomlistpeople(self, room_name):
		found = False
		for room in self.rooms:
			if room.name.lower() != room_name.lower():
				continue

			print room.nameplate()
			if len(room.people) > 0 :
				for person in room.people:
					print person.name + ', ',
				print '\n'
			else:
				Util.printline('not allocated')
			found = True

		if found == False:
			Util.printline('Oops, we are unable to locate a room called ' + room_name)

	def exit(self):
		Util.printdivider()
		print '                     THANK YOU FOR USING OUR SOLUTION                        '
		rating = Util.prompt('Rate This app (scale of 1 to 10):')
		with open('data/rating.txt','r+') as file:
			file.read()
			data = 'Rating from ' + self.name + ': ' + rating + '\n'
			file.write(data)

		Util.printdivider()

