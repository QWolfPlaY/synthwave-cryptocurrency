from blockchain import *
import pprint
from time import time
import sqlite3 as sqlite



pp = pprint.PrettyPrinter(indent=4)

bc = Blockchain()
tr = []

for i in range(8):
    bc.addTransaction('a', 'b', 2137, 'a', 'b', True)

bc.minePendingTransactions('a')

print(len(bc.chain))
pp.pprint(bc.chain)