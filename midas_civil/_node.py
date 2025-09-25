
from ._mapi import *
from ._utils import *
from math import hypot
from ._group import _add_node_2_stGroup

def dist_tol(a,b):
    return hypot((a.X-b.X),(a.Y-b.Y),(a.Z-b.Z)) < 0.00001  #TOLERANCE BUILT IN (UNIT INDEP)

def cell(point,size=1): #SIZE OF GRID
    return str(f"{int(point.X//size)},{int(point.Y//size)},{int(point.Z//size)}")


# -------- FUNCTIONS ARE DEFINED BELOW TO RECOGNISE NODE CLASS ----------------



#5 Class to create nodes
class Node:
    """X ordinate, Y ordinate, Z ordinate, Node ID (optional). \nSample: Node(1,0,5)"""
    nodes = [] # Node object stores in a list
    ids = []    # Node IDs used for auto increment of ID and replacement of nodes
    Grid ={}    # Node object in cube grid
    __nodeDic__ = {} # Stores
    def __init__(self,x,y,z,id=0,group='',merge=1):
        ''' Create Node object

            Parameters:
                x: X - ordinate of node
                y: Y - ordinate of node 
                z: Z - ordinate of node
                id: Node ID (default 0 for auto-increment)
                mat: Material property number (default 1)
                group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
                merge: If enabled, checks for existing nodes and return their IDs. No additional/duplicate node will be created.
            
            Examples:
                ```python
                Node(0,0,0, id =1 , group = 'Support', merge=1)
                ```
                
        '''


        #----------------- ORIGINAL -----------------------
    
        if Node.ids == []: 
            node_count = 1
        else:
            node_count = max(Node.ids)+1
        
        
        self.X = round(x,6)
        self.Y = round(y,6)
        self.Z = round(z,6)

        if id == 0 : self.ID = node_count
        if id != 0 : self.ID = id


        #REPLACE - No merge check
        if id in Node.ids:

            index=Node.ids.index(id)
            n_orig = Node.nodes[index]
            loc_orig = str(cell(n_orig))
            Node.Grid[loc_orig].remove(n_orig)

            loc_new = str(cell(self))
            
            zz_add_to_dict(Node.Grid,loc_new,self)
            Node.nodes[index]=self
            Node.__nodeDic__[str(id)] = self


        #CREATE NEW - Merge Check based on input
        else:
            self.AXIS = [[0,0,0],[0,0,0],[0,0,0]]
            cell_loc = str(cell(self))      

            if cell_loc in Node.Grid:

                if merge == 1:
                    chk=0   #OPTIONAL
                    for node in Node.Grid[cell_loc]:
                        if dist_tol(self,node):
  
                            chk=1
                            self.ID=node.ID
                            self.AXIS = node.AXIS
                    if chk==0:

                        self.AXIS = [[0,0,0],[0,0,0],[0,0,0]]
                        Node.nodes.append(self)
                        Node.ids.append(self.ID)
                        Node.Grid[cell_loc].append(self)
                        

                else:

                    Node.nodes.append(self)
                    Node.ids.append(self.ID)
                    Node.Grid[cell_loc].append(self)
            else:

                Node.Grid[cell_loc]=[]
                Node.nodes.append(self)
                Node.ids.append(self.ID)
                Node.Grid[cell_loc].append(self)
            Node.__nodeDic__[str(self.ID)] = self
            
        if group !="":
            _add_node_2_stGroup(self.ID,group)

        
    def __str__(self):
        return f"NODE ID : {self.ID} | X:{self.X} , Y:{self.Y} , Z:{self.Z} \n {self.__dict__}"

    @classmethod
    def json(cls):
        json = {"Assign":{}}
        for i in cls.nodes:
            json["Assign"][i.ID]={"X":i.X,"Y":i.Y,"Z":i.Z}
        return json
    
    @staticmethod
    def create():
        MidasAPI("PUT","/db/NODE",Node.json())
        
    @staticmethod
    def get():
        return MidasAPI("GET","/db/NODE")
    
    @staticmethod
    def sync():
        Node.nodes=[]
        Node.ids=[]
        Node.Grid={}
        Node.__nodeDic__ = {}
        a = Node.get()
        if a != {'message': ''}:
            if list(a['NODE'].keys()) != []:
                for j in a['NODE'].keys():
                    Node(round(a['NODE'][j]['X'],6), round(a['NODE'][j]['Y'],6), round(a['NODE'][j]['Z'],6), id=int(j), group='', merge=0)


    @staticmethod
    def delete():
        MidasAPI("DELETE","/db/NODE/")
        Node.nodes=[]
        Node.ids=[]
        Node.Grid={}
        Node.__nodeDic__ = {}

    @staticmethod
    def clear():
        Node.nodes=[]
        Node.ids=[]
        Node.Grid={}
        Node.__nodeDic__ = {}








