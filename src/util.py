import os
import os.path


class Util(object):


	@staticmethod
	def isfile(file_path):
		return os.path.isfile(file_path) 

	@staticmethod
	def printline(message):
		Util.printdivider()
		print message
		Util.printdivider()


	@staticmethod
	def prompt(message):
		return raw_input(message)

	@staticmethod
	def clearscreen():
		os.system('clear')

	@staticmethod
	def starttipscommandlistener():
		command = Util.prompt('Enter Command: ')
		while len(command) == 0:
			Util.printline('Invalid Command')
			Util.showstarttips()
			command = Util.prompt('Enter Command: ')
		else:
			return command.upper()

	@staticmethod
	def printdivider():
		print '---------------------------------------------------------------------------'
		
	@staticmethod
	def showstarttips():
		Util.printline('INSTRUCTIONS');
		print 'COMMAND           DESCRIPTION'
		print 'LP          List all people'
		print 'LP -A       List all allocated people'
		print 'LP -U       List all unallocated people'
		print 'LR          List all rooms'
		print 'LR -A       List all allocations'
		print 'LR -U       List all unallocated rooms'
		print 'AP          Add people'
		print 'AR          Add Room'
		print 'I           Show this instructions again'
		Util.printdivider()

	@staticmethod
	def welcome():
		Util.printdivider()
		Util.printdivider()
		print '                     WELCOME TO ALLOCATION APP                               '
		print '           One stop solution for room allocation management                  '
		Util.printdivider()
		Util.printdivider()
