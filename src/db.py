import sqlite3

class Db(object):
	"""Database manipulation"""
	name = 'amity.db'

	def __init__(self):
		self.connection = sqlite3.connect(self.name)
		