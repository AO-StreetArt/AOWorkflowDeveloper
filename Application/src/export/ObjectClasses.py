# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 23:17:39 2016

Class files to store workflow information

@author: alex
"""

#Node object for use in a tree
class Node(object):
    def __init__(self):
        self.connections = []
        self.data = None
        
#Tree datastructure to allow for storage of non-linear flows
class Tree(object):
    def __init__(self):
        self.root = Node()
        
#Key Action object for in-memory storage of key actions
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
        self.next_action_list = []
        
    def add_nextaction(self, next_act):
        self.next_action_list.append(next_act)
        self.next_action_id = next_act.id
        
    def has_nextaction(self):
        if self.next_action_id == -1:
            return False
        else:
            return True
        
    def add_inputparameter(self, new_ip):
        self.input_parameters.append(new_ip)
        
    def remove_inputparameter(self, ip):
        self.input_parameters.remove(ip)
        
    def clear_inputparameters(self):
        del self.input_parameters[:]
        
    def numParams(self):
        return len(self.input_parameters)
        
#Input Parameter Object for in-memory storage of input params
class _InputParameter():
    def __init__(self):
        self.name = ''
        self.id = 0
        self.value = ''

#Workflow object for in-memory storage of workflow objects, as well as analysis/data manipulation
class _Workflow():
    def __init__(self):
        self.name = ''
        self.id = 0
        self.keyactions = []
        self.keyactiontreelist = []
        
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
        
    #Key Action Tree Methods
        
    def is_element_in_tree(self, input_id, tree):
        return self.is_element_in_nodechain(input_id, tree.root)
    
    def is_element_in_nodechain(self, input_id, node):
        if node.data.id == input_id:
            return True
            print('Match on element %s found' % (input_id))
        else:
            if len(node.connections) > 0:
                match=False
                for con in node.connections:
                    if self.is_element_in_nodechain(input_id, con):
                        match = True
                print('Match on element %s found' % (input_id))
                return match
            else:
                return False
                
    def is_element_connected_to_tree(self, input_id, tree):
        return self.is_element_connected_to_nodechain(input_id, tree.root)
    
    def is_element_connected_to_nodechain(self, input_id, node):
        for act in node.data.next_action_list:
            if act.id == input_id:
                print('Connection on element %s found' % (input_id))
                return True

#        if len(node.connections) > 0:
        for con in node.connections:
            a = self.is_element_connected_to_nodechain(input_id, con)
            print('Is Element Connected To Node Chain Returned with Value %s' % (a))
            return a
#        else:
#        return False
        
    def print_trees(self):
        for tree in self.keyactiontreelist:
            self.print_node(tree.root)
        
    def print_node(self, node):
        print(node.data.id)
        for cons in node.connections:
            self.print_node(cons)
            
    #Methods for building the Key Action Tree
        
    def find_keyaction(self, keyactionid):
        for action in self.keyactions:
            if action.id == keyactionid:
                return action
        return 0
        
    def build_keyactionchain(self, act, chain_list):
        print('Build Key Action Chain called with action %s and chain list %s' % (act.id, chain_list))
        new_chain = []
        test_action = act
        multi_hit=False
        #Loop until an ending action is found
        while test_action.has_nextaction():
            print('Loop entered, next action list length %s' % (len(test_action.next_action_list)))
            new_chain.append(test_action)
            #If this is a standard node, we can just read the next action id
            if len(test_action.next_action_list) == 1:
                test_action = self.find_keyaction(test_action.next_action_id)
                print('Node %s appended and new test action assigned' % (test_action.id))
                
            #If this is an and or or node, we need to account for splits
            else:
                acts = test_action.next_action_list
                
                for action in acts:
                    multi_hit=True
                    test_action = self.build_keyactionchain(action, chain_list)
        if multi_hit == False:
            new_chain.append(test_action)
        chain_list.append(new_chain)
        print('Adding chain to chain list with starting ID %s and length %s' % (new_chain[0].id, len(new_chain)))
        for element in new_chain:
            print(element.id)
        return test_action
        
    def compare_chain(self, chain, comp_chain):
        print('Comparing Chain %s to Chain %s' % (chain, comp_chain))
        #Compare the given chain to the compare chain and see whether it is a 
        #New Chain (0), Prepend (1), or Append (2) Scenario.  We return -1 if no change is necessary
        if len(comp_chain) < 1:
            print('Length of base chain less than 1')
            return 0
        elif len(chain) < 1:
            print('Length of compare chain less than 1')
            return -1
        else:
            #Compare the first elements
            if comp_chain[0].id == chain[0].id:
                print('First elements are equal')
                if len(comp_chain) > len(chain) - 1:
                    print('Length of base chain is greater than compare chain - 1')
                    return -1
                else:
                    return 2
            else:
                #The first elements aren't equal, we need to compare the other 
                #elements to determine whether it's a new chain or prepend scenario
                match=False
                match_indicator=False
                match_id=-1
                for link in chain:
                    print('Processing started for link with ID %s' % (link.id))
                    for element in comp_chain:
                        print('Compare started on element with ID %s' % (element.id))
                        if match==False:
                            print('Match is false')
                            if link.id == element.id:
                                print('Match found')
                                match=True
                                match_id = link.id
                if match:
                    #A match exists, meaning we have a prepend/append scenario
                    if comp_chain[0].id == match_id:
                        #The first element of the comparison chain is the match, 
                        #This is a pure prepend scenario
                        print('Prepend Scenario detected')
                        return 1
                    else:
                        #This is a tree scenario, which is a new chain scenario
                        print('New chain scenario detected')
                        return 0
                else:
                    #We have a new chain scenario
                    print('New chain scenario defaulted')
                    return 0
                    
    def connect_chain_to_tree(self, chain, tree):
        print('Is Chain Connected to Tree Called with chain that has start element ID %s' % (chain[0].id))
        
        self.print_trees()
        node=tree.root
        keep_going=True
        while keep_going:
            print('While loop entered')
            #Test for match
            print('Comparison started on %s and %s' % (node.data.next_action_id, chain[0].id))
            for act in node.data.next_action_list:
                if act.id == chain[0].id:
                    connected_node = node
                    print('matching node found with ID %s' % (node.data.id))
                    
                    #Add the chain onto the connected node
                    z=0
                    for z in range(0, len(chain)):
                        new_node = Node()
                        new_node.data=chain[z]
                        print('New Node added with ID %s' % (new_node.data.id))
                        connected_node.connections.append(new_node)
                        connected_node = new_node
                    return True
            if len(node.connections) == 0:
                keep_going=False
            
            #If no match was encountered, then we move on to the next node
            if len(node.connections) == 1:
                node = node.connections[0]
            else:
                for con in node.connections:
                    self.connect_chain_to_nodeset(chain, con)
        return False
                    
    def connect_chain_to_nodeset(self, chain, node):
        print('Is chain connected to nodeset called with chain %s and node %s' % (chain, node))
        while len(node.connections) != 0:
            #Test for match
            for el in chain:
                if node.data.next_action_id == el.id:
                    connected_node = node
                    print('matching node found with ID %s' % (node.data.id))
                    
                    #Add the chain onto the connected node
                    z=0
                    for z in range(0, len(chain)):
                        new_node = Node()
                        new_node.data=new_chain[z]
                        print('New Node added with ID %s' % (new_node.data.id))
                        connected_node.connections.append(new_node)
                        connected_node = new_node
                    return True
            
            #If no match was encountered, then we move on to the next node
            if len(node.connections) == 1:
                node = node.connections[0]
            else:
                for con in node.connections:
                    self.connect_chain_to_nodeset(chain, con)
        return False
            
    def build_keyactiontree(self):
        
        print('Build Key Action Tree Called')
        
        keep_going = True
        
        #Cycle through each action and take the following steps:
        #1. Compare to existing chains and, if already accounted for, do nothing
        #2. Build a full chain until an end point is reached, then push this to a list of lists (chains)
        # Splits are represented by new chains from the diverging node
        # Prepending Tail scenario common
        
        chain_list=[]
        
        #Check for already accounted for actions
        for action in self.keyactions:
            for chain in chain_list:
                for element in chain:
                    if action.id == element.id:
                        keep_going = False
                        
            if keep_going:
                
                #Build a chain list
                self.build_keyactionchain(action, chain_list)
        
        #Attach each chain into the final chain list
        #This step removes prepending scenarios
        
        #3 Distinct Possibilities:
        #New Chain: Create new tree
        #Prepend: Create a new tree, replace the old tree
        #Append: Add Brances to a tree
        final_list=[]
        prepend_list=[]
        for chain in chain_list:
            print('Processing Started for chain with first element ID %s and length %s' % (chain[0].id, len(chain)))
            if len(final_list) == 0:
                final_list.append(chain)
                print('First chain appended to final list')
            else:
                final_compare=-1
                for element in final_list:
                    print('Comparison against element in final list started')
                    comp = self.compare_chain(chain, element)
                    if comp > -1:
                        #If the final comparison is < comparison, then set to comparison
                        print('Compare result is %s' % (comp))
                        if final_compare<comp:
                            print('Final Compare is less than comparison')
                            final_compare=comp
                            prepend_list=element
                            
                if final_compare == 0 or final_compare == 2:
                    #New Chain
                    final_list.append(chain)
                    print('Chain with start element ID %s appended to final list')
                    
                elif final_compare == 1:
                    #Prepend
                    new_elements=[]
                    keep_running=True
                    for obj in chain:
                        if obj.id == prepend_list[0].id:
                            keep_running=False
                        elif keep_running:
                            new_elements.append(obj)
                           
                    e_counter=0
                    for e in new_elements:
                        prepend_list.insert(e_counter, e)
                        e_counter+=1
                        
        #Loop 1
        print('Now we have a list of chains, none of which overlap, we can build them into trees')
        for f in final_list:
            for c in f:
                print(c.id)
        chain_count=0
        for chain in final_list:

            #Determine which case we're dealing with, if a single stack it can
            #be added to the tree list.  If a branch then do nothing
            match_indicator=False
            for c in final_list:
                print('Comparison against chain with start element ID %s started' % (c[0].id))
                for el in c:
                    for na in el.next_action_list:
                        if na.id == chain[0].id:
                            match_indicator=True
                            print('Match encountered')
                    
            if match_indicator==False:
                #Create a tree from the chain and add it to the tree list
                chain_count+=1
                print('Root found, tree started')
                t = Tree()
                t.root.data = chain[0]
                i=1
                node=t.root
                print('Chain Length %s' % (len(chain)))
                for i in range(1, len(chain)):
                    new_node = Node()
                    new_node.data=chain[i]
                    print('Adding node with ID %s to tree' % (new_node.data.id))
                    node.connections.append(new_node)
                    node = new_node
                self.keyactiontreelist.append(t)
                    
        #Loop 2
        #Secondary Mechanism to prevent infinite loops
        original_chain_count=0
        no_match_counter=0
        no_match_limit=30
        while chain_count < len(final_list) and no_match_counter < no_match_limit:
            for chain in final_list:
                print('Processing started on chain with start element ID %s and length %s' % (chain[0].id, len(chain)))
                
                #Need to reverse the logic to add things onto existing trees instead of creating new ones
                
                #Determine which case we're dealing with, if a root then we should build it
                #and add it to the tree list once completed, then mark all the other chains to
                #not be considered in the rest of the loop.  If a branch do nothing.
            
                for tree in self.keyactiontreelist:
                    for el in chain:
                        #Check for existing key actions
                        match=True
                        for element in chain:
                            if self.is_element_in_tree(element.id, tree) == False:
                                match = False
                        
                        if match == False:
                            if self.is_element_connected_to_tree(el.id, tree):
                                print('Element in a tree references this chain')
                                #Pull the tree and add the chain
                                self.connect_chain_to_tree(chain, tree)
                                chain_count+=1
                if chain_count == original_chain_count:
                    no_match_counter+=1
                    print('No Match Counter Iterated')
                else:
                    original_chain_count=chain_count
                    no_match_counter=0