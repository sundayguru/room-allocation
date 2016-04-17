from db import Db
class Person(Db):
	""" this will manage people creation"""
	is_allocated = False
	person_type = None

	def __init__(self,firstname,lastname,living_space = False):
		if type(firstname) != str or type(lastname) != str or type(living_space) != bool:
			raise ValueError

		self.firstname = firstname
		self.lastname = lastname
		self.living_space = living_space


	def fulldetails(self):
		return self.name() + ' ' + self.person_type + ' ' + self.livingspace() + ' ' + self.isallocated()

	def livingspace(self):
		if self.living_space:
			return 'YES'
		else:
			return 'NO'

	def isallocated(self):
		if self.is_allocated:
			return 'YES'
		else:
			return 'NO'

	def name(self):
		return self.firstname + ' ' + self.lastname