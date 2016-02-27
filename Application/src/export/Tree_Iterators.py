# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 18:38:26 2016

Tree Iterators

@author: alex
"""

#Base class which other iterators will inherit from
class Tree_Iterator(object):
    
    """
    :param Tree tree: Internal tree
    :param String name: Iterator name
    """
    def __init__(self, tree, name):
        self.tree = tree
        self.name = name
        
    def get_name(self):
        return self.name
        
    """
    :param Method function: The function to recurse
    """
    def iterate(self, function):
        pass
        #This is implemented and called in each successive iterator to determine how iterations happen
        
#--------Example of passing function down the stack--------
#        class Foo(object):
#            def method1(self):
#                pass
#            def method2(self, method):
#                return method()
#        
#        foo = Foo()
#        foo.method2(foo.method1)
#        
#From http://stackoverflow.com/questions/706721/how-do-i-pass-a-method-as-a-parameter-in-python#706735
        
        
#Basic Recursive Operator that supports functions without the actual node or any other parameters
class Basic_Recursive_Iterator(Tree_Iterator):
    """
    :param Tree tree: Internal tree
    """
    def __init__(self, tree):
        super(Basic_Recursive_Iterator, self).__init__(tree, "Basic Recursive Iterator")
        
    """
    :param Method function: The function to recurse (No parameters passed)
    """
    def iterate(self, function):
        self.process_node(function, self.tree.root)
        
    def process_node(self, function, node):
        function()
        if len(node.connections) > 0:
            for con in node.connections:
                self.process_node(function, con)
        else:
            return True
            
#Advanced Recursive Operator that supports functions with the actual node and a single parameter
class Advanced_Recursive_Iterator(Tree_Iterator):
    """
    :param Tree tree: Internal tree
    """
    def __init__(self, tree):
        super(Advanced_Recursive_Iterator, self).__init__(tree, "Advanced Recursive Iterator")
        
    """
    :param Method function: The function to recurse (1 parameter passed)
    """
    def iterate(self, function, **kwargs):
        self.process_node(function, self.tree.root, **kwargs)
        
    def process_node(self, function, node, **kwargs):
        function(node, **kwargs)
        if len(node.connections) > 0:
            for con in node.connections:
                self.process_node(function, con, **kwargs)
        else:
            return True
            
#Tail Recursion Iterator that supports functions with the actual node and a single parameter
class Tail_Recursion_Iterator(Tree_Iterator):
    """
    :param Tree tree: Internal tree
    """
    def __init__(self, tree):
        super(Tail_Recursion_Iterator, self).__init__(tree, "Tail Recursion Iterator")
        
    """
    :param Method function: The function to recurse (1 parameter passed)
    """
    def iterate(self, function, **kwargs):
        self.process_node(function, self.tree.root, **kwargs)
        
    def process_node(self, function, node, **kwargs):
        while len(node.connections) == 1:
            function(node, **kwargs)
            node=node.connections[0]
        if len(node.connections) > 1:
            for con in node.connections:
                self.process_node(function, con, **kwargs)
        else:
            return True
            
#Chain Iterator that supports functions with the actual node and a single parameter
class Chain_Iterator(Tree_Iterator):
    """
    :param Tree tree: Internal tree
    """
    def __init__(self, tree):
        super(Chain_Iterator, self).__init__(tree, "Chain Iterator")
        
    """
    :param Method function: The function to recurse (1 parameter passed)
    """
    def iterate(self, function, **kwargs):
        chain_list=[]
        self.process_node(function, self.tree.root, chain_list, **kwargs)
        for chain in chain_list:
            for element in chain:
                function(element, **kwargs)
        
    def process_node(self, function, node, chain_list, **kwargs):
        chain=[]
        while len(node.connections) == 1:
            chain.append(node.connections[0])
            node=node.connections[0]
        if len(node.connections) > 1:
            chain.append(node.connections[0])
            node=node.connections[0]
            chain_list.append(chain)
            for con in node.connections:
                self.process_node(function, con, chain_list, **kwargs)
        else:
            chain.append(node.connections[0])
            node=node.connections[0]
            chain_list.append(chain)
            return True
            
#Chain Iterator that supports pre & post functions, 
#and a main function with the actual node and any number of parameters
class Advanced_Chain_Iterator(Tree_Iterator):
    """
    :param Tree tree: Internal tree
    """
    def __init__(self, tree):
        super(Chain_Iterator, self).__init__(tree, "Advanced Chain Iterator")
        
    """
    :param Method function: The function to recurse (1 parameter passed)
    """
    def iterate(self, pre_function, function, post_function, **kwargs):
        chain_list=[]
        self.process_node(function, self.tree.root, chain_list, **kwargs)
        for chain in chain_list:
            pre_function(**kwargs)
            for element in chain:
                function(element, **kwargs)
            post_function(**kwargs)
        
    def process_node(self, function, node, chain_list, **kwargs):
        chain=[]
        while len(node.connections) == 1:
            chain.append(node.connections[0])
            node=node.connections[0]
        if len(node.connections) > 1:
            chain.append(node.connections[0])
            node=node.connections[0]
            chain_list.append(chain)
            for con in node.connections:
                self.process_node(function, con, chain_list, **kwargs)
        else:
            chain.append(node.connections[0])
            node=node.connections[0]
            chain_list.append(chain)
            return True