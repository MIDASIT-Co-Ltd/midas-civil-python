
from ._mapi import *
from ._utils import *
from math import hypot




def dist_tol(a,b):
    return hypot((a.X-b.X),(a.Y-b.Y),(a.Z-b.Z)) < 0.00001  #TOLERANCE BUILT IN (UNIT INDEP)

def cell(point,size=1): #SIZE OF GRID
    return (int(point.X//size),int(point.Y//size),int(point.Z//size))

#-- NEW SYSTEM

#5 Class to create nodes
class Node:
    """X ordinate, Y ordinate, Z ordinate, Node ID (optional). \nSample: Node(1,0,5)"""
    nodes = []
    ids = []
    Grid ={}
    def __init__(self,x,y,z,id=0,merge=1):


        #----------------- ORIGINAL -----------------------
    
        if Node.ids == []: 
            node_count = 1
        else:
            node_count = max(Node.ids)+1
        
        
        self.X = x
        self.Y = y
        self.Z = z

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
        a = Node.get()
        if a != {'message': ''}:
            if list(a['NODE'].keys()) != []:
                Node.nodes = []
                Node.ids=[]
                for j in a['NODE'].keys():
                    Node(round(a['NODE'][j]['X'],6), round(a['NODE'][j]['Y'],6), round(a['NODE'][j]['Z'],6),int(j),0)

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

    @staticmethod
    def delete():
        MidasAPI("DELETE","/db/NODE/")
        Node.nodes=[]
        Node.ids=[]
        Node.Grid={}















