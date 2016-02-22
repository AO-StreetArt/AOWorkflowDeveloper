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
class Basic_Recursive_Iterator(object):
    """
    :param Tree tree: Internal tree
    """
    def __init__(self, tree):
        Tree_Iterator.__init__(self, tree, "Basic Recursive Iterator")
        
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
class Advanced_Recursive_Iterator(object):
    """
    :param Tree tree: Internal tree
    """
    def __init__(self, tree):
        Tree_Iterator.__init__(self, tree, "Basic Recursive Iterator")
        
    """
    :param Method function: The function to recurse (No parameters passed)
    """
    def iterate(self, function, func_param):
        self.process_node(function, self.tree.root, func_param)
        
    def process_node(self, function, node, func_param):
        function(func_param, node)
        if len(node.connections) > 0:
            for con in node.connections:
                self.process_node(function, con)
        else:
            return True