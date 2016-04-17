from db import Db

class Migration(Db):
	"""docstring for Migration"""
	table_definitions = [
	'''CREATE TABLE fellow
       (id INTEGER PRIMARY KEY AUTOINCREMENT,
       firstname         CHAR(255),
       lastname         CHAR(255),
       allocation       INT    NOT NULL,
       date_time         CHAR(25));
    ''',

    '''CREATE TABLE staff
       (id INTEGER PRIMARY KEY AUTOINCREMENT,
       firstname         CHAR(255),
       lastname         CHAR(255),
       date_time         CHAR(25));
    ''',

    '''CREATE TABLE room
       (id INTEGER PRIMARY KEY AUTOINCREMENT,
       name           CHAR(255),
       capacity       INT     NOT NULL,
       type           CHAR(25),
       allocated       INT     NOT NULL,
       date_time         CHAR(25));
    ''',

    '''CREATE TABLE fellow_allocation
       (id INTEGER PRIMARY KEY AUTOINCREMENT,
       fellow_id       INT     NOT NULL,
       room_id       INT     NOT NULL,
       date_time         CHAR(25));
    ''',

    '''CREATE TABLE staff_allocation
       (id INTEGER PRIMARY KEY AUTOINCREMENT,
       staff_id       INT     NOT NULL,
       room_id       INT     NOT NULL,
       date_time         CHAR(25));
    '''
	]

	tables = ['fellow','staff','room','fellow_allocation','staff_allocation']

	def __init__(self,dbname = 'amity'):
		super(Migration,self).__init__(dbname)

		

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

m = Migration('amity_test')
m.install()