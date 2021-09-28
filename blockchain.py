import json
from time import time
from datetime import datetime
#import base64
import hashlib

class Blockchain (object):
    def __init__(self):
        self.chain = []
    
    def getPrevBlock(self):
        return self.chain[-1]
    
    def addBlock(self, block):
        if(len(self.chain) > 0):
            block.prev = self.getPrevBlock().hash
        else:
            block.prev = "Null"
        self.chain.append(block)

class Block (object):
    def __init__(self, transactions, time, index):
        self.index = index
        self.transactions = transactions
        self.time = time
        self.prev = ''
        self.hash = self.calculateHash()

    def calculateHash(self):
        hashTransactions = ""
        for transaction in self.transactions:
            hashTransactions +=transaction.hash
        
        hashString = str(self.time) + hashTransactions + self.prev + str(self.index)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()
        
class Transaction (object):
    def __init__(self, sender, reciver, amt):
        self.sender = sender
        self.reciver = reciver
        self.amt = amt
        self.time = time()
        self.hash = self.calculateHash()
        
def calculateHash(self):
        hashTransactions = ""
        for transaction in self.transactions:
            hashTransactions +=transaction.hash
        
        hashString = self.sender + self.reciver + str(self.amt) + str(self.time)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()
