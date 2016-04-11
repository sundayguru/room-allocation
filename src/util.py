import os.path

class Util(object):

	@staticmethod
	def isfile(file_path):
		return os.path.isfile(file_path) 

	@staticmethod
	def printline(message):
		print '---------------------------------------------------------------------------'
		print message
		print '---------------------------------------------------------------------------'