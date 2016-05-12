import os
import os.path
from tabulate import tabulate
from src.db import Db
from src.fileman import FileMan

class Util(object):
	"""This class contains utility methods."""

	def __init__(self):
		self.db = Db()
		self.file_manager = FileMan('')

	@staticmethod
	def is_file(file_path):
		return os.path.isfile(file_path) 

	@staticmethod
	def print_line(message):
		print message
		Util.print_divider()

	@staticmethod
	def print_two_line(message):
		Util.print_divider()
		print message
		Util.print_divider()

	@staticmethod
	def prompt(message):
		return raw_input(message)

	@staticmethod
	def get_base_path():
		return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	@staticmethod
	def clear_screen():
		os.system('clear')
		Util.welcome()

	@staticmethod
	def print_divider():
		print Util.line()
	
	@staticmethod
	def tabulate(data):
		print Util.get_table(data)
	
	@staticmethod
	def get_table(data):
		return tabulate(data, headers="firstrow", tablefmt="pipe")
	
	@staticmethod
	def line():
		return '---------------------------------------------------------------------------\n'
	
	@staticmethod
	def welcome():
		Util.print_divider()
		print '                     WELCOME TO ALLOCATION APP                               '
		print '           One stop solution for room allocation management                  '
		Util.print_divider()
