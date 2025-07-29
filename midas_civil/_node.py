
from ._mapi import *
from ._utils import *
from math import hypot
from ._group import _add_node_2_stGroup



def dist_tol(a,b):
    return hypot((a.X-b.X),(a.Y-b.Y),(a.Z-b.Z)) < 0.00001  #TOLERANCE BUILT IN (UNIT INDEP)

def cell(point,size=1): #SIZE OF GRID
    return (int(point.X//size),int(point.Y//size),int(point.Z//size))


# -------- FUNCTIONS ARE DEFINED BELOW TO RECOGNISE NODE CLASS ----------------



#5 Class to create nodes
class Node:
    """X ordinate, Y ordinate, Z ordinate, Node ID (optional). \nSample: Node(1,0,5)"""
    nodes = []
    ids = []
    Grid ={}
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


        #CREATE NEW - Merge Check based on input
        else:
            cell_loc = str(cell(self))      

            if cell_loc in Node.Grid:
                if merge == 1:
                    chk=0   #OPTIONAL
                    for node in Node.Grid[cell_loc]:
                        if dist_tol(self,node):
                            chk=1
                            self.ID=node.ID
                    if chk==0:
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
            
        if group !="":
            _add_node_2_stGroup(self.ID,group)

        


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
        a = Node.get()
        if a != {'message': ''}:
            if list(a['NODE'].keys()) != []:
                for j in a['NODE'].keys():
                    Node(round(a['NODE'][j]['X'],6), round(a['NODE'][j]['Y'],6), round(a['NODE'][j]['Z'],6), id=int(j), group='', merge=0)

    @staticmethod
    def delete2(nodes_list):
        if type(nodes_list)!=list:
            nodes_list = [nodes_list]
        url_add = arr2csv(nodes_list)

        MidasAPI("DELETE",f"/db/NODE/{url_add}")


    @staticmethod
    def delete3(*args):
        try:
            args2=sFlatten(args)
            url_add = arr2csv(args2)
            MidasAPI("DELETE",f"/db/NODE/{url_add}") 
        except:
            MidasAPI("DELETE",f"/db/NODE/")
            Node.nodes=[]
            Node.ids=[]
            Node.Grid={}

    @staticmethod
    def delete():
        MidasAPI("DELETE","/db/NODE/")
        Node.nodes=[]
        Node.ids=[]
        Node.Grid={}








# ---- GET NODE OBJECT FROM ID ----------

def nodeByID(nodeID:int) -> Node:
    ''' Return Node object with the input ID '''
    for node in Node.nodes:
        if node.ID == nodeID:
            return node
        
    print(f'There is no node with ID {nodeID}')
    return None