# ---- GET NODE OBJECT FROM ID ----------

# def nodeByID(nodeID:int) -> Node:
#     ''' Return Node object with the input ID '''
#     for node in Node.nodes:
#         if node.ID == nodeID:
#             return node
        
#     print(f'There is no node with ID {nodeID}')
#     return None



def nodeByID(nodeID:int) -> Node:
    ''' Return Node object with the input ID '''
    try:
        return (Node.__nodeDic__[str(nodeID)])
    except:
        print(f'There is no node with ID {nodeID}')
        return None





class NodeLocalAxis:
    skew = []
    ids = [] 

    def __init__(self,nodeID,type,angle):
        '''
        nodeID(int) : ID of the node
        axis (str) : Axis of rotation, 'X' , 'Y' , 'Z' , 'XYZ' or 'Vector'
        angle (float) : Angle of rotation if axis = 'X' , 'Y' or 'Z'  ;
        angle (list : float) = [30,0,0] if type = 'XYZ'
        angle (list : vector) -> node.AXIS = [[1,0,0],[0,1,0]] if type = 'Vector'
        '''

        self.ID = nodeID

        if nodeID in NodeLocalAxis.ids:
            index = NodeLocalAxis.ids.index(nodeID)
            intial_angle = NodeLocalAxis.skew[index].ANGLE
            if intial_angle == [[0,0,0],[0,0,0],[0,0,0]]:
                intial_angle = [[1,0,0],[0,1,0],[0,0,1]]

            if type == 'Vector':
                self.TYPE = 'VEC'
                self.VEC = angle
            elif type == 'X':
                self.TYPE = 'ANGLE'
                self.ANGLE = [angle,intial_angle[1],intial_angle[2]]
            elif type == 'Y':
                self.TYPE = 'ANGLE'
                self.ANGLE = [intial_angle[0],angle,intial_angle[2]]
            elif type == 'Z':
                self.TYPE = 'ANGLE'
                self.ANGLE = [intial_angle[0],intial_angle[1],angle]
            elif type == 'XYZ':
                self.TYPE = 'ANGLE'
                self.ANGLE = angle
            NodeLocalAxis.skew[index] = self
        else:
            if type == 'Vector':
                self.TYPE = 'VEC'
                self.VEC = angle
                self.ANGLE = [0,0,0]
            elif type == 'X':
                self.TYPE = 'ANGLE'
                self.ANGLE = [angle,0,0]
            elif type == 'Y':
                self.TYPE = 'ANGLE'
                self.ANGLE = [0,angle,0]
            elif type == 'Z':
                self.TYPE = 'ANGLE'
                self.ANGLE = [0,0,angle]
            elif type == 'XYZ':
                self.TYPE = 'ANGLE'
                self.ANGLE = angle
        
            NodeLocalAxis.skew.append(self)
            NodeLocalAxis.ids.append(self.ID)

    @classmethod
    def json(cls):
        json = {"Assign":{}}
        for i in cls.skew:
            if i.TYPE == 'ANGLE':
                json["Assign"][i.ID]={
                                    "iMETHOD": 1,
                                    "ANGLE_X": i.ANGLE[0],
                                    "ANGLE_Y": i.ANGLE[1],
                                    "ANGLE_Z": i.ANGLE[2]
                                }
            elif i.TYPE == 'VEC':
                json["Assign"][i.ID]={
                                    "iMETHOD": 3,
                                    "V1X": i.VEC[0][0],
                                    "V1Y": i.VEC[0][1],
                                    "V1Z": i.VEC[0][2],
                                    "V2X": i.VEC[1][0],
                                    "V2Y": i.VEC[1][1],
                                    "V2Z": i.VEC[1][2]
                                }
        return json
    
    @staticmethod
    def create():
        MidasAPI("PUT","/db/SKEW",NodeLocalAxis.json())

    @staticmethod
    def delete():
        MidasAPI("DELETE","/db/SKEW/")
        NodeLocalAxis.skew=[]
        NodeLocalAxis.ids=[]

    @staticmethod
    def get():
        return MidasAPI("GET","/db/SKEW")
    
    # @staticmethod
    # def sync():
    #     NodeLocalAxis.skew=[]
    #     NodeLocalAxis.ids=[]
    #     a = NodeLocalAxis.get()
    #     if a != {'message': ''}:
    #         if list(a['NODE'].keys()) != []:

    #             for j in a['NODE'].keys():

    #                 Node(round(a['NODE'][j]['X'],6), round(a['NODE'][j]['Y'],6), round(a['NODE'][j]['Z'],6), id=int(j), group='', merge=0)