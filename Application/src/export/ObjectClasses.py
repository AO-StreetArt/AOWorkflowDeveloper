# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 23:17:39 2016

Class files to store workflow information

@author: alex
"""

class Node(object):
    def __init__(self):
        self.connections = []
        self.data = None
        
class Tree(object):
    def __init__(self):
        self.root = Node()

class _Workflow():
    def __init__(self):
        self.name = ''
        self.id = 0
        self.keyactions = []
        self.keyactiontree = Tree()
        
    def add_keyaction(self, new_action):
        self.keyactions.append(new_action)
        
    def remove_keyaction(self, action):
        self.keyactions.remove(action)
        
    def clear_keyactions(self):
        del self.keyactions[:]
        
    def numRows(self):
        num_rows = 0
        for action in self.keyactions:
            if action.numParams() == 0:
                num_rows+=1
            else:
                num_rows+=action.numParams()
        return num_rows
        
    def build_keyactiontree(self):
        
        chains = []
        keep_going = True
        
        #Cycle through each action and take the following steps:
        #1. Compare to existing chains and, if already accounted for, do nothing
        #2. Build a full chain until an end point is reached, then push this to a list of lists (chains)
        # Splits are represented by new chains from the diverging node
        # Prepending Tail scenario common
        for action in self.keyactions:
            for chain in chains:
                for element in chain:
                    if action.id == element.id:
                        keep_going = False
            if keep_going:
                new_chain=[]
                while a.next_action_id == -1:
        
        
        #Compare the chains, the one with the first position element that is not
        #contained in any other chain is the root
        
        
        
        #Attach each chain into the tree
                
        
        
        
class _KeyAction():
    def __init__(self):
        self.name = ''
        self.description = ''
        self.systemarea = ''
        self.module = ''
        self.custom = False
        self.id = 0
        self.expected_result = ''
        self.notes = ''
        self.input_parameters = []
        self.next_action_id = -1
        
    def add_inputparameter(self, new_ip):
        self.input_parameters.append(new_ip)
        
    def remove_inputparameter(self, ip):
        self.input_parameters.remove(ip)
        
    def clear_inputparameters(self):
        del self.input_parameters[:]
        
    def numParams(self):
        return len(self.input_parameters)
        
class _InputParameter():
    def __init__(self):
        self.name = ''
        self.id = 0
        self.value = ''