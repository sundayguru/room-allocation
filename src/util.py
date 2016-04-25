import os
import os.path

class Util(object):
	"""this class contains utility methods"""

	@staticmethod
	def is_file(file_path):
		return os.path.isfile(file_path) 

	@staticmethod
	def print_line(message):
		Util.print_divider()
		print message

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
	def line():
		return '---------------------------------------------------------------------------\n'
	
	@staticmethod
	def welcome():
		Util.print_divider()
		Util.print_divider()
		print '                     WELCOME TO ALLOCATION APP                               '
		print '           One stop solution for room allocation management                  '
		Util.print_divider()
		Util.print_divider()
