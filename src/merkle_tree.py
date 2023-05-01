 # Python code for implemementing Merkle Tree
from typing import List
import hashlib
import math
class Node:
	def __init__(self, left, right, value: str, content, is_copied=False) -> None:
		#Initialize a new node of the Merkle Tree.

		self.left: Node = left
		self.right: Node = right
		self.value = value
		self.content = content
		self.is_copied = is_copied
		self.is_left = None
		self.parent: Node = None
	
	@staticmethod
	def hash(val: str) -> str:
		# val (str): The input string to hash.
		# The SHA-256 hash of the input string.

		return hashlib.sha256(val.encode('utf-8')).hexdigest()

	def __str__(self):
		return (str(self.value))  #Converts and returns string implementation of node

	def copy(self):
		#creates and returns the copy of a node. 
		return Node(self.left, self.right, self.value, self.content, True)

	

class MerkleTree:  # Defining the MerkleTree class

	def __init__(self, addresses: List[str]) -> None:
		#Initialize a new Merkle Tree.
		self.addresses = addresses #addresses of files that are to be hashed 
		self.leaves=[]   #all leaf nodes are stored here 
		self.leaves_dictionary = {}  #values are leaf nodes and keys are their corresponding hashes
		self.root = self.__buildTree(addresses)
	

	def __buildTree(self, addresses: List[str]) -> None:

		#Build the list of nodes needed to create the tree.
		# Create leaf nodes for each address given


		contents = []
		#first we read each file from given list of file addresses and store it in a list
		for filename in addresses:
			with open(filename, 'r') as f:
				file_data = f.read()
			f.close()
			contents.append(file_data)
	
		leaves: List[Node] = []
		#then we make a (MerkleTree) Node object for each element 
		for content in contents:
			node = Node(None, None, Node.hash(content), content)
			self.leaves_dictionary[node.value] = node
			leaves.append(node)

		# If the number of leaves is odd, duplicate the last leaf
		if len(leaves) % 2 == 1:
			leaves.append(leaves[-1].copy()) # duplicate last elem if odd number of elements

		self.leaves = leaves

		# Build the tree recursively
		
		return self.__buildTreeRec(leaves)
	
	#--------------obsolete (was made for testing)--------------------------
	# def __buildTreefromString(self, contents: List[str]) -> None:

	# 	#leaves: List[Node] = [Node(None, None, Node.hash(e), e) for e in values]
	# 	# contents = []
	# 	# for filename in addresses:
	# 	# 	with open(filename, 'r') as f:
	# 	# 		file_data = f.read()
	# 	# 	f.close()
	# 	# 	contents.append(file_data)
	
	# 	leaves: List[Node] = []
	# 	for content in contents:
	# 		node = Node(None, None, Node.hash(content), content)
	# 		self.leaves_dictionary[node.value] = node
	# 		leaves.append(node)

	# 	# If the number of leaves is odd, duplicate the last leaf
	# 	if len(leaves) % 2 == 1:
	# 		leaves.append(leaves[-1].copy()) # duplicate last elem if odd number of elements

	# 	self.leaves = leaves
		
	# 	return self.__buildTreeRec(leaves)
	
	def __buildTreeforVerify(self, addresses: List[str]) -> None:

		# builds a non-destructive merkle tree only used for verification purposes
		# Create leaf nodes for each value in the input list
		#leaves: List[Node] = [Node(None, None, Node.hash(e), e) for e in values]
		contents = []
		for filename in addresses:
			with open(filename, 'r') as f:
				file_data = f.read()
			f.close()
			contents.append(file_data)
	
		leaves: List[Node] = []
		for content in contents:
			node = Node(None, None, Node.hash(content), content)
			leaves.append(node)

		# If the number of leaves is odd, duplicate the last leaf
		if len(leaves) % 2 == 1:
			leaves.append(leaves[-1].copy()) # duplicate last elem if odd number of elements
			leaves[-1].is_copied = True

		#Build the tree recursively
		
		return self.__buildTreeRec(leaves)

	def __buildTreeRec(self, nodes: List[Node]) -> Node: #Contains The list of nodes to be included in the Merkle Tree.
		if len(nodes) % 2 == 1:  # If the number of nodes is odd, duplicate the last node
			nodes.append(nodes[-1].copy()) # duplicate last elem if odd number of elements
			nodes[-1].is_copied = True

		# Calculate the index of the middle node
		half: int = len(nodes) // 2  

		# If there are only two nodes, create a parent node for them
		if len(nodes) == 2:
			Hash_Value = Node.hash(nodes[0].value + nodes[1].value)
			Combined_Content = nodes[0].content+"+"+nodes[1].content
			parent = Node(nodes[0], nodes[1], Hash_Value, Combined_Content)

			nodes[0].is_left = 1
			nodes[0].parent = parent

			nodes[1].is_left = 0
			nodes[1].parent = parent

			return parent
		
		# Recursively build the left and right subtrees
		left: Node = self.__buildTreeRec(nodes[:half])
		right: Node = self.__buildTreeRec(nodes[half:])
		left.is_left = 1
		right.is_left = 0

		value: str = Node.hash(left.value + right.value)  #Calculates Hash
		content: str = f'{left.content}+{right.content}'
		
		parent = Node(left, right, value, content) 
		left.parent = parent
		right.parent = parent #Storing Content for testing purposes
		return parent #Returns The root node of the Merkle Tree.

	def verify_tree(self):
		hashed_value = self.__buildTreeforVerify(self.addresses).value
		print(hashed_value, self.root.value)
		if(hashed_value == self.root.value):
			return True
		else:
			return False

	def printTree(self) -> None:
		self.__printTreeRec(self.root) #Calling Helper function
		
	def __printTreeRec(self, node: Node) -> None:
		# Check if the node is not None
		if node != None:
			# If the node is not a leaf node, print the left and right child nodes
			if node.left != None:
				print("Left: "+str(node.left))
				print("Right: "+str(node.right))
			else:
				# If the node is a leaf node, print that it is an input
				print("Input")

			# If the node is a copy, print that it is padding
			if node.is_copied:
				print('(Padding)')
			# Print the value and content of the node
			print("Value: "+str(node.value))
			print("Content: "+str(node.content))
			print("")
			# Recursively call the method on the left and right child nodes
			self.__printTreeRec(node.left)
			self.__printTreeRec(node.right)

	def generate_path(self, node):
		path = []  #hash values of siblings of each node that is on the path from leaf to root
		bitmap = [] #whether each sibling is left orr right

		while(node.parent != None):
			if(node.is_left):
				hash_of_sibling = node.parent.right.value
			else:
				hash_of_sibling = node.parent.left.value
			path.append(hash_of_sibling)
			bitmap.append(node.is_left)
			node = node.parent
		
		return [path, bitmap]
	
	def merkle_proof(self, node:Node):
		retrieved = self.generate_path(node) #generating path from the leaf node to the root
		path = retrieved[0]
		bitmap = retrieved[1]

		hashed_value = Node.hash(node.content)
		#hashing each node hash added with its sibling hash retrieved from path. We will repeat this process by moving to parent of current node until we reach the root node.
		for i in range(len(path)):
			if(bitmap[i]): #if current element is left then hash(current node + right sibling)
				hashed_value = Node.hash(hashed_value + path[i])
			else:	 #otherwise hash(left_sibling + current node)
				hashed_value = Node.hash(path[i] + hashed_value)

		if(self.root.value != hashed_value): #checking if the root hash is the same as the hash we have calulated
			return False
		return True
		
	
	def verify_inclusion(self, address):   #this function currently takes in self.content but that's probably a bad idea when working with files
		try:							#changed it to address
			with open(address, 'r') as f:
				file_data = f.read()
			f.close()
		except:
			return False
			
		content = file_data

		hashed_value = Node.hash(content)
		
		if(hashed_value in self.leaves_dictionary.keys()): #we use dictionary here to generate path from leaf node to root, if path was given we would not use dictionary and just use the merkle proof algorithm.
			node = self.leaves_dictionary[hashed_value]
			return self.merkle_proof(node)
		return False


	def add_element(self, element : str): 
		node_list : List[Node]= []
		node, check = self.checkLeafsIsCopied()
		if check == False:
			#no copy nodes exist, a subtree of the same height as the Merkle Tree needs to be created 
			node_list.append(Node(None, None, Node.hash(element), element, False))
			for i in range(len(self.leaves)-1):
				node_list.append(Node(None, None, Node.hash(element), element, True))
			root = self.__buildTreeRec(node_list)
			self.root = self.__buildTreeRec([self.root, root])		
			self.leaves.extend(node_list)
			for i in node_list:
				self.leaves_dictionary[i.value] = i
		else:
			#copy leaf nodes exist and can be replaced
			#change the copied leafs value
			node.content = element
			original_value = node.value
			node.value = Node.hash(element)
			original_node = node
			while node.parent != None: #Loop until you reach the root 
				#here we are changing the parents value
				node = node.parent
				node.value: str = Node.hash(node.left.value + node.right.value)  #Calculates Hash
				node.content: str = f'{node.left.content}+{node.right.content}'
			#here we finally change the root values
			node.value: str = Node.hash(node.left.value + node.right.value)  #Calculates Hash
			node.content: str = f'{node.left.content}+{node.right.content}'	

			del self.leaves_dictionary[original_value] 
			self.leaves_dictionary[original_node.value] = original_node

			self.root = node


	def add_Document(self, address : str):
		self.addresses.append(address)
		with open(address, 'r') as f:
				element = f.read()
		f.close()
		self.add_element(element)

	def checkLeafsIsCopied(self):
		for thisLeaf in self.leaves:
			if thisLeaf.is_copied == True:
				return thisLeaf, True
		return thisLeaf, False

	def getRootHash(self) -> str:
	    return self.root.value  #Returns The SHA-256 hash of the root node of the Merkle Tree.

	
	
def mixmerkletree() -> None:
	#for testing perposes

	# Define a list of input values
	elems = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
	#As there are odd number of inputs, the last input is repeated
	print("Inputs: ")
	print(*elems, sep=" | ") # Print the input values separated by "|"
	print("")
	mtree = MerkleTree(elems) 
	print("Root Hash: "+mtree.getRootHash()+"\n")

	#print(mtree.root.content)
	#mtree.printTree() # Print the entire Merkle 
	#print(mtree.leaves[9].c)

	#------------testing merkle proof-----------------
	mtree.leaves[9].content = 'j'
	print(mtree.merkle_proof(mtree.leaves[9]))
	mtree.addelement('g')
	print(mtree.merkle_proof(mtree.leaves[10]))
	print("Root Hash: "+mtree.getRootHash()+"\n")
	mtree.leaves[10].content = 'a'
	print(mtree.merkle_proof(mtree.leaves[10]))
	#print(mtree.verify_inclusion('g'))
	
#mixmerkletree()

