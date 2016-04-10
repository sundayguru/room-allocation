class Person(object):
	""" this will manage people creation"""
	is_allocated = False

	def __init__(self,name,person_type,living_space = False):
		self.name = name
		self.person_type = person_type
		self.living_space = living_space
