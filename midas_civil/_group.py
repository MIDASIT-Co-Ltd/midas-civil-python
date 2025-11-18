
from ._mapi import *

from ._utils import _convItem2List
from ._utils import sFlatten

# ----------- HELPER FUNCTION -----------
    # --------   RETRIEVE NODE / ELEMENT FROM STRUCTURE GROUP -------

def nodesInGroup(groupName:str,unique:bool=True,reverse:bool=False) -> list:
    ''' Returns Node ID list in a Structure Group or list of Structure groups
    eg. nodesInGroup('SG_A')   
        nodesInGroup(['SG_1','SG_2','SG_3'])
        groupName : 'SG_A' or ['SG_1' , 'SG_2' , 'SG_2']
        unique : True -> Only unique ID is returned.
        In case of multiple groups, we may require only uniques ids
        reverse : True -> Reverses the returned list
    '''
    groupNames = _convItem2List(groupName)
    nlist = []
    for gName in groupNames:
        chk=1
        rev = reverse
        if gName[0] == '!':
            gName = gName[1:]
            rev = not rev
        for i in Group.Structure.Groups:
                if i.NAME == gName:
                    chk=0
                    nIDlist = i.NLIST
                    if rev: nIDlist = list(reversed(nIDlist))
                    nlist.append(nIDlist)
        if chk:
            print(f'⚠️   "{gName}" - Structure group not found !')
    if unique:
        return list(dict.fromkeys(sFlatten(nlist)))
    return sFlatten(nlist)


def elemsInGroup(groupName:str,unique:bool=True,reverse:bool=False) -> list:
    ''' Returns Element ID list in a Structure Group '''
    groupNames = _convItem2List(groupName)
    elist = []
    for gName in groupNames:
        chk=1
        rev = reverse
        if gName[0] == '!':
            gName = gName[1:]
            rev = not rev
        for i in Group.Structure.Groups:
                if i.NAME == gName:
                    chk=0
                    eIDlist = i.ELIST
                    if rev: eIDlist = list(reversed(eIDlist))
                    elist.append(eIDlist)
        if chk:
            print(f'⚠️   "{gName}" - Structure group not found !')
    if unique:
        return list(dict.fromkeys(sFlatten(elist)))
    return sFlatten(elist)


    # --------   ADD ELEMENT TO STRUCTURE GROUP -------

def _add_elem_2_stGroup(elemID,groupName):
    up = 0
    if groupName in Group.Structure._names:
        for i in Group.Structure.Groups:
            if i.NAME == groupName:
                i.ELIST = list(i.ELIST + [elemID])
    else:
        Group.Structure(groupName)
        _add_elem_2_stGroup(elemID,groupName)



def _add_node_2_stGroup(nodeID,groupName):
    if groupName in Group.Structure._names:
        for i in Group.Structure.Groups:
            if i.NAME == groupName:
                if nodeID not in i.NLIST:
                    i.NLIST = list(i.NLIST + [nodeID])
    else:
        Group.Structure(groupName)
        _add_node_2_stGroup(nodeID,groupName)


#---------------------------------------------------------------------------------------------------------------
class Group:

    @classmethod
    def create(cls):
        if cls.Structure.Groups!=[]: cls.Structure.create()
        if cls.Boundary.Groups!=[]:cls.Boundary.create()
        if cls.Load.Groups!=[]:cls.Load.create()
        if cls.Tendon.Groups!=[]:cls.Tendon.create()

    @classmethod
    def sync(cls):
        cls.Structure.sync()
        cls.Boundary.sync()
        cls.Load.sync()
        cls.Tendon.sync()
        
    @classmethod
    def delete(cls):
        cls.Structure.delete()
        cls.Boundary.delete()
        cls.Load.delete()
        cls.Tendon.delete()
        
    


#---------------------------------         STRUCTURE       ---------------------------------------


    class Structure:

        Groups = []
        ids=[]
        _names = []
        url= "/db/GRUP"

        def __init__(self, name:str, nlist:list=[],elist:list=[]):
            """"""
            self.NAME = name
            if Group.Structure.Groups == []: self.ID=1
            else: self.ID= max(Group.Structure.ids)+1
            self.ELIST = list(set(elist))
            self.NLIST = list(set(nlist))
            Group.Structure.ids.append(self.ID)
            Group.Structure.Groups.append(self)
            Group.Structure._names.append(self.NAME)
    
        @classmethod
        def update(cls, name,operation = "r", nlist = [],elist = [] ):
            """Group name, element list, node list, operation ("add" or "replace").\n
            Sample:  update_SG("Girder", [1,2,...20],[],"replace")"""
            up = 0
            for i in cls.Groups:
                if name == i.NAME:
                    up = 1
                    if operation == "r":
                        i.ELIST = list(set(elist))
                        i.NLIST = list(set(nlist))
                    if operation == "a":
                        i.ELIST = list(set(i.ELIST + elist))
                        i.NLIST = list(set(i.NLIST + nlist))
            if up == 0: print(f"⚠️  Structure group {name} is not defined!")
        
        @classmethod
        def json(cls) -> dict:
            """Generates the json file for all defined structure groups."""
            json = {"Assign":{}}
            for i in cls.Groups:
                json["Assign"][i.ID] = {
                    "NAME": i.NAME,
                    "P_TYPE": 0,
                    "N_LIST": i.NLIST,
                    "E_LIST": i.ELIST
                }
            return json
        
        @classmethod
        def create(cls):
            MidasAPI("PUT",cls.url,cls.json())
            
        @classmethod
        def get(cls) -> dict:
            return MidasAPI("GET",cls.url)
        

        @classmethod
        def sync(cls):
            a = cls.get()
            if a != {'message': ''}:
                if list(a['GRUP'].keys()) != []:
                    cls.Groups = []
                    cls.ids=[]
                    for j in a['GRUP'].keys():
                        nlist=[]
                        elist=[]
                        try: nlist = a['GRUP'][j]["N_LIST"]
                        except: pass
                        try: elist = a['GRUP'][j]["E_LIST"]
                        except: pass

                        Group.Structure(a['GRUP'][j]["NAME"],nlist,elist)

        @classmethod
        def delete(cls):
            cls.Groups=[]
            cls.ids=[]
            MidasAPI("DELETE",cls.url)
        


