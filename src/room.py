class Room(object):
	""" room allocation """
	capacity = 4

	def __init__(self,name,room_type):
		self.name = name
		self.room_type = room_type
		self.setCapacity()

	def setCapacity(self):
		if self.room_type == 'O':
			self.capacity = 6