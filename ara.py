"""Amity Room Allocation

Usage:
  ara create_room (<room_name> <room_type>)...
  ara add_person <firstname> <lastname> <person_type> [-w]

Options:
  -h --help     Show this screen.
  -w            want accomodation

"""
from docopt import docopt

def addperson(args):
    print 'add person'
    print args

def createroom(args):
  room_names = args['<room_name>']
  room_types = args['<room_type>']
  print room_names,room_types

#function mapping to avoid long if else chain
func_map = {
  'create_room':createroom,
  'add_person':addperson,
}

if __name__ == '__main__':
    arguments = docopt(__doc__)
    
    for command in func_map:
      if arguments[command]:
        func_map[command](arguments)
        break
