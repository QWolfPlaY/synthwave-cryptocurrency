from blockchain import *
import pprint
from time import time

pp = pprint.PrettyPrinter(indent=4)

bc = Blockchain()
tr = []

block = Block(tr, time(), 0)
bc.addBlock(block)

block = Block(tr, time(), 1)
bc.addBlock(block)

block = Block(tr, time(), 2)
bc.addBlock(block)

pp.pprint(bc.chainJSONEncode())
print("Length: ", len(bc.chain))