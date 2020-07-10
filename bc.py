import time
import hashlib

class Block:
    def __init__(self, previous_hash, data, difficulty, timestamp):
        self.previous_hash = previous_hash
        self.data = data
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

    def verify(self):
        """
        Checks to see if the blockchain has been tampered with
        Returns True if the blockchain is valid
        """

        # First it hashes all of the blocks and compares them with hash that is provided in the block
        for block in self.chain:
            if block.hash != block.calc_hash(self.difficulty):
                return False

        # Then it compares each block's hash with the previous_hash attribute of the last block
        # and they should match
        for index, block in enumerate(self.chain):
            # For genesis block
            if index == 0:
                continue
            
            if block.previous_hash != self.chain[index-1].hash:
                return False

        return True
