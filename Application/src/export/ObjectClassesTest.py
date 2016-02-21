# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 23:33:09 2016

@author: alex
"""

from ObjectClasses import Node, Tree, _KeyAction, _InputParameter, _Workflow

#Tree Test
node1 = Node()
node1.data = 1
node2 = Node()
node2.data = 2
node3 = Node()
node3.data = 3
node4 = Node()
node4.data = 4
node5 = Node()
node5.data = 5

tree = Tree()
tree.root = node1
tree.root.connections.append(node2)
tree.root.connections[0].connections.append(node3)
node2.connections.append(node4)
node4.connections.append(node5)

print(tree.root.data)
for con in tree.root.connections:
    print(con.data)
    for connection in con.connections:
        print(connection.data)
        
#Key Action Tests
act = _KeyAction()
act.id=1
act2 = _KeyAction()
act2.id=2
act3 = _KeyAction()
act3.id=3

ip=_InputParameter()
ip.id=1
ip2 = _InputParameter()
ip2.id=2
ip3=_InputParameter()
ip3.id=3
ip4 = _InputParameter()
ip4.id=4
ip5=_InputParameter()
ip5.id=5
ip6 = _InputParameter()
ip6.id=6

act.add_inputparameter(ip)
print(act.numParams())

act.add_inputparameter(ip2)
print(act.numParams())

act2.add_inputparameter(ip3)
print(act2.numParams())

act2.add_inputparameter(ip4)
print(act2.numParams())

act3.add_inputparameter(ip5)
print(act3.numParams())

act3.add_inputparameter(ip6)
print(act3.numParams())

act.clear_inputparameters()
print(act.numParams())

act.add_inputparameter(ip)
print(act.numParams())

act.add_inputparameter(ip2)
print(act.numParams())

act4 = _KeyAction()
act4.id=4
act5 = _KeyAction()
act5.id=5
act6 = _KeyAction()
act6.id=6
act.name = "AND"
act2.name = "OR"
act3.name="a"
act4.name="b"
act5.name="c"
act6.name="d"

act.add_nextaction(act2)
act2.add_nextaction(act3)
act.add_nextaction(act4)
act5.add_nextaction(act6)
act3.add_nextaction(act5)

#Workflow Tests

flow = _Workflow()
flow.add_keyaction(act)
flow.add_keyaction(act2)
flow.add_keyaction(act3)
flow.add_keyaction(act4)
flow.add_keyaction(act5)
flow.add_keyaction(act6)
flow.build_keyactiontree()

for tree in flow.keyactiontreelist:
    print(tree.root.data.id)
    for con in tree.root.connections:
        print(con.data.id)
        for connection in con.connections:
            print(connection.data.id)
            for c in connection.connections:
                print(c.data.id)
                for a in c.connections:
                    print(a.data.id)
                    
#Linear flow test
aact = _KeyAction()
aact.id=7
aact2 = _KeyAction()
aact2.id=8
aact3 = _KeyAction()
aact3.id=9
aact4 = _KeyAction()
aact4.id=10
aact5 = _KeyAction()
aact5.id=11
aact6 = _KeyAction()
aact6.id=12

aact.add_nextaction(aact2)
aact2.add_nextaction(aact3)
aact3.add_nextaction(aact4)
aact4.add_nextaction(aact5)
aact5.add_nextaction(aact6)

flow2 = _Workflow()
flow2.add_keyaction(aact)
flow2.add_keyaction(aact2)
flow2.add_keyaction(aact3)
flow2.add_keyaction(aact4)
flow2.add_keyaction(aact5)
flow2.add_keyaction(aact6)

flow2.build_keyactiontree()
for tree in flow2.keyactiontreelist:
    print(tree.root.data.id)
    for con in tree.root.connections:
        print(con.data.id)
        for connection in con.connections:
            print(connection.data.id)
            for c in connection.connections:
                print(c.data.id)
                for a in c.connections:
                    print(a.data.id)
                    for b in a.connections:
                        print(b.data.id)
                        
#Branch out flow test
bact = _KeyAction()
bact.id=13
bact2 = _KeyAction()
bact2.id=14
bact3 = _KeyAction()
bact3.id=15
bact4 = _KeyAction()
bact4.id=16
bact5 = _KeyAction()
bact5.id=17
bact6 = _KeyAction()
bact6.id=18
bact7 = _KeyAction()
bact7.id=19
bact8 = _KeyAction()
bact8.id=20

bact.add_nextaction(bact2)
bact2.add_nextaction(bact3)
bact2.add_nextaction(bact4)
bact3.add_nextaction(bact5)
bact4.add_nextaction(bact6)
bact6.add_nextaction(bact7)
bact6.add_nextaction(bact8)

flow3 = _Workflow()
flow3.add_keyaction(bact)
flow3.add_keyaction(bact2)
flow3.add_keyaction(bact3)
flow3.add_keyaction(bact4)
flow3.add_keyaction(bact5)
flow3.add_keyaction(bact6)
flow3.add_keyaction(bact7)
flow3.add_keyaction(bact8)

flow3.build_keyactiontree()
for tree in flow3.keyactiontreelist:
    print(tree.root.data.id)
for con in tree.root.connections:
    print(con.data.id)
for con in tree.root.connections[0].connections:
    print(con.data.id)
for con in tree.root.connections[0].connections[0].connections:
    print(con.data.id)
for con in tree.root.connections[0].connections[1].connections:
    print(con.data.id)
for con in tree.root.connections[0].connections[1].connections[0].connections:
    print(con.data.id)
    
flow3.print_trees()