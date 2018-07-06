import  json
from Constants_and_classes import *
x = Player('bayron', 3, 'Druid', 'forest elf', 10,10,10,10,10,10,300)
json.dump(x,'Heroes\\bayron.json')