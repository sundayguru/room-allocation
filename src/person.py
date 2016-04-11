class Person(object):
	""" this will manage people creation"""
	is_allocated = False

	def __init__(self,name,person_type,living_space = False):
		if type(name) != str or type(person_type) != str or type(living_space) != bool:
			raise ValueError

		if person_type != 'FELLOW' and person_type != 'STAFF':
			raise ValueError

		self.name = name
		self.person_type = person_type
		self.living_space = living_space


	def fulldetails(self):
		return self.name + ' ' + self.person_type + ' ' + self.livingspace() + ' ' + self.isallocated()

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