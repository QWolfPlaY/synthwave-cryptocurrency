from blockchain import *
import pprint
from time import time
import sqlite3 as sqlite
import threading
import multiprocessing

threadPoolSize = 4

pp = pprint.PrettyPrinter(indent=4)

bc = Blockchain()
tr = []

bc.loadJSON()

# for i in range(99999):
    # bc.addTransaction('a', 'b', 2137, 'a', 'b', False)
    
# bc.minePendingTransactions('a', False)

# t1 = threading.Thread(target=mine)
# t2 = threading.Thread(target=mine)

# t1.start()
# t2.start()
# t1.join()
# t2.join()


pp.pprint(len(bc.chain))
# pp.pprint(bc.chain)
bc.saveJSON()