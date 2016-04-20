"""Amity Room Allocation

Usage:
  ara create_room (<room_name> <room_type>)...
  ara add_person (<firstname> <lastname> <person_type>) [-w]
  ara reallocate_person <person_id> <new_room_name>
  ara load_people <file_location>
  ara print_allocations [(-o <file_name>)]
  ara print_unallocated [(-o <file_name>)]
  ara print_room <name_of_room>


Options:
  -h --help     Show this screen.
  -w            want accomodation

"""
from docopt import docopt
from src.amity import Amity


#function mapping to avoid long if else chain
func_map = [
  'create_room',
  'add_person',
  'reallocate_person',
  'load_people',
  'print_allocations',
  'print_unallocated',
  'print_room',
]

if __name__ == '__main__':
    arguments = docopt(__doc__)
    
    for command in func_map:
      if arguments[command]:
        amity = Amity(command)
        amity.run_command(arguments)
        break
