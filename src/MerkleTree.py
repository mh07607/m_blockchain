import hashlib

class MerkleTree():

    def __init__(self, data):
        self.data = data
        self.tree = self.__createTree()
        self.leafs = []
        self.root = None

    def __createTree(self):
        hashedLeafs = [] 
        for thisData in self.data:
            hashedLeafs.append(hashlib.sha256(thisData.encode('utf-8')).hexdigest()) #first layer of encryption
        print(hashedLeafs)

tree = MerkleTree(['a', 'b', 'c', 'd'])