from db import Db
from person import Person
from fileman import FileMan
class Room(Db,FileMan):
	""" room allocation """
	capacity = 4
	people = []
	is_filled = False

	def __init__(self,name):
		if type(name) != str:
			raise ValueError

		self.name = name
		self.people = []

	def allocate(self,person):
		
		if not self.allocateAble(person):
			return False

		if(len(self.people) == self.capacity):
			self.is_filled = True

		if self.is_filled == True:
			return False
			
		self.people.append(person)
		return True


	def allocateAble(self,person):
		if(person.person_type == 'STAFF' and self.room_type == 'OFFICE'):
			return True
		elif(person.person_type == 'FELLOW' and self.room_type == 'LIVINGSPACE'):
			if(person.living_space == True):
				return True

			return False
		else:
			return False

	def nameplate(self):
		return self.name + ' (' + self.room_type + ')'
