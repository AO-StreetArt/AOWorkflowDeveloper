# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 23:31:48 2015

2nd Version Flowchart Node

@author: alex barry
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from Connector import Connector
from Magnet import Magnet
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.logger import Logger

#This class defines a draggable image
class DraggableImage(Magnet):
    #The object to be dragged
    img = ObjectProperty(None, allownone=True)
    
    #The App Object
    app = ObjectProperty(None)
    
    #The Drag Grid
    grid = ObjectProperty(None)
    
    #Drag List Elements
    grid_layout = ObjectProperty(None)
    float_layout = ObjectProperty(None)
    
    #The cell currently occupied
    cell = ObjectProperty(None)
    
    #The flowchart node it belongs to
    node=ObjectProperty(None)
    
    #A Property to expose the on_double_press event
    double_press=ListProperty([0,0])
    is_double_pressed=BooleanProperty(False)
    
    def on_img(self, *args):
        self.clear_widgets()
        if self.img:
            Clock.schedule_once(lambda *x: self.add_widget(self.img), 0)

    def on_touch_down(self, touch, *args):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                self.double_press=touch.pos
                is_double_pressed = True
                
                #Set all other nodes to is_double_pressed = False
                for node in self.grid.nodes:
                    node.label.is_double_pressed=False
                
                self.app.LoadSideEditor(self)
                Logger.debug('Draggable double pressed at %s' % (self.double_press))
            else:
                #Grab the widget and pull the image out of the flowchart node
                touch.grab(self)
                self.remove_widget(self.img)
                self.app.root.get_screen('workflow').add_widget(self.img)
                self.img.center = touch.pos
            return True

        return super(DraggableImage, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):

        #If the node is grabbed, move the image center to the touch position
        #If the widget is grabbed
        if touch.grab_current == self:
            #Move the image to the touch position
            self.img.center = touch.pos
        return super(DraggableImage, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if touch.grab_current == self:
            if self.grid.collide_point(*touch.pos):
                for cel in self.grid.cells:
                    if cel.collide_point(*touch.pos):
                        self.node.parent.clear_widgets()
                        self.app.root.get_screen('workflow').remove_widget(self.img)
                        self.cell=cel
                        self.node.cell=cel
                        self.cell.add_widget(self.node)
                        self.add_widget(self.img)
                        touch.ungrab(self)
                        return True
                self.app.root.get_screen('workflow').remove_widget(self.img)
                self.cell=1
                self.add_widget(self.img)
                touch.ungrab(self)
                return True
            elif self.grid_layout.collide_point(*touch.pos) or self.float_layout.collide_point(*touch.pos):
                
                #Eliminate the node from the nodes and connections list
                self.grid.nodes.remove(self.node)
                i=0
                temp_con = []
                temp_con.append([])
                temp_con.append([])
                for action in self.grid.connections[0]:
                    if self.grid.connections[0][i] != self.node and self.grid.connections[1][i] != self.node:
                        temp_con[0].append(self.grid.connections[0][i])
                        temp_con[1].append(self.grid.connections[1][i])
                self.grid.connections = temp_con
                
                #Remove the node from the flowchart
                self.cell.remove_widget(self.node)
                self.app.root.get_screen('workflow').remove_widget(self.node.label.img)
                
                #Add the image to the grid layout
                self.app.add_draggable_node(self.node.label.img)
                
            else:
                self.node.parent.clear_widgets()
                self.app.root.get_screen('workflow').remove_widget(self.img)
                self.cell.add_widget(self.node)
                self.add_widget(self.img)
                touch.ungrab(self)
        Clock.schedule_once(self.node.update_connections)
        return super(DraggableImage, self).on_touch_up(touch, *args)

class ConnectorForward(ToggleButton):
    
    grid=ObjectProperty(None)
    connections=ListProperty([])
    node=ObjectProperty(None)
    matching_connection=ObjectProperty(None)
    connector_color=ListProperty([1, 1, 1])
    
    def __init__(self, **kwargs):
        
        super(ConnectorForward, self).__init__(**kwargs)
        self.background_down='src/flowcharts/img/drag_node_down_small.png'
        self.background_normal='src/flowcharts/img/drag_node_small.png'
        self.group='front'
        self.bind(on_press=self.create_connections)
        
    def create_connections(self, *args):
        keep_going=False
        match=False
        
        for node in self.grid.nodes:
            if node.receiver.state=='down':
                keep_going=True
                Logger.debug('FlowChart: Active Receiver Detected')
        
        if keep_going:
                
            for node in self.grid.nodes:
                if node.receiver.state=='down':
                    if node != self.node:
                        self.state='normal'
                        node.receiver.state='normal'
#                        connector = Connector(line_color=self.connector_color)
#                        self.connections.append(connector)
#                        self.node.connections.append(node)
#                        self.matching_connection=node
                        
                        #Validate for duplicates
                        j=0
                        for con_start in self.grid.connections[0]:
                            if self.node == self.grid.connections[0][j] and node == self.grid.connections[1][j]:
                                match=True
                                Logger.debug('Duplicate Connection Found: %s, %s' % (str(self.grid.connections[0][j]), str(self.grid.connections[1][j])))
                                con_out_1 = ""
                                i=0
                                for connection in self.grid.connections[0]:
                                    con_out_1+="%s, %s" % (str(self.grid.connections[0][i]), str(self.grid.connections[1][i]))
                                    i+=1
                                Logger.debug('Current Grid Connections are: %s' % (con_out_1))
                                
                                i=0
                                con_out_2 = ""
                                for connection in self.node.connections:
                                    con_out_2+=str(connection)
                                Logger.debug('Current node connections are: %s' % (con_out_2))
                                
                                self.grid.connections[0].remove(self.grid.connections[0][j])
                                self.grid.connections[1].remove(self.grid.connections[1][j])
                                self.node.connections.remove(node)
                            j+=1
                                
                                
                        if match == False:
                            connector = Connector(line_color=self.connector_color)
                            self.connections.append(connector)
                            self.node.connections.append(node)
                            self.matching_connection=node
                            self.grid.connections[0].append(self.node)
                            self.grid.connections[1].append(self.matching_connection)
                            Logger.debug('FlowChart: Matching Connector appended: Node 1 %s & Node 2 %s' % (self.node, self.matching_connection))
                            
                            con_out_1 = ""
                            i=0
                            for connection in self.grid.connections[0]:
                                con_out_1+="%s, %s" % (str(self.grid.connections[0][i]), str(self.grid.connections[1][i]))
                                i+=1
                            Logger.debug('Current Grid Connections are: %s' % (con_out_1))
                            
                            i=0
                            con_out_2 = ""
                            for connection in self.node.connections:
                                con_out_2+=str(connection)
                            Logger.debug('Current node connections are: %s' % (con_out_2))
                    
            #Add the connections to the widget
            for connect in self.connections:
                self.clear_widgets()
                self.add_widget(connect)
                connect.front=self.center
#                connect.back=self.matching_connection.receiver.center
                Logger.debug('FlowChart: Connections Updated')
    
class ConnectorBack(ToggleButton):
    app=ObjectProperty(None)
    node=ObjectProperty(None)
    grid=ObjectProperty(None)
    def __init__(self, **kwargs):
        
        super(ConnectorBack, self).__init__(**kwargs)
        self.background_down='src/flowcharts/img/drag_node_down_small.png'
        self.background_normal='src/flowcharts/img/drag_node_small.png'
        self.group='back'
        self.bind(on_press=self.make_connections)
        
    def make_connections(self, *args):
        for node in self.grid.nodes:
            if node.connector.state=='down':
                node.connector.create_connections()
                Logger.debug('FlowChart: Active Connector Detected')

class FlowChartNode(BoxLayout):
    
    #The label for the widget
    #Exposed so that any widget can be added
    label = ObjectProperty(None)
    
    #The app being added to
    app = ObjectProperty(None)
    
    #The Grid the widget is in
    grid = ObjectProperty(None)
    
    #The cell the widget is currently in
    cell = ObjectProperty(None)
    
    #Internal Properties
    #The connector node for the widget
    connector = ObjectProperty(None)
    
    #The receiver for the widget
    receiver = ObjectProperty(None)
    
    #A list of forward connections to other nodes
    connections = ListProperty([])
    
    row1=ObjectProperty(None)
    row2=ObjectProperty(None)
    row3=ObjectProperty(None)
    
    def __init__(self, **kwargs):
        
        super(FlowChartNode, self).__init__(**kwargs)
        
        con = ConnectorForward(grid=self.grid, node=self)
        Logger.debug('Flowchart: ConnectorNode: Connector Node initialized with grid %s' % (self.grid))
        rec = ConnectorBack(app=self.app, node=self, grid=self.grid)
        self.connector = con
        self.receiver = rec

        Clock.schedule_once(self.build_widget)
        
    def build_widget(self, *args):
        row1 = BoxLayout(size_hint=[1, 0.3])
        row2 = BoxLayout(size_hint=[1, 0.4])
        row3 = BoxLayout(size_hint=[1, 0.3])
        self.row1=row1
        self.row2=row2
        self.row3=row3
        buf1 = BoxLayout(size_hint=[0.35, 1])
        buf2 = BoxLayout(size_hint=[0.35, 1])
        buf3 = BoxLayout(size_hint=[0.35, 1])
        buf4 = BoxLayout(size_hint=[0.35, 1])
        
        self.connector.size_hint=[0.3, 1]
        self.receiver.size_hint=[0.3, 1]
        self.label.size_hint=[1, 1]
        
        self.orientation='vertical'
        row1.orientation='horizontal'
        row2.orientation='horizontal'
        row3.orientation='horizontal'
        
        row1.add_widget(buf1)
        row1.add_widget(self.receiver)
        row1.add_widget(buf2)
        row2.add_widget(self.label)
        row3.add_widget(buf3)
        row3.add_widget(self.connector)
        row3.add_widget(buf4)
        
        self.add_widget(row1)
        self.add_widget(row2)
        self.add_widget(row3)
        
    def clear_all_widgets(self, *args):
        self.clear_widgets()
        self.connector.clear_widgets()
        
    def update_connections(self, *args):
        i=0
        self.connector.clear_widgets()
        Logger.debug('FlowChart: Connections Updated')
        for con in self.connections:
            self.connector.add_widget(self.connector.connections[i])
            self.connector.connections[i].front=self.connector.center
            self.connector.connections[i].back=con.receiver.center
            i+=1