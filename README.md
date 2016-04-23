Room Allocation
===============

One stop solution for room allocation management
--------------------------------------------------

### Features

- Create rooms
- Add Person
- Auto allocate person to a room when added
- reallocate person
- manual allocation of person
- display allocations
- load people from text file (see sample text file format below)
- display unallocated people and room
- display rooms base on allocated or unallocated
- display room details with list of members
- save state to sqlite database
- load state from sqlite database

### Dependecies

- docopt
	`` pip install docopt ``
- python 2.7.X and above

### Modules used

- datetime
- sqlite3
- pickle
- random
- os

### How to use

- clone project
	`` git clone git@github.com:andela-snwuguru/room-allocation.git ``
- install dependecies
- navigate to project folder
	`` cd ~/room-allocation ``
- see list of available command
	`` python ara.py -h ``

### Sample Operations

- create multiple rooms
	`` python ara.py create_room "room 1" "office" "room 2" "living" ``
