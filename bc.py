import time
import hashlib

class Block:
    def __init__(self, previous_hash, data, difficulty, timestamp):
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp
        self.nonce = 0
        self.hash = self.calc_hash(difficulty)

    def calc_hash(self, difficulty=0):
        """
        Calculates the hash of block.
        An optional `difficulty` argument can also be passed which determines how many zeros
        should be in the beggining of the hash.
        """

        while True:
            # Keeps hashing until it reaches a none which can be added to the block
            # in order to get the desired output
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
        """
        Adds a block to the blockchain.
        A special case is also considered for the genesis block.
        """

        if len(self.chain) == 0:
            # If there is no block in the blockchain,
            # The first block should be constructed a bit differently.
            # We sould pass the previous hash a random value since there is no previus hash.
            # In this case I passed 0 and created `genesis block`.
            block = Block("0", data, self.difficulty, time.time())
            self.chain.append(block)
        else:
            # After creating genesis block, we begit to create regular blocks
            # and pass the hash of previous block to the `previous_hash` attribute.
            latest_hash = self.chain[-1].hash
            block = Block(latest_hash, data, self.difficulty, time.time())
            self.chain.append(block)

    def verify(self):
        """
        Checks to see if the blockchain has been tampered with
        Returns True if the blockchain is valid
        """

        for block in self.chain:
            # First it hashes all of the blocks and compares them with hash that is provided in the block.
            if block.hash != block.calc_hash(self.difficulty):
                return False

        for index, block in enumerate(self.chain):
            # Then it compares each block's hash with the previous_hash attribute of the last block,
            # and they should match.

            # For genesis block
            if index == 0:
                continue
            
            if block.previous_hash != self.chain[index-1].hash:
                return False

        return True
