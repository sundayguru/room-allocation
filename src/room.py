from db import Db
from person import Person
from fileman import FileMan
from util import Util
class Room(Db,FileMan):
	""" room allocation """
	capacity = 4
	people = []
	is_filled = False
	error_message = ''

	def __init__(self,name):
		if type(name) != str:
			raise ValueError

		self.name = name
		self.people = []

	def allocate(self,person):
		"""allocates person to a room"""
		if not self.allocate_able(person):
			self.error_message = person.name() + ' cannot be allocated to ' + self.name
			return False

		if(len(self.people) == self.capacity):
			self.is_filled = True

		if self.is_filled == True:
			self.error_message = self.name + ' is occupied'
			return False
			
		self.people.append(person)
		return True

	def people_list_with_room_name(self,output = True):
		"""build data of room details and the people allocated to it.
		returns the data or outputs it if output parameter is set to True"""
		data = self.nameplate() + '\n'
		members = ''
		for person in self.people:
			members += person.name() + ', '
		
		data += members[:-2] + '\n'
		
		return data if not output else Util.print_line(data)



	def allocate_able(self,person):
		"""checks if person can be allocated"""
		if(person.person_type == 'STAFF' and self.room_type == 'OFFICE'):
			return True
		elif(person.person_type == 'FELLOW' and self.room_type == 'LIVINGSPACE'):
			if(person.living_space == True):
				return True

			return False
		else:
			return False

	def nameplate(self):
		"""returns room name and type as string"""
		return self.name + ' (' + self.room_type + ')'

	def save(self):
		"""saves rooms details o sqlite db"""
		data = {
		'name':self.name,
		'capacity':self.capacity,
		'type':self.room_type,
		'allocated':len(self.people),
		}
		return self.create(data)