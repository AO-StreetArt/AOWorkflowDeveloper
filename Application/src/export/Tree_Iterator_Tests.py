# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 20:49:30 2016

Iterator Tests

@author: alex
"""

from Tree_Iterators import Basic_Recursive_Iterator, Advanced_Recursive_Iterator
from ObjectClasses import Node, Tree

#Define the Recursion Functions
def write_test():
    print('test')
    
def write_node(node, param):
    print('%s%s' % (node.data, param))

#Build a few trees to test with
node_list=[]
i=0

for i in range(0, 30):
    n = Node()
    n.data = i
    node_list.append(n)
    
#Single Stack Test
tree1 = Tree()
tree1.root = node_list[0]

node_list[0].connections.append(node_list[1])
node_list[1].connections.append(node_list[2])
node_list[2].connections.append(node_list[3])
node_list[3].connections.append(node_list[4])
node_list[4].connections.append(node_list[5])
    
#Bidirectional search tree
tree2 = Tree()
tree2.root = node_list[6]

node_list[6].connections.append(node_list[7])
node_list[6].connections.append(node_list[8])
node_list[7].connections.append(node_list[9])
node_list[7].connections.append(node_list[10])
node_list[8].connections.append(node_list[11])
node_list[8].connections.append(node_list[12])
node_list[9].connections.append(node_list[13])
node_list[10].connections.append(node_list[14])
node_list[11].connections.append(node_list[15])
node_list[12].connections.append(node_list[16])

#Closed loop tree
tree3 = Tree()
tree3.root = node_list[17]

node_list[17].connections.append(node_list[18])
node_list[18].connections.append(node_list[19])
node_list[19].connections.append(node_list[20])
node_list[19].connections.append(node_list[21])
node_list[20].connections.append(node_list[22])
node_list[21].connections.append(node_list[23])
node_list[22].connections.append(node_list[24])
node_list[23].connections.append(node_list[25])
node_list[24].connections.append(node_list[26])
node_list[25].connections.append(node_list[26])
node_list[26].connections.append(node_list[27])
node_list[27].connections.append(node_list[28])

#Iterator Tests

#Basic Iterator Test
basic_iterator1 = Basic_Recursive_Iterator(tree1)
basic_iterator2 = Basic_Recursive_Iterator(tree2)
basic_iterator3 = Basic_Recursive_Iterator(tree3)

basic_iterator1.iterate(write_test)
basic_iterator1.iterate(write_test)
basic_iterator1.iterate(write_test)

#Advanced Iterator Test
adv_iterator1 = Advanced_Recursive_Iterator(tree1)
adv_iterator2 = Advanced_Recursive_Iterator(tree2)
adv_iterator3 = Advanced_Recursive_Iterator(tree3)

adv_iterator1.iterate(write_node, param=0)
adv_iterator2.iterate(write_node, param=1)
adv_iterator3.iterate(write_node, param=2)

#Tail Recursion Iterator Test
t_iterator1 = Advanced_Recursive_Iterator(tree1)
t_iterator2 = Advanced_Recursive_Iterator(tree2)
t_iterator3 = Advanced_Recursive_Iterator(tree3)

t_iterator1.iterate(write_node, param=0)
t_iterator2.iterate(write_node, param=1)
t_iterator3.iterate(write_node, param=2)