from db import Db

class Migration(Db):
	"""docstring for Migration"""
	table_definitions = [
	'''CREATE TABLE fellow
       (ID INT PRIMARY KEY     NOT NULL,
       firstname         CHAR(255),
       lastname         CHAR(255),
       allocation       INT    NOT NULL,
       date_time         CHAR(25));
    ''',

    '''CREATE TABLE staff
       (ID INT PRIMARY KEY     NOT NULL,
       firstname         CHAR(255),
       lastname         CHAR(255),
       date_time         CHAR(25));
    ''',

    '''CREATE TABLE room
       (ID INT PRIMARY KEY     NOT NULL,
       name           CHAR(255),
       capacity       INT     NOT NULL,
       type           CHAR(25),
       allocated       INT     NOT NULL,
       date_time         CHAR(25));
    ''',

    '''CREATE TABLE fellow_allocation
       (ID INT PRIMARY KEY     NOT NULL,
       fellow_id       INT     NOT NULL,
       room_id       INT     NOT NULL,
       date_time         CHAR(25));
    ''',

    '''CREATE TABLE staff_allocation
       (ID INT PRIMARY KEY     NOT NULL,
       staff_id       INT     NOT NULL,
       room_id       INT     NOT NULL,
       date_time         CHAR(25));
    '''
	]

	tables = ['fellow','staff','room','fellow_allocation','staff_allocation']

	def __init__(self):
		super(Migration,self).__init__()

		

	def install(self):
		for index,sql in enumerate(self.table_definitions):
			try:
				if self.execute(sql):
					print 'table created'
				else:
					print 'failed to create table'
			except:
				print 'table exists'

	
	def drop(self):
		for table in self.tables:
			try:
				if self.execute('DROP TABLE '+table+';'):
					print 'dropped table '+table
			except:
				print table+' does not exist'

m = Migration()
m.install()