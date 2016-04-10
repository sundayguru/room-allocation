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
