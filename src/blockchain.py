import base64
import hashlib
import json
import os
from datetime import datetime
from time import time

from colorama import Back, Fore, Style, init
# from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
# from Crypto.Signature import *
# from cryptography.fernet import Fernet, MultiFernet

class Blockchain (object):
    def __init__(self):
        self.chain = [self.addGenesisBlock()]
        self.pendingTransactions = []
        self.difficulty = 2
        self.minerRewards = 12
        self.blockSize = 10
        self.nodes = set()
    
    def getPrevBlock(self):
        return self.chain[-1]
    
    def addGenesisBlock(self): #   !!!WARNING!!! - This function will break blockchain
        tArray = []
        tArray.append(Transaction("system0", "system1", 1))
        genesis = Block(tArray, str(datetime.now()) ,0)
        genesis.prev = "Null"
        return genesis
    
    def addTransaction(self, sender, receiver, amt, keyString, senderKey, showDebug):
         keyByte = keyString.encode("ASCII")
         senderKeyByte = senderKey.encode("ASCII")

         if(showDebug == True):
             print(type(keyByte), keyByte) #DEBUG ONLY
         
        #  key = RSA.import_key(keyByte)
        #  senderKey = RSA.import_key(senderKeyByte)

         if not sender or not receiver or not amt:
            print(Fore.RED + "Transaction Failed - Error code: 1")
            print(Style.RESET_ALL)
            return False
        
         transaction = Transaction(sender, receiver, amt)

        #  transaction.signTransaction(key, senderKey)

         if not transaction.isTransactionValid():
             print(Fore.RED + "Transaction failed - Error code: 2")
             return False
         self.pendingTransactions.append(transaction)
         return len(self.chain) + 1

    def isChainValid(self):
        for i in range(1, len(self.chain)):
            b1 = self.chain[i-1]
            b2 = self.chain[i]

            if not b2.hasValidTransactions():
                print(Fore.RED + "Failed - Error code: 1")
                print(Style.RESET_ALL)
                return False
            
            if b2.hash != b2.calculateHash():
                print(Fore.RED + "Failed - Error code: 2")
                print(Style.RESET_ALL)
                return False
            
            if b2.prev != b1.hash:
                print(Fore.RED + "Failed - Error code: 3")
                print(Style.RESET_ALL)
                return False
            
        return True

    def minePendingTransactions(self, miner, showDebug):
        lenPT = len(self.pendingTransactions)
        if(lenPT < 1):
            print(Fore.RED + "No transactions!")
            print(Style.RESET_ALL)
            return False
        else:
            for i in range(0, lenPT):
                end = i + self.blockSize
                if i >= lenPT:
                    end = lenPT
                
                transactionSlice = self.pendingTransactions[i:end]
                newBlock = Block(transactionSlice, str(datetime.now()), len(self.chain))
                hashVal = self.getPrevBlock().hash
                newBlock.prev = hashVal
                newBlock.mineBlock(self.difficulty, showDebug)
                self.chain.append(newBlock)
            
            # print("Mining Transactions success!")
            self.addTransaction("Miner Reward", miner, self.minerRewards, 'a', 'b', True)
     
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

    def generateKeys(self):
        key = RSA.generate(2048)
        private_key = key.export_key
        file_out = open("private.pem", "wb")
        file_out.write(private_key)

        public_key = key.publickey().export_key()
        file_out = open("public.pem", "wb")
        file_out.write(public_key)

        print(public_key.decode('ASCII'))
        return key.public_key().export_key().decode("ASCII")

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
    
    def saveJSON(self):
        Json = str(self.chainJSONEncode())
        J = base64.b64encode(Json.encode('ascii'), altchars=None)
        
        with open('blockchain', 'w') as file_out:
            file_out.write(str(J))
            file_out.close()
        
        # Encryption Section - Needs work!
        # with open('blockchain.tmp', 'r') as tmp_file:
        #     k = Fernet.generate_key()
        #     pemKPV = open('blockchainkey.fnet', 'w')
        #     pemKPV.write(str(k))
        #     pemKPV.close()
        #     #tempfile = tmp_file.read()
        #     mf = MultiFernet(k)
        #     out_file = open('blockchain', 'w')
        #     out_file.write(mf.encrypt(Json.encode()))
        #     out_file.close()
        #     os.remove("blockchain.tmp")
    
    def loadJSON(self):
        self.chain = []
        
        with open('blockchain', 'r') as f:
            b64s = f.read()
            b64 = str(b64s.encode('ascii'))
            f.close()
        
        self.chain = self.chainJSONDecode(b64)

class Block (object):
    def __init__(self, transactions, time, index):
        self.index = index
        self.transactions = transactions
        self.time = time
        self.prev = ''
        self.nonce = 0
        self.wave = self.calculateWave()
        self.hash = self.calculateHash()
    
    def calculateWave(self):
        return "8a6b9n"

    def calculateHash(self):
        hashTransactions = ""
        
        for transaction in self.transactions:
            hashTransactions +=transaction.hash
        
        hashString = str(self.time) + hashTransactions + self.wave +  self.prev + str(self.nonce)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()

    def mineBlock(self, difficulty, showDebug):
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
                print(len(hashPuzzle))              # DEBUG ONLY
                print(len(self.hash[0:difficulty])) # DEBUG ONLY
            print("Block Mined!")
            return True
    
    def hasValidTransactions(self):
        for i in range(0, len(self.transactions)):
            transaction = self.transactions[i]
            if not transaction.isTransactionValid():
                return False
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
        
        hashString = self.sender + self.receiver + str(self.amt) + str(self.time)
	    
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
		
        return hashlib.sha256(hashEncoded).hexdigest()
    
    def isTransactionValid(self):
        if (self.hash != self.calculateHash()):
            return False
        if (self.sender == self.receiver):
            return False
        # if not self.signature or len(self.signature) == 0:
            # print("Signature Error!")
            # return False
        return True

    # def signTransaction(self, key, senderKey):
	#     if(self.hash != self.calculateHash()):
	# 	    print("transaction tampered error")
	# 	    return False
	#     if(str(key.publickey().export_key()) != str(senderKey.publickey().export_key())):
	# 	    print("Transaction attempt to be signed from another wallet")
	# 		return False
	#     pkcs1_15.new(key)
	#     self.signature = "made"
	# 	#print(key.sign(self.hash, ""))
	#     print("made signature!")
    #     return True