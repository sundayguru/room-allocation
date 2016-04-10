class Room(object):
	""" room allocation """
	capacity = 4
	beds = []
	is_filled = False

	def __init__(self,name,room_type):
		if type(name) != str or type(room_type) != str:
			raise ValueError

		if room_type != 'L' and room_type != 'O':
			raise ValueError

		self.name = name
		self.room_type = room_type
		self.setCapacity()

	def setCapacity(self):
		if self.room_type == 'O':
			self.capacity = 6

	def allocate(self,person):
		self.beds.append(person)

