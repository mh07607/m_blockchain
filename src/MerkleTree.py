import hashlib

class MerkleTree():

    def __init__(self, data):
        self.data = data
        self.tree = self.__createTree()
        self.leafs = []
        self.root = None

    def __createTree(self):
        tree = [] 
        for thisData in self.data:
            tree.append(hashlib.sha256(thisData.encode('utf-8')).hexdigest()) #first layer of encryption
        print("The Zeroth Layer: ", tree)

        while len(tree) > 1:
            if len(tree) % 2 != 0:
                tree.append(tree[-1]) #if there is an odd number of data values we duplicate the last data value

        level= []
        for i in range (0, len(tree), 2): #Combining two hashed nodes to create the next level
            level.append(hashlib.sha256((tree[i] + tree[i+1]).encode('utf-8')).hexdigest())
            print("Level ", i, " :", level)
        tree = level

        return tree

tree = MerkleTree(['a', 'b', 'c', 'd'])