#---------------------------------         BOUNDARY       ---------------------------------------

    class Boundary:

        Groups = []
        ids=[]
        url= "/db/BNGR"

        def __init__(self, name:str):
            """"""
            self.NAME = name
            if Group.Boundary.Groups == []: self.ID=1
            else: self.ID= max(Group.Boundary.ids)+1
            Group.Boundary.ids.append(self.ID)
            Group.Boundary.Groups.append(self)
        
        @classmethod
        def json(cls) -> dict:
            "Generates the json file for all defined structure groups."
            json = {"Assign":{}}
            for i in cls.Groups:
                json["Assign"][i.ID] = {
                    "NAME": i.NAME,
                    "AUTOTYPE": 0,
                }
            return json
        
        @classmethod
        def create(cls):
            MidasAPI("PUT",cls.url,cls.json())
            
        @classmethod
        def get(cls) -> dict:
            return MidasAPI("GET",cls.url)
        

        @classmethod
        def sync(cls):
            a = cls.get()
            if a != {'message': ''}:
                if list(a['BNGR'].keys()) != []:
                    cls.Groups = []
                    cls.ids=[]
                    for j in a['BNGR'].keys():
                        Group.Boundary(a['BNGR'][j]["NAME"])

        @classmethod
        def delete(cls):
            cls.Groups=[]
            cls.ids=[]
            MidasAPI("DELETE",cls.url)


# --------------------------------    LOAD   -------------------------------

    class Load:

        Groups = []
        ids=[]
        url= "/db/LDGR"

        def __init__(self, name:str):
            """"""
            self.NAME = name
            if Group.Load.Groups == []: self.ID=1
            else: self.ID= max(Group.Load.ids)+1
            Group.Load.ids.append(self.ID)
            Group.Load.Groups.append(self)
    
        
        @classmethod
        def json(cls) -> dict:
            "Generates the json file for all defined structure groups."
            json = {"Assign":{}}
            for i in cls.Groups:
                json["Assign"][i.ID] = {
                    "NAME": i.NAME
                }
            return json
        
        @classmethod
        def create(cls):
            MidasAPI("PUT",cls.url,cls.json())
            
        @classmethod
        def get(cls) -> dict:
            return MidasAPI("GET",cls.url)
        
        @classmethod
        def sync(cls):
            a = cls.get()
            if a != {'message': ''}:
                if list(a['LDGR'].keys()) != []:
                    cls.Groups = []
                    cls.ids=[]
                    for j in a['LDGR'].keys():
                        Group.Load(a['LDGR'][j]["NAME"])

        @classmethod
        def delete(cls):
            cls.Groups=[]
            cls.ids=[]
            MidasAPI("DELETE",cls.url)

# ------------------------  TENDON  ----------

    class Tendon:

        Groups = []
        ids=[]
        url= "/db/TDGR"

        def __init__(self, name:str):
            """"""
            self.NAME = name
            if Group.Tendon.Groups == []: self.ID=1
            else: self.ID= max(Group.Tendon.ids)+1
            Group.Tendon.ids.append(self.ID)
            Group.Tendon.Groups.append(self)

        
        @classmethod
        def json(cls) -> dict:
            "Generates the json file for all defined structure groups."
            json = {"Assign":{}}
            for i in cls.Groups:
                json["Assign"][i.ID] = {
                    "NAME": i.NAME
                }
            return json
        
        @classmethod
        def create(cls):
            MidasAPI("PUT",cls.url,cls.json())
            
        @classmethod
        def get(cls) -> dict:
            return MidasAPI("GET",cls.url)
        
        @classmethod
        def sync(cls):
            a = cls.get()
            if a != {'message': ''}:
                if list(a['TDGR'].keys()) != []:
                    cls.Groups = []
                    cls.ids=[]
                    for j in a['TDGR'].keys():
                        Group.Tendon(a['TDGR'][j]["NAME"])

        @classmethod
        def delete(cls):
            cls.Groups=[]
            cls.ids=[]
            MidasAPI("DELETE",cls.url)
