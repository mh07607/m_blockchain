import hashlib

class Block:
    def __init__(self, data, previous_block=None):
        self.data = data
        self.previous_block = previous_block
        self.previous_hash = None
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.data).encode('utf-8'))
        if self.previous_block:
            sha.update(str(self.previous_block.hash).encode('utf-8'))
        return sha.hexdigest()

    def update_hash(self):
        self.hash = self.calculate_hash()
        if self.previous_block:
            self.previous_block.update_hash()

class Blockchain:
    def __init__(self):
        self.head = None

    def add(self, data):
        if not self.head:
            self.head = Block(data)
        else:
            new_block = Block(data, self.head)
            new_block.previous_hash = self.head.hash
            self.head = new_block

    def verify(self):
        if not self.head:
            return True

        current_block = self.head
        while current_block.previous_block:
            if current_block.previous_hash != current_block.previous_block.hash:
                return False
            current_block = current_block.previous_block
        return True

    def update_block(self, block_data, new_data):
        current_block = self.head
        while current_block:
            if current_block.data == block_data:
                current_block.data = new_data
                current_block.update_hash()
                break
            current_block = current_block.previous_block


blockchain = Blockchain()


blockchain.add("Hello")
blockchain.add("Arsalan")
blockchain.add("!")


print(blockchain.verify())  


blockchain.update_block("Arsalan", "Muzammil")


print(blockchain.verify()) 
