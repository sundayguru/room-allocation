import os
from os import path
import pickle
from util import Util

class FileMan(object):
	"""FileMan reads and write to file"""

	def __init__(self, filename):
		if type(filename) != str:
			raise ValueError
			
		self.setfilelocation(filename)


	def setfilelocation(self,filename):
		self.file_location = Util.getbasepath() + '/data/' + filename


	def read(self):
		"""
		reads a file and return content in a list
		returns False is path is not a file
		"""
		if not self.validate():
			return False

		data = []
		with open(self.file_location,'r') as file:
			for line in file:
				data.append(line[:-1])
			return data

	def write(self,data):
		"""appends content to a file"""
		if type(data) != str:
			raise ValueError

		with open(self.file_location,'a+') as file:
			file.read()
			file.write(data+'\n')

	def replace(self,data):
		"""replaces content of a file"""
		if type(data) != str:
			raise ValueError
			
		with open(self.file_location,'w') as file:
			file.write(data+'\n')

	def remove(self):
		"""deletes file"""
		if not self.validate():
			return False

		return os.remove(self.file_location)

	def validate(self):
		"""validates the existence of a give file location"""
		if not Util.isfile(self.file_location):
			Util.printline('make this file is in data folder')
			return False
		return True

	def pickledump(self,data):
		"""dumps data structure into a file"""
		with open(self.file_location,'wb') as file:
			pickle.dump(data, file)
		return True

	def pickleload(self):
		"""load data structure from a file"""
		with open(self.file_location,'rb') as file:
			return pickle.load(file)
