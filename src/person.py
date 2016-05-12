from util import Util


class Person(object):
	"""This manages person entity and contains helper methods that ease content display."""

	state_dict = {0: 'NO', 1: 'YES'}
	table_name = 'person'
	date_time = ''
	person_type = ''

	def __init__(self, firstname, lastname, living_space=False):
		if type(firstname) != str or type(lastname) != str or type(living_space) != bool:
			raise ValueError

		self.util = Util()
		self.firstname = firstname
		self.lastname = lastname
		self.living_space = living_space
		self.assigned_room = {}
		self.is_allocated = False
		self.uid = firstname[0:1] + lastname[0:1] + str(self.get_next_id())


	def get_next_id(self):
		"""
		This method will return incremental value for person id
		"""
 
		self.util.file_manager.set_file_location('people.pkl')
		people = self.util.file_manager.pickle_load()
		return len(people) + 1 if people else 1

	def full_details(self):
		"""Returns person full details as string."""

		details = self.name() + ' ' + self.person_type + ' ' + self.get_state_dict(self.living_space) 
		details += ' ' + self.get_state_dict(self.is_allocated) + ' ' + self.date_time
		return details

	def details_list(self):
		"""Returns person full details as list."""
		
		return [
			self.uid,
			self.firstname,
			self.lastname,
			self.person_type,
			self.get_state_dict(self.living_space),
			self.get_state_dict(self.is_allocated),
			self.date_time
		]


	def get_details_dict(self):
		"""Returns person full details as dictionary."""

		return {
			'firstname':self.firstname,
			'lastname':self.lastname,
			'living_space':self.transalate(self.living_space),
			'allocated':self.transalate(self.is_allocated),
			'person_type':self.person_type,
			'assigned_room':self.get_assigned_room_string(),
			'date_time':self.date_time,
		}

	def get_assigned_room_string(self):
		keys = ','.join(self.assigned_room.keys())
		values = ','.join(self.assigned_room.values())
		return keys + '=' + values

	def get_state_dict(self, state):
		"""Returns corresponding value in state_dict."""

		try:
			return self.state_dict[state]
		except:
			return self.state_dict[0]

	def transalate(self, status):
		"""This simply converts bool to int (0 or 1)."""

		if status:
			return 1
		else:
			return 0

	def name(self):
		"""Returns full name of the person."""

		return self.firstname + ' ' + self.lastname

	@staticmethod
	def headers():
		return ['S/N','ID','Firstname','Lastname','Type','Wants Accommodation','Allocated','Datetime']

	def allocate(self, room, allocated=True):
		self.is_allocated = allocated
		self.assigned_room[room.room_type] = room.name

	def save(self):
		"""Saves person into sqlite database."""
		
		data = self.get_details_dict()
		self.util.db.table_name = self.table_name
		exists = self.util.db.find_by_attr({'firstname':data['firstname'],'lastname':data['lastname'],'person_type':data['person_type']})
		if exists:
			return False
			
		return self.util.db.create(data)

	def is_fellow(self):
		return self.person_type == 'FELLOW'

	def is_staff(self):
		return self.person_type == 'STAFF'
