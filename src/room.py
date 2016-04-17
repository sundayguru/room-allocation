from db import Db
from person import Person
class Room(Db):
	""" room allocation """
	capacity = 4
	people = []
	is_filled = False

	def __init__(self,name):
		if type(name) != str or type(room_type) != str:
			raise ValueError

		self.name = name
		self.room_type = room_type
		self.people = []

	def setCapacity(self):
		if self.room_type == 'O':
			self.capacity = 6

	def allocate(self,person):
		if type(person) != Person:
			raise ValueError

		if not self.allocateAble(person):
			return False

		if(len(self.people) == self.capacity):
			self.is_filled = True

		if self.is_filled == True:
			return False
			
		self.people.append(person)
		return True


	def allocateAble(self,person):
		if(person.person_type == 'STAFF' and self.room_type == 'O'):
			return True
		elif(person.person_type == 'FELLOW' and self.room_type == 'L'):
			if(person.living_space == True):
				return True

			return False
		else:
			return False

	def nameplate(self):
		return self.name + ' (' + self.room_type + ')'
