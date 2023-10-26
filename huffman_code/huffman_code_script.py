from collections import Counter
from dataclasses import dataclass

@dataclass
class Tree:
	left: str
	right: str

	def children(self):
		return self.left, self.right

class HuffmanCodingTree:
	"""
	Class to build a Huffman coding tree.

	Parameters:
	chars (str): Input text. 
	
	Returns: 
	Dictionary of characters and corresponding huffman code
	"""
	def __init__(self, chars):
		self.chars = chars.lower()

	def get_huffman_code(self):
		tree = self._build_tree()
		encoding = self._assign_huffman_coding(node=tree)
		return encoding

	def _build_tree(self):
		# Get count of unique characters in chars
		char_counts = dict(Counter(self.chars))
		# Initiate priority queue Q of unique characters
		# and sort by descending order of frequencies
		Q = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)
		print(Q)
		while len(Q) > 1:
			# Get minimum value of Q to be assigned as left node
			node_l, freq_l = Q.pop()
			# Get next minimum value of Q to be assigned as right node
			node_r, freq_r = Q.pop()
			# Build tree with left and right nodes
			parent_node = Tree(left=node_l, right=node_r)
			# Sum frequencies of both returned values and assign to tree
			parent_node_freq = freq_l + freq_r
			# Add parent node to tree
			Q.append((parent_node, parent_node_freq))
			Q = sorted(Q, key=lambda x: x[1], reverse=True)

		return Q[0][0]

	def _assign_huffman_coding(self, node, encoding=''):
		# Case when node is a single node
		if type(node) == str:
			return {node: encoding}
		huffman_dict = {}
		(node_l, node_r) = node.children()
		# Recursively build left branch 
		huffman_dict.update(self._assign_huffman_coding(node=node_l, encoding=encoding + '0'))
		# Recursively build right branch 
		huffman_dict.update(self._assign_huffman_coding(node=node_r, encoding=encoding + '1'))
		return huffman_dict

if __name__ == '__main__':
	chars = 'minimum'
	huffman = HuffmanCodeTree(chars)
	encoding = huffman.get_huffman_code()
	for e in encoding:
		print(e, ' : ', encoding[e])
