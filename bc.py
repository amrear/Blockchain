import time
import hashlib

class Block:
    def __init__(self, previous_hash, data, difficulty, timestamp):
        self.previous_hash = previous_hash
        self.data = data
        print(timestamp)
        self.timestamp = timestamp
        self.nonce = 0
        self.hash = self.calc_hash(difficulty)

    
    def calc_hash(self, difficulty):
        while True:
            hash = hashlib.sha256(str([self.previous_hash, self.data, self.timestamp, self.nonce]).encode("utf-8")).hexdigest()
            if hash.startswith("0" * difficulty):
                return hash
                break
        
            self.nonce += 1

    def __repr__(self):
         return str(self.__dict__)

class Blockchain:
    def __init__(self, difficulty):
        self.chain = []
        self.difficulty = difficulty

    def add_block(self, data):
        if len(self.chain) == 0:
            block = Block("0", data, self.difficulty, time.time())
            self.chain.append(block)
        else:
            latest_hash = self.chain[-1].hash
            block = Block(latest_hash, data, self.difficulty, time.time())
            self.chain.append(block)
