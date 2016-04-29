from db import Db
from fileman import FileMan
from person import Person
from util import Util


class Room(Db,FileMan):
	"""This class manages room entity, it include people attribute that holds the list people allocated to it."""

	def __init__(self, name):

		if type(name) != str:
			raise ValueError

		self.error_message = ''
		self.name = name
		self.people = []
		self.is_filled = False

	def allocate(self, person):
		"""allocates person to a room."""

		if not self.allocate_able(person):
			self.error_message = person.name() + ' cannot be allocated to ' + self.name
			return False

		if(len(self.people) == self.capacity):
			self.is_filled = True

		if self.is_filled == True:
			self.error_message = self.name + ' is occupied'
			return False
			
		self.people.append(person)
		person.allocate(self)
		return True

	def people_list_with_room_name(self, output=True):
		"""build data of room details and the people allocated to it.
		returns the data or outputs it if output parameter is set to True."""

		data = self.nameplate() + ' ' + str(len(self.people)) + ' of ' + str(self.capacity) +'\n'
		data += Util.line()
		members = ''
		for person in self.people:
			members += person.name() + ', '
		
		data += members[:-2] + '\n'
		
		return data if not output else Util.print_line(data)



	def allocate_able(self, person):
		"""checks if person can be allocated."""
		if self.people:
			for old_person in self.people:
				if old_person.name() == person.name():
					return False

		if(person.person_type == 'STAFF' and self.room_type == 'LIVINGSPACE'):
			return False
		
		return True

	def nameplate(self):
		"""returns room name and type as string."""

		return self.name + ' (' + self.room_type + ')'

	def save(self):
		"""saves rooms details to sqlite db."""
		
		data = {
		'name':self.name,
		'capacity':self.capacity,
		'type':self.room_type,
		'allocated':len(self.people),
		}
		exists = self.find_by_attr({'name':data['name'],'type':data['type']})
		if exists:
			return False
		return self.create(data)
