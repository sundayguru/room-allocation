from db import Db
from fileman import FileMan
class Person(Db,FileMan):
	""" this will manage people creation"""
	is_allocated = False
	person_type = None
	state_dict = {0:'NO',1:'YES'}

	def __init__(self,firstname,lastname,living_space = False):
		if type(firstname) != str or type(lastname) != str or type(living_space) != bool:
			raise ValueError

		self.firstname = firstname
		self.lastname = lastname
		self.living_space = living_space


	def fulldetails(self):
		return self.name() + ' ' + self.person_type + ' ' + self.getstatedict(self.living_space) + ' ' + self.getstatedict(self.is_allocated)


	def getdetailsdict(self):
		return {
		'firstname':self.firstname,
		'lastname':self.lastname,
		'allocation':self.transalate(self.living_space),
		'allocated':self.transalate(self.is_allocated),
		'person_type':self.person_type,
		}

	def getstatedict(self,state):
		"""returns corresponding value in state_dict """
		try:
			return self.state_dict[state]
		except:
			return self.state_dict[0]

	def transalate(self,status):
		if status:
			return 1
		else:
			return 0

	def name(self):
		return self.firstname + ' ' + self.lastname

	def allocate(self):
		file = FileMan('room.pkl')
		rooms = file.pickleload()
		if not rooms:
			print 'No room available'
			return False
		for room in rooms:
			if room.allocate(self):
				print 'Person allocated to '+ room.name
				return True
		else:
			print 'No room available'
			return False

	def process(self):
		self.setfilelocation('people.pkl')
		people = self.pickleload()
		if not people:
			people = []

		if self.allocate():
			self.is_allocated = True
			
		people.append(self)
		self.pickledump(people)
		return True

