import os
from os import path
from util import Util

class FileMan(object):
	"""FileMan reads and write to file"""

	def __init__(self, filename):
		self.file_location = Util.getbasepath() + '/data/' + filename

	def read(self):
		if not Util.isfile(self.file_location):
			Util.printline('make this file is in data folder')
			return False

		data = []
		with open(self.file_location,'r') as file:
			for line in file:
				data.append(line)
			return data

	def write(self,data):
		with open(self.file_location,'a+') as file:
			file.read()
			file.write(data)

	def replace(self,data):
		with open(self.file_location,'w') as file:
			file.write(data)

	def remove(self):
		return os.remove(self.file_location)
