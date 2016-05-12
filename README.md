Room Allocation
===============
[![Build Status](https://travis-ci.org/andela-snwuguru/room-allocation.svg?branch=master)](https://travis-ci.org/andela-snwuguru/room-allocation) [![Coverage Status](https://coveralls.io/repos/github/andela-snwuguru/room-allocation/badge.svg?branch=master)](https://coveralls.io/github/andela-snwuguru/room-allocation?branch=master)

Room Allocation is a checkpoint 1 project used to evaluate Fellow proviciency in Python programming. This is not a real solution for room allocation but it is a good start for python beginners.

### Features

- Create rooms
- Add Person
- Auto allocate person to a room when added
- Reallocate person
- remove person
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
- Tabulate `` pip install tabulate ``
- Coverage `` pip install coverage ``
- Python 2.7.X and above

### How to use

- Clone project `` git clone git@github.com:andela-snwuguru/room-allocation.git ``
- Create a virtual environment `` mkvirtualenv ara ``
- Install dependecies `` pip install -r requirements.txt ``
- Navigate to project folder `` cd ~/room-allocation ``
- See list of available command `` python ara.py -h ``

### Sample Operations

- Create multiple rooms `` python ara.py create_room "room 1" "office" "room 2" "living" ``
- Add Person `` python ara.py add_person "Sunday" "Nwuguru" "fellow" -w ``
- Reallocate person `` python ara.py reallocate_person "SN3" "room 2" ``
- remove person `` python ara.py remove_person "SN3" "room 2" ``
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
- Clear Records `` python ara.py clear ``

### How to Contribute

- Fork Repo
- Create new branch and add your contribution
- Push to your branch
- Raise a pull request
