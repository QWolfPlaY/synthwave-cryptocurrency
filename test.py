from blockchain import *
import pprint
from time import time

pp = pprint.PrettyPrinter(indent=4)

bc = Blockchain()
tr = []

bc.addGenesisBlock()
bc.addGenesisBlock()
bc.addGenesisBlock()

bc.saveJSON()

bc.loadJSON()