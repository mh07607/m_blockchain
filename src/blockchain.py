import hashlib
from merkle_tree import MerkleTree, Node

class Block:
    def __init__(self, merkle_tree: MerkleTree, previous_block=None):
        #self.data = data
        self.previous_block = previous_block
        self.mtree: MerkleTree = merkle_tree
        #self.previous_hash = None
        self.hash = self.mtree.root.value#self.calculate_hash()

    def verify(self):
        return self.mtree.verify()
    """ def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.data).encode('utf-8'))
        if self.previous_block:
            sha.update(str(self.previous_block.hash).encode('utf-8'))
        return sha.hexdigest() """

    #def calculate_hash(self):
        # sha = hashlib.sha256()
        # sha.update(str(self.data).encode('utf-8'))
        # if self.previous_block:
        #     sha.update(str(self.previous_block.hash).encode('utf-8'))
        # return sha.hexdigest()

    # def update_hash(self):
    #     self.hash = self.calculate_hash()
    #     if self.previous_block:
    #         self.previous_block.update_hash()

class Blockchain:
    def __init__(self):
        self.head = None
        #self.file_hash = None

    def add_files(self, filenames):      

        if not self.head:
            mtree = MerkleTree(filenames)
            self.head = Block(mtree)
            #self.file_hash = hashlib.sha256(file_data).hexdigest()
        else:
            mtree = MerkleTree(filenames)
            new_block = Block(self.head)
            #new_block.previous_hash = self.head.hash
            new_block.previous_block = self.head
            self.head = new_block
                    #self.file_hash = hashlib.sha256(file_data + self.file_hash.encode('utf-8')).hexdigest()

    def verify(self):
        if not self.head:
            return True

        current_block = self.head
        i = 0
        while current_block:
            if(current_block.verify()):
                current_block = current_block.previous_block
            else:
                return i
            i = i + 1
        return True

    def verify_document(self, address, block_number):
        i = 0
        current_block = self.head
        while i < block_number:
            current_block = current_block.previous_block
            i = i+1

        return current_block.mtree.verify_inclusion(address)

    def update_block(self, block_data, new_data):
        current_block = self.head
        while current_block:
            if current_block.data == block_data:
                current_block.data = new_data
                current_block.update_hash()
                self.file_hash = hashlib.sha256(new_data + self.file_hash.encode('utf-8')).hexdigest()
                break
            current_block = current_block.previous_block


# blockchain = Blockchain()

# blockchain.add_file("s1.txt")

# print(blockchain.verify())

# with open("s1.txt", "a") as f:
#     f.write("This is some new content.")

# print(blockchain.verify())

# blockchain.update_block(b'This is the original file contents.', b'This is the new file contents.')

# print(blockchain.verify())
bc = Blockchain()
bc.add_files(["dataset\sample test case\s1.txt", "dataset\sample test case\s2.txt", "dataset\sample test case\s3.txt"])
print(bc.verify())
with open("dataset\sample test case\s1.txt", "a") as f:
    f.write("yeet")
print(bc.verify())
print("doc3", bc.verify_document("dataset\sample test case\s3.txt", 0))
print("doc2", bc.verify_document("dataset\sample test case\s2.txt", 0))
print("doc1", bc.verify_document("dataset\sample test case\s1.txt", 0))

