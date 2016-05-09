Room Allocation
===============

One stop solution for room allocation management

### Badges
[![Build Status](https://travis-ci.org/andela-snwuguru/room-allocation.svg?branch=master)](https://travis-ci.org/andela-snwuguru/room-allocation)

!https://coveralls.io/repos/github/andela-snwuguru/room-allocation/badge.svg?branch=master(Coverage Status)!:https://coveralls.io/github/andela-snwuguru/room-allocation?branch=master

### Features

- Create rooms
- Add Person
- Auto allocate person to a room when added
- Reallocate person
- Manual allocation of person
- Display allocations
- Load people from text file (see sample text file format below)
- Display unallocated people and room
- Display rooms base on allocated or unallocated
- Display room details with list of members
- Save state to sqlite database
- Load state from sqlite database

### Dependecies

- Docopt `` pip install docopt ``
- Python 2.7.X and above

### Modules used

- Datetime
- Sqlite3
- Pickle
- Random
- Os

### How to use

- Clone project `` git clone git@github.com:andela-snwuguru/room-allocation.git ``
- Install dependecies
- Navigate to project folder `` cd ~/room-allocation ``
- See list of available command `` python ara.py -h ``

### Sample Operations

- Create multiple rooms `` python ara.py create_room "room 1" "office" "room 2" "living" ``
- Add Person `` python ara.py add_person "Sunday" "Nwuguru" "fellow" -w ``
- Reallocate person `` python ara.py reallocate_person "SN3" "room 2" ``
- Allocate person `` python ara.py reallocate_person "SN3" "room 2" -w ``
- Load people from text file `` python ara.py load_people "people.txt" ``
- Display allocations `` python ara.py print_allocations ``
- Export allocations to file `` python ara.py print_allocations "allocation.txt" `` exported file will be located in data folder
- Display unallocated `` python ara.py print_unallocated ``
- Export unallocated to file `` python ara.py print_unallocated "unallocated.txt" `` exported file will be located in data folder
- Display room details `` python ara.py print_room "room 1" ``
- Display people `` python ara.py list_people ``
- Display unallocated people `` python ara.py list_people -u``
- Display rooms `` python ara.py list_rooms ``
- Display allocated rooms `` python ara.py list_rooms -a``
- Save current state to sqlite database `` python ara.py save_state "my_db" ``
- Load current state from sqlite database `` python ara.py load_state "my_db" ``

### How to Contribute

- Fork Repo
- Create new branch and add your contribution
- Push to your branch
- Raise a pull request
