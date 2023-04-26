import hashlib
from merkle_tree import *
import os

class Block:
    def __init__(self, data, merkle_tree: Node, previous_block=None):
        self.data = data
        self.previous_block = previous_block
        self.mtree = merkle_tree
        self.previous_hash = None
        self.hash = self.calculate_hash()

    """ def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.data).encode('utf-8'))
        if self.previous_block:
            sha.update(str(self.previous_block.hash).encode('utf-8'))
        return sha.hexdigest() """

    def update_hash(self):
        self.hash = self.calculate_hash()
        if self.previous_block:
            self.previous_block.update_hash()

class Blockchain:
    def __init__(self):
        self.head = None
        self.file_hash = None

    def add_file(self, folder_path: str, filename: str):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as f:
            file_data = f.read()
            if not self.head:
                self.head = Block(file_data)
                self.file_hash = hashlib.sha256(file_data).hexdigest()
            else:
                merkle_tree = MerkleTree([self.head.data, file_data])
                new_block = Block(file_data, self.head, merkle_tree)
                new_block.previous_hash = self.head.hash
                self.head = new_block
                self.file_hash = hashlib.sha256(file_data + self.file_hash.encode('utf-8')).hexdigest()

...

blockchain = Blockchain()

folder_path = "dataset/sample test case"
filename = "s1.txt"

blockchain.add_file(folder_path, filename)

print(blockchain.verify())

with open(os.path.join(folder_path, filename), "a") as f:
    f.write("This is some new content.")

print(blockchain.verify())

blockchain.update_block(b'This is the original file contents.', b'This is the new file contents.')

print(blockchain.verify())