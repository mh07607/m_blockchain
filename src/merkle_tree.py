 # Python code for implemementing Merkle Tree
from typing import List
import hashlib
class Node:
	def __init__(self, left, right, value: str, content, is_copied=False) -> None:
		#Initialize a new node of the Merkle Tree.
 	
		#- left (Node): The left child node.
		#- right (Node): The right child node.
		#- value (str): The hash value of the node.
		#- content (str): The content of the node.
		#- is_copied (bool): A flag indicating whether the node is a copy (True) or not (False).

		self.left: Node = left
		self.right: Node = right
		self.value = value
		self.content = content
		self.is_copied = is_copied
		self.is_left = None
		self.parent: Node = None
		self.leaves = []

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
	
	def neighbour(self): 
		if(self.is_left== 1):
			return self.parent.right
		else:
			return self.parent.left

	def set_parent(self, parent):
		self.parent = parent
	

class MerkleTree:  # Defining the MerkleTree class

	def __init__(self, values: List[str]) -> None:
		#Initialize a new Merkle Tree.
		
		self.__buildTree(values)

	def __buildTree(self, values: List[str]) -> None:

		#Build the Merkle Tree recursively.
		# Create leaf nodes for each value in the input list
		leaves: List[Node] = [Node(None, None, Node.hash(e), e) for e in values]
		self.leaves = leaves
		# If the number of leaves is odd, duplicate the last leaf
		if len(leaves) % 2 == 1:
			leaves.append(leaves[-1].copy()) # duplicate last elem if odd number of elements
		# Build the tree recursively
		self.root: Node = self.__buildTreeRec(leaves)

	def __buildTreeRec(self, nodes: List[Node]) -> Node: #Contains The list of nodes to be included in the Merkle Tree.
		if len(nodes) % 2 == 1:  # If the number of nodes is odd, duplicate the last node
			nodes.append(nodes[-1].copy()) # duplicate last elem if odd number of elements

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

	def merkle_proof(self, node:Node):
		path = []
		hashed_value = Node.hash(node.content)

		while(node.parent != None):
			path.append(node.content)
			hashed_value = Node.hash(hashed_value + node.neighbour().value)
			# if(hashed_value != node.parent.value):
			# 	return False
			node.parent.value
			node = node.parent

		#hashed_value = Node.hash(str(node.value) + str(node.neighbour().value))
		path.append(node.content)
		#path.append(self.root.content)

		if(self.root.value != hashed_value):
			print(node.content)
			return False
		return path


	def getRootHash(self) -> str:
	    return self.root.value  #Returns The SHA-256 hash of the root node of the Merkle Tree.
	
	
def mixmerkletree() -> None:
	""" The mixmerkletree() function takes a list of transactions and generates a Merkle tree by 
	recursively combining pairs of hashes until only one root hash remains. It then adds a 
	"mixing" hash to the root hash to make it unique and returns the final root hash. This 
	process helps to ensure the privacy of the transactions by making it difficult to trace the 
	original transaction from the final output. """

	# Define a list of input values
	elems = ["a", "b", "c", "d"]
	#As there are odd number of inputs, the last input is repeated
	print("Inputs: ")
	print(*elems, sep=" | ") # Print the input values separated by "|"
	print("")
	mtree = MerkleTree(elems) # Create a Merkle Tree from the input values
	print("Root Hash: "+mtree.getRootHash()+"\n") # Print the root hash of the Merkle Tree
	mtree.printTree() # Print the entire Merkle Tree
	mtree.leaves[0].content = 'a'
	print(mtree.merkle_proof(mtree.leaves[0]))

mixmerkletree()

#This code was contributed by Pranay Arora (TSEC-2023).