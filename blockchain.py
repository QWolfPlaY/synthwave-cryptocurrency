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
    
    def chainJSONEncode(self):
        blockArrayJSON = []

        for block in self.chain:
            blockJSON = {}
            blockJSON["hash"] = block.hash
            blockJSON["prev"] = block.prev
            blockJSON["index"] = block.index
            blockJSON["time"] = block.time
            blockJSON["nonce"] = block.nonce
            blockJSON["wave"] = block.wave
        
        transactionsJSON = []
        tJSON = {}
        for transaction in block.transactions:
            tJSON["time"] = transaction.time
            tJSON["sender"] = transaction.sender
            tJSON["reciever"] = transaction.reciever
            tJSON["amt"] = transaction.amt
            tJSON["hash"] = transaction.hash
        
        blockJSON['transactions'] = transactionsJSON
        
        blockArrayJSON.append(blockJSON)

        return blockArrayJSON

    def chainJSONDecode(self,chainJSON):
        chain = []
        for blockJSON in chainJSON:

            tArray = []
            for tJSON in blockJSON['transactions']:
                transaction = Transaction(tJSON['sender'], tJSON['receiver'], tJSON['amt'])
                transaction.time = tJSON['time']
                transaction.hash = tJSON['hash']
                tArray.append(transaction)
            
            block = Block((tArray), blockJSON['time'], blockJSON['index'])
            block.hash = blockJSON['hash']
            block.prev = blockJSON['prev']
            block.nonce = blockJSON['nonce']
            block.wave = blockJSON['wave']
            
            chain.append(block)
        return chain

class Block (object):
    def __init__(self, transactions, time, index):
        self.index = index
        self.transactions = transactions
        self.time = time
        self.prev = ''
        self.nonce = 0
        self.wave = self.calculateWave()
        self.hash = self.calculateHash()
    
    def calculateWAve(self):
        return "8a6b9n"

    def calculateHash(self):
        hashTransactions = ""
        
        for transaction in self.transactions:
            hashTransactions +=transaction.hash
        
        hashString = str(self.time) + hashTransactions + self.wave +  self.prev + str(self.nonce)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()
        
class Transaction (object):
    def __init__(self, sender, receiver, amt):
        self.sender = sender
        self.receiver = receiver
        self.amt = amt
        self.time = str(datetime.now())
        self.hash = self.calculateHash()
        
def calculateHash(self):
        hashTransactions = ""
        for transaction in self.transactions:
            hashTransactions +=transaction.hash
        
        hashString = self.sender + self.receiver + str(self.amt) + str(self.time)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()