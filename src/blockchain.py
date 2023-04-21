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
        self.file_hash = None

    def add_file(self, filename):
        with open(filename, 'rb') as f:
            file_data = f.read()
            if not self.head:
                self.head = Block(file_data)
                self.file_hash = hashlib.sha256(file_data).hexdigest()
            else:
                new_block = Block(file_data, self.head)
                new_block.previous_hash = self.head.hash
                self.head = new_block
                self.file_hash = hashlib.sha256(file_data + self.file_hash.encode('utf-8')).hexdigest()

    def verify(self):
        if not self.head:
            return True

        current_block = self.head
        while current_block.previous_block:
            if current_block.previous_hash != current_block.previous_block.hash:
                return False
            current_block = current_block.previous_block

        if self.file_hash != current_block.hash:
            return False

        return True

    def update_block(self, block_data, new_data):
        current_block = self.head
        while current_block:
            if current_block.data == block_data:
                current_block.data = new_data
                current_block.update_hash()
                self.file_hash = hashlib.sha256(new_data + self.file_hash.encode('utf-8')).hexdigest()
                break
            current_block = current_block.previous_block


blockchain = Blockchain()

blockchain.add_file("s1.txt")

print(blockchain.verify())

with open("s1.txt", "a") as f:
    f.write("This is some new content.")

print(blockchain.verify())

blockchain.update_block(b'This is the original file contents.', b'This is the new file contents.')

print(blockchain.verify())
