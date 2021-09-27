import json
from time import time
from datetime import datetime

class Blockchain (object):
    def __init__(self):
        self.chain = [];

class Block (object):
    def __init__(self, transactions, time, index):
        self.index = index;
        self.transactions = transactions;
        self.time = time;

        
class Transaction (object):
    def __init__(self, sender, reciver, amt):
