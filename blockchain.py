import json
from time import time
from datetime import datetime
#import base64
import hashlib

class Blockchain (object):
    def __init__(self):
        self.chain = []
        self.pendingTransactions = []
    
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
            tJSON["receiver"] = transaction.receiver
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
    
    def getBalance(self, person):
        balance = 0
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            try:
                for j in range(1, len(block.transactions)):
                    transaction = block.transactions[j]
                    if(transaction.sender == person):
                        balance -= transaction.amt
                    if(transaction.receiver == person):
                        balance += transaction.amt
            except AttributeError:
                print("no transaction")
        return balance + 100

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

    def MineBlock(self, difficulty, showDebug):
        arr = []
        for i in range(0, difficulty):
            arr.append(i)
        
        arrStr = map(str, arr)
        hashPuzzle = ''.join(arrStr)
        if(showDebug == True):
            print(len(hashPuzzle))                  # DEBUG ONLY
        
        while self.hash[0:difficulty] != hashPuzzle:
            self.nonce += 1
            self.hash = self.calculateHash()
            if(showDebug == True):
                print(len(self.hashPuzzle))         # DEBUG ONLY
                print(len(self.hash[0:difficulty])) # DEBUG ONLY
            print("Block Mined!")
            return True

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
    
    def isTransactionValid(self):
        if(self.hash != self.calculateHash()):
            return False
        if(self.sender == self.receiver):
            return False
        if not self.signature or len(self.signature) == 0:
            print("Signature Error!")
            return False
        return True