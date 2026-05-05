from ._mapi import MidasAPI
from ._group import Group
from ._element import elemByID
import numpy as np
from typing import Literal

_presDir = Literal['LX','LY','LZ','GX','GY','GZ','VECTOR']
_beamLoadDir = Literal['LX','LY','LZ','GX','GY','GZ']
_beamLoadType = Literal['CONLOAD','CONMOMENT','UNILOAD','UNIMOMENT']
_lineDistType = Literal['Abs','Rel']
_swDir= Literal['X','Y','Z','VECTOR']
_LCType = Literal["USER", "D", "DC", "DW", "DD", "EP", "EANN", "EANC", "EAMN", "EAMC", "EPNN", "EPNC", "EPMN", "EPMC", "EH", "EV", "ES", "EL", "LS", "LSC", 
            "L", "LC", "LP", "IL", "ILP", "CF", "BRK", "BK", "CRL", "PS", "B", "WP", "FP", "SF", "WPR", "W", "WL", "STL", "CR", "SH", "T", "TPG", "CO",
            "CT", "CV", "E", "FR", "IP", "CS", "ER", "RS", "GE", "LR", "S", "R", "LF", "RF", "GD", "SHV", "DRL", "WA", "WT", "EVT", "EEP", "EX", "I", "EE"]
# -----  Extend for list of nodes/elems -----

def _ADD_NodalLoad(self):
    if isinstance(self.NODE,int):
        Load.Nodal.data.append(self)
    elif isinstance(self.NODE,(list,tuple,set)):
        for nID in self.NODE:
            Load.Nodal(nID,self.LCN,self.LDGR,self.FX,self.FY,self.FZ,self.MX,self.MY,self.MZ,self.ID)

def _ADD_PressureLoad(self):
    if isinstance(self.ELEM,int):
        Load.Pressure.data.append(self)
    elif isinstance(self.ELEM,(list,tuple,set)):
        for eID in self.ELEM:
            Load.Pressure(eID,self.LCN,self.LDGR,self.DIR,self.PRES,self.VECTOR,self.bPROJ,self.ID)


def _ADD_BeamLoad(self):
    if isinstance(self.ELEMENT,int):
        Load.Beam.data.append(self)
    elif isinstance(self.ELEMENT,(list,tuple,set)):
        for eID in self.ELEMENT:
            Load.Beam(eID,self.LCN,self.LDGR,self.VALUE,self.DIRECTION,self.D,self.P,self.CMD,self.TYPE,self.USE_ECCEN,self.USE_PROJECTION,
                      self.ECCEN_DIR,self.ECCEN_TYPE,self.IECC,self.JECC,self.USE_H,self.I_H,self.J_H,self.ID)

def _ADD_LoadCase(self):
    Load_Case.maxID = max(max(self.ID),Load_Case.maxID)
    Load_Case.maxNO = max(max(self.NO),Load_Case.maxNO)
    for i in range(len(self.ID)):
        Load_Case.cases.append(_LoadCase(self.TYPE,self.NAME[i],self.ID[i],self.NO[i]))
        
def _ADD_NodalMass(self):
    if isinstance(self.NODE_ID,int):
        Load.NodalMass.data.append(self)
    elif isinstance(self.NODE_ID,(list,tuple,set,)):
        for nID in self.NODE_ID:
            Load.NodalMass(nID,self.MX,self.MY,self.MZ,self.RMX,self.RMY,self.RMZ)

def _ADD_SpDisp(self):
    if isinstance(self.NODE,int):
        Load.SpDisp.data.append(self)
    elif isinstance(self.NODE,(list,tuple,set,)):
        for nID in self.NODE:
            Load.SpDisp(nID,self.LCN,self.LDGR,self.VALUES,self.ID)

# class _hLC:
#     ID, NAME, TYPE , NO= 0,0,0,0

class _LoadCase:
    def __init__(self, type, name , id , no):
        self.TYPE = type
        self.NAME = name
        self.ID = id
        self.NO = no
        self.DESC = ""

#11 Class to define Load Cases:
class Load_Case:
    """Type symbol (Refer Static Load Case section in the Onine API Manual, Load Case names.  
    \nSample: Load_Case("USER", "Case 1", "Case 2", ..., "Case n")"""
    maxID = 0
    maxNO = 0
    cases:list[_LoadCase] = []
    types = ["USER", "D", "DC", "DW", "DD", "EP", "EANN", "EANC", "EAMN", "EAMC", "EPNN", "EPNC", "EPMN", "EPMC", "EH", "EV", "ES", "EL", "LS", "LSC", 
            "L", "LC", "LP", "IL", "ILP", "CF", "BRK", "BK", "CRL", "PS", "B", "WP", "FP", "SF", "WPR", "W", "WL", "STL", "CR", "SH", "T", "TPG", "CO",
            "CT", "CV", "E", "FR", "IP", "CS", "ER", "RS", "GE", "LR", "S", "R", "LF", "RF", "GD", "SHV", "DRL", "WA", "WT", "EVT", "EEP", "EX", "I", "EE"]
    def __init__(self, type:_LCType, *name):
        self.TYPE = type
        self.NAME = name
        self.ID = []
        self.NO = []
        for i in range(len(self.NAME)):
            if Load_Case.cases == []: 
                self.ID.append(i+1)
                self.NO.append(i+1)
            if Load_Case.cases != []: 
                self.ID.append(Load_Case.maxID + i + 1)
                self.NO.append(Load_Case.maxNO + i + 1)
        _ADD_LoadCase(self)
    
    @classmethod
    def json(cls):
        ng = []
        json = {"Assign":{}}
        for i in cls.cases:
            if i.TYPE in cls.types:
                json['Assign'][i.ID] = {
                    "NO": i.NO,
                    "NAME": i.NAME,
                    "TYPE": i.TYPE,
                    "DESC" : i.DESC  
                    }
            else:
                ng.append(i.TYPE)
        if ng != []: print(f"These load case types are incorrect: {ng}.\nPlease check API Manual.")
        return json
    
    @staticmethod
    def create():
        MidasAPI("PUT","/db/stld",Load_Case.json())
        
    @staticmethod
    def get():
        return MidasAPI("GET","/db/stld")
    
    @staticmethod
    def sync():
        Load_Case.clear()
        a = Load_Case.get()
        if a != {'message': ''}:
            if list(a['STLD'].keys()) != []:
                for j in a['STLD'].keys():
                    lc = Load_Case(a['STLD'][j]['TYPE'], a['STLD'][j]['NAME'])
                    lcID = int(j)
                    lCNO = int(a['STLD'][j]['NO'])
                    lc.ID = [lcID]
                    lc.NO = [lCNO]

                    Load_Case.maxID = max(Load_Case.maxID ,lcID )
                    Load_Case.maxNO = max(Load_Case.maxNO ,lCNO )
    
    @classmethod
    def delete(cls):
        cls.clear()
        return MidasAPI("DELETE","/db/stld")
    
    @classmethod
    def clear(cls):
        cls.maxID = 0
        cls.maxNO = 0
        cls.cases=[]
#---------------------------------------------------------------------------------------------------------------



class Load:

    @classmethod
    def create(cls):
        if Load_Case.cases: Load_Case.create()
        if cls.SW.data: cls.SW.create()
        if cls.Nodal.data: cls.Nodal.create()
        if cls.Beam.data: cls.Beam.create()
        if cls.Pressure.data: cls.Pressure.create()
        if cls.FloorLoadDefine.data : cls.FloorLoadDefine.create()
        if cls.FloorLoadAssign.data : cls.FloorLoadAssign.create()
        if cls.Misc.PreCompositeSection.loadCases : cls.Misc.PreCompositeSection.create()
    
    @classmethod
    def clear(cls):
        Load_Case.clear()
        cls.SW.clear()
        cls.Nodal.clear()
        cls.Beam.clear()
        cls.Pressure.clear()
        cls.FloorLoadAssign.clear()
        cls.FloorLoadDefine.clear()
        cls.Misc.PreCompositeSection.clear()
        

    class SW:
        """Load Case Name, direction, Value, Load Group.\n
        Sample: Load_SW("Self-Weight", "Z", -1, "DL")"""
        data = []
        def __init__(self, load_case:str, dir:_swDir = "Z", value = -1, load_group:str = ""):

            chk = 0
            for i in Load_Case.cases:
                if load_case in i.NAME: chk = 1
            if chk == 0: Load_Case("D", load_case)
            
            if load_group != "":
                chk = 0
                a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                if load_group in a: chk = 1
                if chk == 0: Group.Load(load_group)

            if type(value)==int:
                if dir == "X":
                    fv = [value, 0, 0]
                elif dir == "Y":
                    fv = [0, value, 0]
                else:
                    fv = [0, 0, value]
            elif type(value)==list:
                fv = value
                dir = 'VECTOR'
            else: fv = [0,0,-1]


            self.LC = load_case
            self.DIR = dir
            self.FV = fv
            self.LG = load_group
            self.ID = len(Load.SW.data) + 1
            if any(self.FV):
                Load.SW.data.append(self)
        
        @classmethod
        def json(cls):
            json = {"Assign":{}}
            for i in cls.data:
                json["Assign"][i.ID] = {
                    "LCNAME": i.LC,
                    "GROUP_NAME": i.LG,
                    "FV": i.FV
                }
            return json
        
        @staticmethod
        def create():
            MidasAPI("PUT","/db/BODF",Load.SW.json())
        
        @staticmethod
        def get():
            return MidasAPI("GET","/db/BODF")
        
        @classmethod
        def delete(cls):
            cls.clear()
            return MidasAPI("DELETE","/db/BODF")

        @classmethod
        def clear(cls):
            cls.data=[]
        
        @staticmethod
        def sync():
            a = Load.SW.get()
            if a != {'message': ''}:
                for i in list(a['BODF'].keys()):
                    if a['BODF'][i]['FV'][0] != 0 and a['BODF'][i]['FV'][1] == 0 and a['BODF'][i]['FV'][2] == 0:
                        di = "X"
                        va = a['BODF'][i]['FV'][0]
                    elif a['BODF'][i]['FV'][0] == 0 and a['BODF'][i]['FV'][1] != 0 and a['BODF'][i]['FV'][2] == 0:
                        di = "Y"
                        va = a['BODF'][i]['FV'][1]
                    elif a['BODF'][i]['FV'][0] == 0 and a['BODF'][i]['FV'][1] == 0 and a['BODF'][i]['FV'][2] != 0:
                        di = "Z"
                        va = a['BODF'][i]['FV'][2]
                    else:
                        di = 'VECTOR'
                        va = a['BODF'][i]['FV']
                    
                    Load.SW(a['BODF'][i]['LCNAME'], di, va, a['BODF'][i]['GROUP_NAME'])
    
    
    #--------------------------------   NODAL LOADS  ------------------------------------------------------------

    #18 Class to add Nodal Loads:
    class Nodal:
        """Creates node loads and converts to JSON format.
        Example: Load_Node(101, "LC1", "Group1", FZ = 10)
        """
        data = []
        def __init__(self, node, load_case, load_group = "", FX:float = 0, FY:float = 0, FZ:float= 0, MX:float =0, MY:float =0, MZ:float=0, id = None):


            chk = 0
            for i in Load_Case.cases:
                if load_case in i.NAME: chk = 1
            if chk == 0: Load_Case("D", load_case)
            if load_group != "":
                chk = 0
                a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                if load_group in a: chk = 1
                if chk == 0: Group.Load(load_group)


            self.NODE = node
            self.LCN = load_case
            self.LDGR = load_group
            self.FX = FX
            self.FY = FY
            self.FZ = FZ
            self.MX = MX
            self.MY = MY
            self.MZ = MZ

            if id is None:
                self.ID = len(Load.Nodal.data) + 1
            else:
                self.ID = id

            if any([FX,FY,FZ,MX,MY,MZ]):
                _ADD_NodalLoad(self)
            # Load.Nodal.data.append(self)
        
        @classmethod
        def json(cls):
            json = {"Assign": {}}
            for i in cls.data:
                if i.NODE not in list(json["Assign"].keys()):
                    json["Assign"][i.NODE] = {"ITEMS": []}

                json["Assign"][i.NODE]["ITEMS"].append({
                    "ID": i.ID,
                    "LCNAME": i.LCN,
                    "GROUP_NAME": i.LDGR,
                    "FX": i.FX,
                    "FY": i.FY,
                    "FZ": i.FZ,
                    "MX": i.MX,
                    "MY": i.MY,
                    "MZ": i.MZ
                })
            return json
        
        @classmethod
        def create(cls):
            MidasAPI("PUT", "/db/CNLD",cls.json())
        
        @classmethod
        def get(cls):
            return MidasAPI("GET", "/db/CNLD")
        
        @classmethod
        def delete(cls):
            cls.clear()
            return MidasAPI("DELETE", "/db/CNLD")
        
        @classmethod
        def clear(cls):
            cls.data=[]
        
        @classmethod
        def sync(cls):
            cls.data = []
            a = cls.get()
            if a != {'message': ''}:
                for i in a['CNLD'].keys():
                    for j in range(len(a['CNLD'][i]['ITEMS'])):
                        Load.Nodal(int(i),a['CNLD'][i]['ITEMS'][j]['LCNAME'], a['CNLD'][i]['ITEMS'][j]['GROUP_NAME'], 
                            a['CNLD'][i]['ITEMS'][j]['FX'], a['CNLD'][i]['ITEMS'][j]['FY'], a['CNLD'][i]['ITEMS'][j]['FZ'], 
                            a['CNLD'][i]['ITEMS'][j]['MX'], a['CNLD'][i]['ITEMS'][j]['MY'], a['CNLD'][i]['ITEMS'][j]['MZ'],
                            a['CNLD'][i]['ITEMS'][j]['ID'])
    #---------------------------------------------------------------------------------------------------------------

    #19 Class to define Beam Loads:
    class Beam:
        data = []
        def __init__(self, element:list[int], load_case: str, load_group: str = "", value: float=0, direction:_beamLoadDir = "GZ",
             D:list = [0, 1, 0, 0], P = [0, 0, 0, 0], cmd = "BEAM", typ:_beamLoadType = "UNILOAD", use_ecc = False, use_proj = False,
            eccn_dir = "LY", eccn_type = 1, ieccn = 0, jeccn = 0, adnl_h = False, adnl_h_i = 0, adnl_h_j = 0,id = None): 
            """
            element: Element ID or list of Element IDs 
            load_case (str): Load case name
            load_group (str, optional): Load group name. Defaults to ""
            value (float): Load value
            direction (str): Load direction (e.g., "GX", "GY", "GZ", "LX", "LY", "LZ"). Defaults to "GZ"
            D: Relative distance (list with 4 values, optional) based on length of element. Defaults to [0, 1, 0, 0]
            P: Magnitude of UDL at corresponding position of D (list with 4 values, optional). Defaults to [value, value, 0, 0]
            cmd: Load command (e.g., "BEAM", "LINE", "TYPICAL")
            typ: Load type (e.g., "CONLOAD", "CONMOMENT", "UNITLOAD", "UNIMOMENT", "PRESSURE")
            use_ecc: Use eccentricity (True or False). Defaults to False.
            use_proj: Use projection (True or False). Defaults to False.
            eccn_dir: Eccentricity direction (e.g., "GX", "GY", "GZ", "LX", "LY", "LZ"). Defaults to "LZ"
            eccn_type: Eccentricity from offset (1) or centroid (0). Defaults to 1.
            ieccn, jeccn: Eccentricity values at i-end and j-end of the element
            adnl_h: Consider additional H when applying pressure on beam (True or False). Defaults to False.
            adnl_h_i, adnl_h_j: Additional H values at i-end and j-end of the beam.  Defaults to 0.
            id (default=None): Load ID. Defaults to auto-generated\n
            Example:
            - Load_Beam(115, "UDL_Case", "", -50.0, "GZ")  # No eccentricity
            - Load_Beam(115, "UDL_Case", "", -50.0, "GZ", ieccn=2.5)  # With eccentricity
            """

            chk = 0
            for i in Load_Case.cases:
                if load_case in i.NAME: chk = 1
            if chk == 0: Load_Case("D", load_case)
            if load_group != "":
                chk = 0
                a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                if load_group in a: chk = 1
                if chk == 0: Group.Load(load_group)
            D = (D + [0] * 4)[:4]
            P = (P + [0] * 4)[:4]
            if P == [0, 0, 0, 0]: P = [value, value, 0, 0]
            if eccn_type not in (0, 1):
                eccn_type = 1
            if direction not in ("GX", "GY", "GZ", "LX", "LY", "LZ"): direction = "GZ"
            if eccn_dir not in ("GX", "GY", "GZ", "LX", "LY", "LZ"): eccn_dir = "LY"
            if cmd not in ("BEAM", "LINE", "TYPICAL"): cmd = "BEAM"
            if typ not in ("CONLOAD", "CONMOMENT", "UNILOAD", "UNIMOMENT","PRESSURE"): typ = "UNILOAD"
            if use_ecc == False:
                if ieccn != 0 or jeccn != 0: use_ecc = True
            self.ELEMENT = element
            self.LCN = load_case
            self.LDGR = load_group
            self.VALUE = value
            self.DIRECTION = direction
            self.CMD = cmd
            self.TYPE = typ
            self.USE_PROJECTION = use_proj
            self.USE_ECCEN = use_ecc
            self.ECCEN_TYPE = eccn_type
            self.ECCEN_DIR = eccn_dir
            self.IECC = ieccn
            if jeccn == 0:
                self.JECC = 0
                self.USE_JECC = False
            else:
                self.JECC = jeccn
                self.USE_JECC = True
            self.D = D
            self.P = P
            self.USE_H = adnl_h
            self.I_H = adnl_h_i
            if adnl_h == 0:
                self.USE_JH = False
                self.J_H = 0
            else:
                self.USE_JH = True
                self.J_H = adnl_h_j
            
            if id is None:
                self.ID = len(Load.Beam.data) + 1
            else:
                self.ID = id

            if any(self.P):
                _ADD_BeamLoad(self)
            # Load.Beam.data.append(self)
        
        @classmethod
        def json(cls):
            json = {"Assign": {}}
            for i in cls.data:
                item_data = {
                    "ID": i.ID,
                    "LCNAME": i.LCN,
                    "GROUP_NAME": i.LDGR,
                    "CMD": i.CMD,
                    "TYPE": i.TYPE,
                    "DIRECTION": i.DIRECTION,
                    "USE_PROJECTION": i.USE_PROJECTION,
                    "USE_ECCEN": i.USE_ECCEN,
                    "D": i.D,
                    "P": i.P
                }
                if i.USE_ECCEN == True:
                    item_data.update({
                        "ECCEN_TYPE": i.ECCEN_TYPE,
                        "ECCEN_DIR": i.ECCEN_DIR,
                        "I_END": i.IECC,
                        "J_END": i.JECC,
                        "USE_J_END": i.USE_JECC
                    })
                if i.TYPE == "PRESSURE":
                    item_data.update({
                        "USE_ADDITIONAL": i.USE_H,
                        "ADDITIONAL_I_END": i.I_H,
                        "ADDITIONAL_J_END": i.J_H,
                        "USE_ADDITIONAL_J_END": i.J_H
                    })
                if i.ELEMENT not in json["Assign"]:
                    json["Assign"][i.ELEMENT] = {"ITEMS": []}
                json["Assign"][i.ELEMENT]["ITEMS"].append(item_data)
            return json
        
        @classmethod
        def create(cls):
            MidasAPI("PUT", "/db/bmld", cls.json())
        
        @classmethod
        def get(cls):
            return MidasAPI("GET", "/db/bmld")
        
        @classmethod
        def delete(cls):
            cls.clear()
            return MidasAPI("DELETE", "/db/bmld")
        
        @classmethod
        def clear(cls):
            cls.data=[]
        
        @classmethod
        def sync(cls):
            cls.data = []
            a = cls.get()
            if a != {'message': ''}:
                for i in a['BMLD'].keys():
                    for j in range(len(a['BMLD'][i]['ITEMS'])):
                        if a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'] == True and a['BMLD'][i]['ITEMS'][j]['USE_ADDITIONAL'] == True:
                            Load.Beam(int(i),a['BMLD'][i]['ITEMS'][j]['LCNAME'], a['BMLD'][i]['ITEMS'][j]['GROUP_NAME'], a['BMLD'][i]['ITEMS'][j]['P'],
                                a['BMLD'][i]['ITEMS'][j]['DIRECTION'], a['BMLD'][i]['ITEMS'][j]['D'], a['BMLD'][i]['ITEMS'][j]['P'],
                                a['BMLD'][i]['ITEMS'][j]['CMD'], a['BMLD'][i]['ITEMS'][j]['TYPE'], a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'], a['BMLD'][i]['ITEMS'][j]['USE_PROJECTION'],
                                a['BMLD'][i]['ITEMS'][j]['ECCEN_DIR'], a['BMLD'][i]['ITEMS'][j]['ECCEN_TYPE'], a['BMLD'][i]['ITEMS'][j]['I_END'], a['BMLD'][i]['ITEMS'][j]['J_END'],
                                a['BMLD'][i]['ITEMS'][j]['USE_ADDITIONAL'], a['BMLD'][i]['ITEMS'][j]['ADDITIONAL_I_END'], a['BMLD'][i]['ITEMS'][j]['ADDITIONAL_J_END'], a['BMLD'][i]['ITEMS'][j]['ID'])
                        elif a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'] == False and a['BMLD'][i]['ITEMS'][j]['USE_ADDITIONAL'] == True:
                            Load.Beam(int(i),a['BMLD'][i]['ITEMS'][j]['LCNAME'], a['BMLD'][i]['ITEMS'][j]['GROUP_NAME'], a['BMLD'][i]['ITEMS'][j]['P'],
                                a['BMLD'][i]['ITEMS'][j]['DIRECTION'],  a['BMLD'][i]['ITEMS'][j]['D'], a['BMLD'][i]['ITEMS'][j]['P'],
                                a['BMLD'][i]['ITEMS'][j]['CMD'], a['BMLD'][i]['ITEMS'][j]['TYPE'], a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'], a['BMLD'][i]['ITEMS'][j]['USE_PROJECTION'],
                                adnl_h = a['BMLD'][i]['ITEMS'][j]['USE_ADDITIONAL'], adnl_h_i = a['BMLD'][i]['ITEMS'][j]['ADDITIONAL_I_END'], adnl_h_j = a['BMLD'][i]['ITEMS'][j]['ADDITIONAL_J_END'],id= a['BMLD'][i]['ITEMS'][j]['ID'])
                        elif a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'] == True and a['BMLD'][i]['ITEMS'][j]['USE_ADDITIONAL'] == False:
                            Load.Beam(int(i),a['BMLD'][i]['ITEMS'][j]['LCNAME'], a['BMLD'][i]['ITEMS'][j]['GROUP_NAME'], a['BMLD'][i]['ITEMS'][j]['P'],
                                a['BMLD'][i]['ITEMS'][j]['DIRECTION'], a['BMLD'][i]['ITEMS'][j]['D'], a['BMLD'][i]['ITEMS'][j]['P'],
                                a['BMLD'][i]['ITEMS'][j]['CMD'], a['BMLD'][i]['ITEMS'][j]['TYPE'], a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'], a['BMLD'][i]['ITEMS'][j]['USE_PROJECTION'],
                                a['BMLD'][i]['ITEMS'][j]['ECCEN_DIR'], a['BMLD'][i]['ITEMS'][j]['ECCEN_TYPE'], a['BMLD'][i]['ITEMS'][j]['I_END'], a['BMLD'][i]['ITEMS'][j]['J_END'],id=a['BMLD'][i]['ITEMS'][j]['ID'])
                        else:
                            Load.Beam(int(i),a['BMLD'][i]['ITEMS'][j]['LCNAME'], a['BMLD'][i]['ITEMS'][j]['GROUP_NAME'],a['BMLD'][i]['ITEMS'][j]['P'],
                                a['BMLD'][i]['ITEMS'][j]['DIRECTION'], a['BMLD'][i]['ITEMS'][j]['D'], a['BMLD'][i]['ITEMS'][j]['P'],
                                a['BMLD'][i]['ITEMS'][j]['CMD'], a['BMLD'][i]['ITEMS'][j]['TYPE'], a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'], a['BMLD'][i]['ITEMS'][j]['USE_PROJECTION'],id= a['BMLD'][i]['ITEMS'][j]['ID'])
  
  
    #--------------------------------  Load to Mass  ------------------------------------------------------------

    #20 Class to add Load to Mass:
    class LoadToMass:
        """
        Creates load-to-mass conversion entries and converts them to JSON format.

        Example:
            Load.LoadToMass("Z", ["DL", "LL"], [1.0, 0.5])

        Args:
            dir (str): 
                Mass Direction - "X", "Y", "Z", "XY", "YZ", "XZ", "XYZ".
                If invalid, defaults to "XYZ".
            load_case (list | str): 
                List of load case names or a single case name as string.
            load_factor (list | float, optional): 
                List of scale factors corresponding to `load_case`.
                If None or shorter than `load_case`, remaining factors default to 1.0.
            nodal_load (bool, optional): 
                Include nodal loads. Defaults to True.
            beam_load (bool, optional): 
                Include beam loads. Defaults to True.
            floor_load (bool, optional): 
                Include floor loads. Defaults to True.
            pressure (bool, optional): 
                Include pressure loads. Defaults to True.
            gravity (float, optional): 
                Gravity acceleration. Defaults to 9.806.
        """
        data = []
        
        def __init__(self, dir, load_case, load_factor=None, nodal_load=True, beam_load=True, 
                    floor_load=True, pressure=True, gravity=None):
            
            if gravity == None: 
                from ._model import Model
                gravity = Model.gravity()

            valid_directions = ["X", "Y", "Z", "XY", "YZ", "XZ", "XYZ"]
            if dir not in valid_directions:
                dir = "XYZ"
                
            if not isinstance(load_case, list):
                load_case = [load_case]
                
            if load_factor is None:
                load_factor = [1.0] * len(load_case)
            elif not isinstance(load_factor, list):
                load_factor = [load_factor]
                
            while len(load_factor) < len(load_case):
                load_factor.append(1.0)
                
            for case in load_case:
                chk = 0
                for i in Load_Case.cases:
                    if case in i.NAME:
                        chk = 1
                if chk == 0:
                    print(f"Warning: Load case '{case}' does not exist!")
            
            self.DIR = dir
            self.LOAD_CASE = load_case
            self.LOAD_FACTOR = load_factor
            self.NODAL = nodal_load
            self.BEAM = beam_load
            self.FLOOR = floor_load
            self.PRESSURE = pressure
            self.GRAVITY = gravity
            
            if any(self.LOAD_FACTOR):
                Load.LoadToMass.data.append(self)
        
        @classmethod
        def json(cls):
            json_data = {"Assign": {}}
            
            for idx, load_obj in enumerate(cls.data, start=1):
                vlc_array = []
                for i, case_name in enumerate(load_obj.LOAD_CASE):
                    vlc_array.append({
                        "LCNAME": case_name,
                        "FACTOR": load_obj.LOAD_FACTOR[i]
                    })
                
                json_data["Assign"][str(idx)] = {
                    "DIR": load_obj.DIR,
                    "bNODAL": load_obj.NODAL,
                    "bBEAM": load_obj.BEAM, 
                    "bFLOOR": load_obj.FLOOR,
                    "bPRES": load_obj.PRESSURE,
                    "GRAV": load_obj.GRAVITY,
                    "vLC": vlc_array
                }
            
            return json_data
        
        @classmethod
        def create(cls):
            return MidasAPI("PUT", "/db/ltom", cls.json())
        
        @classmethod
        def get(cls):
            return MidasAPI("GET", "/db/ltom")
        
        @classmethod
        def delete(cls):
            cls.data = []
            return MidasAPI("DELETE", "/db/ltom")
        
        @classmethod
        def sync(cls):
            cls.data = []
            response = cls.get()
            
            if response != {'message': ''}:
                for key, item_data in response.get('LTOM', {}).items():
                    load_cases = []
                    load_factors = []
                    
                    for lc_item in item_data.get('vLC', []):
                        load_cases.append(lc_item.get('LCNAME'))
                        load_factors.append(lc_item.get('FACTOR'))
                    
                    Load.LoadToMass(
                        dir=item_data.get('DIR'),
                        load_case=load_cases,
                        load_factor=load_factors,
                        nodal_load=item_data.get('bNODAL'),
                        beam_load=item_data.get('bBEAM'),
                        floor_load=item_data.get('bFLOOR'),
                        pressure=item_data.get('bPRES'),
                        gravity=item_data.get('GRAV')
                    )


    #-----------------------------------------------------------NodalMass-----------------

    class NodalMass:
        """Creates nodal mass and converts to JSON format.
        Example: NodalMass(1, 1.5, 2.0, 3.0, 0.1, 0.2, 0.3)
        """
        data = []

        def __init__(self, node_id:list[int], mX:float=0, mY:float=0, mZ:float=0, rmX:float=0, rmY:float=0, rmZ:float=0):
            """
            node_id (int): Node ID where the mass is applied (Required)
            mX (float): Translational Lumped Mass in GCS X-direction (Required)
            mY (float): Translational Lumped Mass in GCS Y-direction. Defaults to 0
            mZ (float): Translational Lumped Mass in GCS Z-direction. Defaults to 0
            rmX (float): Rotational Mass Moment of Inertia about GCS X-axis. Defaults to 0
            rmY (float): Rotational Mass Moment of Inertia about GCS Y-axis. Defaults to 0
            rmZ (float): Rotational Mass Moment of Inertia about GCS Z-axis. Defaults to 0
            """
            self.NODE_ID = node_id
            self.MX = mX
            self.MY = mY
            self.MZ = mZ
            self.RMX = rmX
            self.RMY = rmY
            self.RMZ = rmZ
            
            if any([mX,mY,mZ,rmX,rmY,rmZ]):
                _ADD_NodalMass(self)
            # Load.NodalMass.data.append(self)
        
        @classmethod
        def json(cls):
            json_data = {"Assign": {}}
            
            for mass_obj in cls.data:
                json_data["Assign"][mass_obj.NODE_ID] = {
                    "mX": mass_obj.MX,
                    "mY": mass_obj.MY,
                    "mZ": mass_obj.MZ,
                    "rmX": mass_obj.RMX,
                    "rmY": mass_obj.RMY,
                    "rmZ": mass_obj.RMZ
                }
            
            return json_data
        
        @classmethod
        def create(cls):
            return MidasAPI("PUT", "/db/nmas", cls.json())
        
        @classmethod
        def get(cls):
            MidasAPI("GET", "/db/nmas")
        
        @classmethod
        def delete(cls):
            cls.data = []
            MidasAPI("DELETE", "/db/nmas")
        
        @classmethod
        def sync(cls):
            cls.data = []
            response = cls.get()
            
            if response and response != {'message': ''}:
                nmas_data = response.get('NMAS', {})
        
                for node_id, item_data in nmas_data.items():
                    Load.NodalMass(
                        node_id=int(node_id),
                        mX=item_data.get('mX'),
                        mY=item_data.get('mY'),
                        mZ=item_data.get('mZ'),
                        rmX=item_data.get('rmX'),
                        rmY=item_data.get('rmY'),
                        rmZ=item_data.get('rmZ')
                    )
    
    class FloorLoadDefine:
        data = []

        def __init__(self, name: str, items: list, desc: str = "", id: int = None):
            """Define Floor Load Type with load case items.
        
            Parameters:
                name (str): Floor Load Type Name.
                items (list): List of floor load items. Each item can be:
                            [load_case, value]  -- Sub Beam Weight defaults to False
                            [load_case, value, sub_beam_weight]
                desc (str, optional): Description. Defaults to "".
                id (int, optional): ID. Auto-assigned if not provided.

            Example:
                Load.FloorLoadDefine("Floor_example", [
                    ["DC", 10, True],
                    ["DW", 20]
                ])
            """

            self.NAME = name
            self.DESC = desc

            # Parse items each entry is [load_case, value] or [load_case, value, sub_beam_weight]
            parsed_items = []
            for entry in items:
                if len(entry) == 2:
                    lc_name, floor_load = entry
                    sub_beam_weight = False
                elif len(entry) == 3:
                    lc_name, floor_load, sub_beam_weight = entry
                else:
                    raise ValueError(
                        f"Each item must have 2 or 3 elements: [load_case, value] or "
                        f"[load_case, value, sub_beam_weight]. Got: {entry}"
                    )
                parsed_items.append({
                    "LCNAME": lc_name,
                    "FLOOR_LOAD": floor_load,
                    "OPT_SUB_BEAM_WEIGHT": sub_beam_weight
                })

            self.ITEMS = parsed_items

            if id is None:
                self.ID = len(Load.FloorLoadDefine.data) + 1
            else:
                self.ID = id

            Load.FloorLoadDefine.data.append(self)

        @classmethod
        def json(cls):
            json = {"Assign": {}}
            for i in cls.data:
                json["Assign"][i.ID] = {
                    "NAME": i.NAME,
                    "DESC": i.DESC,
                    "ITEM": i.ITEMS
                }
            return json

        @classmethod
        def create(cls):
            MidasAPI("PUT", "/db/FBLD", cls.json())

        @classmethod
        def get(cls):
            return MidasAPI("GET", "/db/FBLD")

        @classmethod
        def delete(cls):
            cls.clear()
            return MidasAPI("DELETE", "/db/FBLD")

        @classmethod
        def clear(cls):
            cls.data = []

        @classmethod
        def sync(cls):
            cls.clear()
            a = cls.get()
            if a != {'message': ''}:
                for key in a['FBLD'].keys():
                    entry = a['FBLD'][key]
                    raw_items = entry.get('ITEM', [])

                    # Reconstruct items list in [load_case, value, sub_beam_weight] form
                    items = [
                        [
                            it['LCNAME'],
                            it['FLOOR_LOAD'],
                            it.get('OPT_SUB_BEAM_WEIGHT', False)
                        ]
                        for it in raw_items
                    ]

                    Load.FloorLoadDefine(
                        name=entry['NAME'],
                        items=items,
                        desc=entry.get('DESC', ''),
                        id=int(key)
                    )
    
    class FloorLoadAssign:
        data = []

        def __init__(self, floor_load_name: str, distribution_type: int = 2,
                     direction: str = "GZ", node_list: list = [],
                     group: str = "", load_angle: int = 0,
                     sub_beam_no: int = 0, sub_beam_angle: int = 0,
                     unit_selfweight: int = 0, bProjection: bool = False,
                     exclude_inner_elem_area: bool = False,
                     allow_polygon_type_unit_area: bool = False,
                     id=None):

            """Assign Floor Load to nodes.

            Parameters:
                floor_load_name (str): Floor Load Type Name. Required.
                distribution_type (int): Distribution type. 1=One Way, 2=Two Way,
                                        3=Polygon-Centroid, 4=Polygon-Length. Default: 2.
                direction (str): Load direction. One of "LX","LY","LZ","GX","GY","GZ". Default: "GZ".
                node_list (list): List of node IDs defining the loading area. Required.
                group (str, optional): Load Group Name. Default: "".
                load_angle (int, optional): Load Angle A1. Only used when distribution_type=1. Default: 0.
                sub_beam_no (int, optional): Number of Sub Beams. Only used when distribution_type=1 or 2. Default: 0.
                sub_beam_angle (int, optional): Sub-Beam Angle A2. Only used when distribution_type=1 or 2. Default: 0.
                unit_selfweight (int, optional): Unit Self Weight. Only used when distribution_type=1 or 2. Default: 0.
                opt_projection (bool, optional): Projection Boolean. Default: False.
                exclude_inner_elem_area (bool, optional): Exclude Inner Element of Area.
                                                        Only used when distribution_type=1 or 2. Default: False.
                allow_polygon_type_unit_area (bool, optional): Allow Polygon Type Unit Area.
                                                            Only used when distribution_type=2. Default: False.
                id (int, optional): ID. Auto-assigned if not provided.

            Example:
                Load.FloorLoadAssign("Floor_example", 1, [508, 509, 511, 510])

                Load.FloorLoadAssign("Floor_example", 2, [512, 516, 513, 514, 517, 515],
                                    group="LoadGroup2", sub_beam_no=1, sub_beam_angle=90,
                                    unit_selfweight=-15, opt_projection=False,
                                    exclude_inner_elem_area=True,
                                    allow_polygon_type_unit_area=True)

                Load.FloorLoadAssign("Floor_example", 3, [512, 516, 513],
                                    direction="GZ", group="LoadGroup2", opt_projection=True)
            """

            if distribution_type not in (1, 2, 3, 4):
                distribution_type = 2
            if direction not in ("LX", "LY", "LZ", "GX", "GY", "GZ"):
                direction = "GZ"

            self.FLOOR_LOAD_TYPE_NAME = floor_load_name
            self.FLOOR_DIST_TYPE = distribution_type
            self.DIR = direction
            self.NODES = node_list
            self.GROUP_NAME = group
            self.LOAD_ANGLE = load_angle
            self.SUB_BEAM_NUM = sub_beam_no
            self.SUB_BEAM_ANGLE = sub_beam_angle
            self.UNIT_SELF_WEIGHT = unit_selfweight
            self.OPT_PROJECTION = bProjection
            self.OPT_EXCLUDE_INNER_ELEM_AREA = exclude_inner_elem_area
            self.OPT_ALLOW_POLYGON_TYPE_UNIT_AREA = allow_polygon_type_unit_area

            if id is None:
                self.ID = len(Load.FloorLoadAssign.data) + 1
            else:
                self.ID = id

            Load.FloorLoadAssign.data.append(self)

        @classmethod
        def json(cls):
            json = {"Assign": {}}
            for i in cls.data:
                entry = {
                    "FLOOR_LOAD_TYPE_NAME": i.FLOOR_LOAD_TYPE_NAME,
                    "FLOOR_DIST_TYPE": i.FLOOR_DIST_TYPE,
                    "DIR": i.DIR,
                    "OPT_PROJECTION": i.OPT_PROJECTION,
                    "DESC": "",
                    "GROUP_NAME": i.GROUP_NAME,
                    "NODES": i.NODES
                }

                # Fields only for dist type 1 or 2
                if i.FLOOR_DIST_TYPE in (1, 2):
                    entry["SUB_BEAM_NUM"] = i.SUB_BEAM_NUM
                    entry["SUB_BEAM_ANGLE"] = i.SUB_BEAM_ANGLE
                    entry["UNIT_SELF_WEIGHT"] = i.UNIT_SELF_WEIGHT
                    entry["OPT_EXCLUDE_INNER_ELEM_AREA"] = i.OPT_EXCLUDE_INNER_ELEM_AREA

                # Load angle only for dist type 1
                if i.FLOOR_DIST_TYPE == 1:
                    entry["LOAD_ANGLE"] = i.LOAD_ANGLE

                # Allow polygon type unit area only for dist type 2
                if i.FLOOR_DIST_TYPE == 2:
                    entry["OPT_ALLOW_POLYGON_TYPE_UNIT_AREA"] = i.OPT_ALLOW_POLYGON_TYPE_UNIT_AREA

                json["Assign"][i.ID] = entry
            return json

        @classmethod
        def create(cls):
            MidasAPI("PUT", "/db/fbla", cls.json())

        @classmethod
        def get(cls):
            return MidasAPI("GET", "/db/fbla")

        @classmethod
        def delete(cls):
            cls.clear()
            return MidasAPI("DELETE", "/db/fbla")

        @classmethod
        def clear(cls):
            cls.data = []

        @classmethod
        def sync(cls):
            cls.data = []
            a = cls.get()
            if a != {'message': ''}:
                for i in a['FBLA'].keys():
                    item = a['FBLA'][i]
                    Load.FloorLoadAssign(
                        floor_load_name=item['FLOOR_LOAD_TYPE_NAME'],
                        distribution_type=item['FLOOR_DIST_TYPE'],
                        direction=item.get('DIR', 'GZ'),
                        node_list=item.get('NODES', []),
                        group=item.get('GROUP_NAME', ''),
                        load_angle=item.get('LOAD_ANGLE', 0),
                        sub_beam_no=item.get('SUB_BEAM_NUM', 0),
                        sub_beam_angle=item.get('SUB_BEAM_ANGLE', 0),
                        unit_selfweight=item.get('UNIT_SELF_WEIGHT', 0),
                        opt_projection=item.get('OPT_PROJECTION', False),
                        exclude_inner_elem_area=item.get('OPT_EXCLUDE_INNER_ELEM_AREA', False),
                        allow_polygon_type_unit_area=item.get('OPT_ALLOW_POLYGON_TYPE_UNIT_AREA', False),
                        id=int(i)
                    )
#-----------------------------------------------------------Specified Displacement-------------------------------------------------
    class SpDisp:
        """Creates specified displacement loads and converts to JSON format.
        Example: SpDisp(10, "LL", "Group1", [1.5, 1.5, 1.5, 1.5, 0.5, 0.5])
        """
        data = []
        
        def __init__(self, node:list[int], load_case:str, load_group:str="", values:list[float]=[0, 0, 0, 0, 0, 0], id:int=None):
            """
            node (int): Node ID or list of Node IDs (Required)
            load_case (str): Load case name (Required)
            load_group (str, optional): Load group name. Defaults to ""
            values (list): Displacement values [Dx, Dy, Dz, Rx, Ry, Rz]. Defaults to [0, 0, 0, 0, 0, 0]
            id (default=None): Load ID. Defaults to auto-generated
            """
            
            # Check if load case exists - give warning if not
            chk = 0
            for i in Load_Case.cases:
                if load_case in i.NAME:
                    chk = 1
            if chk == 0:
                print(f"Warning: Load case '{load_case}' does not exist!")
                
            # Check if load group exists and create if specified
            if load_group != "":
                chk = 0
                a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                if load_group in a:
                    chk = 1
                if chk == 0:
                    print(f"Warning: Load group '{load_group}' does not exist!")
            
            # Ensure values is a list of 6 elements [Dx, Dy, Dz, Rx, Ry, Rz]
            if not isinstance(values, list):
                values = [0, 0, 0, 0, 0, 0]
            
            # Pad or truncate to exactly 6 values
            values = (values + [0] * 6)[:6]
            
            self.NODE = node
            self.LCN = load_case
            self.LDGR = load_group
            self.VALUES = values
            
            if id is None:
                self.ID = len(Load.SpDisp.data) + 1
            else:
                self.ID = id

            if any(values):
                _ADD_SpDisp(self)
                # Load.SpDisp.data.append(self)
        
        @classmethod
        def json(cls):
            json_data = {"Assign": {}}
            
            for i in cls.data:
                if i.NODE not in list(json_data["Assign"].keys()):
                    json_data["Assign"][i.NODE] = {"ITEMS": []}
                
                # Create VALUES array with OPT_FLAG logic
                values_array = []
                displacement_labels = ["Dx", "Dy", "Dz", "Rx", "Ry", "Rz"]
                
                for idx, value in enumerate(i.VALUES):
                    values_array.append({
                        "OPT_FLAG": value != 0,  # True if value > 0, False if value = 0
                        "DISPLACEMENT": float(value)
                    })
                
                json_data["Assign"][i.NODE]["ITEMS"].append({
                    "ID": i.ID,
                    "LCNAME": i.LCN,
                    "GROUP_NAME": i.LDGR,
                    "VALUES": values_array
                })
                
            return json_data
        
        @classmethod
        def create(cls):
            return MidasAPI("PUT", "/db/sdsp", cls.json())
        
        @classmethod
        def get(cls):
            return MidasAPI("GET", "/db/sdsp")
        
        @classmethod
        def delete(cls):
            cls.data = []
            return MidasAPI("DELETE", "/db/sdsp")
        
        @classmethod
        def sync(cls):
            cls.data = []
            response = cls.get()
            
            if response != {'message': ''}:
                for node_key in response['SDSP'].keys():
                    for j in range(len(response['SDSP'][node_key]['ITEMS'])):
                        item = response['SDSP'][node_key]['ITEMS'][j]
                        
                        # Extract displacement values from VALUES array
                        values = []
                        for val_item in item.get('VALUES', []):
                            values.append(val_item.get('DISPLACEMENT', 0))
                        
                        Load.SpDisp(
                            int(node_key),
                            item['LCNAME'],
                            item['GROUP_NAME'],
                            values,
                            item['ID']
                        )


    class Line:
        def __init__(self, element_ids:list[int], load_case: str, load_group: str = "", D = [0, 1], P = [0, 0], direction:_beamLoadDir = "GZ",
            type:_beamLoadType = "UNILOAD", distType:_lineDistType='Abs',use_ecc = False, use_proj = False,
            eccn_dir:_beamLoadDir = "LY", eccn_type = 1, ieccn = 0, jeccn = 0, adnl_h = False, adnl_h_i = 0, adnl_h_j = 0,id = None) :

            elem_IDS = []
            elem_LEN = []

            for eID in element_ids:
                try: 
                    elm_len = elemByID(eID).LENGTH
                    elem_IDS.append(eID)
                    elem_LEN.append(elm_len)
                    # print(f"ID = {eID} LEN = {elm_len}")
                except: pass
            cum_LEN = np.insert(np.cumsum(elem_LEN),0,0)
            tot_LEN = cum_LEN[-1]

            if distType == 'Rel':
                D = np.array(D)*tot_LEN

            if type == 'CONLOAD':
                for i in range(len(D)):
                    for q in range(len(cum_LEN)):
                        if D[i] >= 0:
                            if D[i] < cum_LEN[q] :
                                # print(f'LOADING ELEMENT at {D[i]}m = {elem_IDS[q-1]}')
                                rel_loc = (D[i] - cum_LEN[q-1]) / elem_LEN[q-1]
                                # print(f"Relative location = {rel_loc}")
                                Load.Beam(element=elem_IDS[q-1],load_case=load_case,load_group=load_group,D=[rel_loc],P=[P[i]],direction=direction,
                                        typ = "CONLOAD", use_ecc = use_ecc, use_proj = use_proj,
                                        eccn_dir = eccn_dir, eccn_type = eccn_type, ieccn = ieccn, jeccn = jeccn, adnl_h = adnl_h, adnl_h_i = adnl_h_i, adnl_h_j = adnl_h_j,id=id)
                                break
                if D[-1] == tot_LEN:
                    Load.Beam(element=elem_IDS[-1],load_case=load_case,load_group=load_group,D=[1,0,0,0],P=[P[-1]],direction=direction,
                                        typ = "CONLOAD", use_ecc = use_ecc, use_proj = use_proj,
                                        eccn_dir = eccn_dir, eccn_type = eccn_type, ieccn = ieccn, jeccn = jeccn, adnl_h = adnl_h, adnl_h_i = adnl_h_i, adnl_h_j = adnl_h_j,id=id) 
            
            if type == 'UNILOAD':
                n_req = len(D)-1
                D_orig = D
                P_orig = P
                for k in range(n_req):      
                    D = D_orig[0+k:2+k]
                    P = P_orig[0+k:2+k]
                    elms_indx = []
                    for i in range(2):
                        for q in range(len(cum_LEN)):
                            if D[i] < cum_LEN[q] :
                                # print(f'LOADING ELEMENT at {D[i]}m = {elem_IDS[q-1]}')
                                elms_indx.append(q-1)
                                # rel_loc = (D[i] - cum_LEN[q-1]) / elem_LEN[q-1]
                                break 
                    if len(elms_indx)==1: elms_indx.append(len(cum_LEN)-2)
                    if elms_indx != []:
                        for i in range(elms_indx[0],elms_indx[1]+1):
                            rel1 = float((max(D[0],cum_LEN[i]) - cum_LEN[i]) / elem_LEN[i])
                            rel2 = float((min(D[1],cum_LEN[i+1]) - cum_LEN[i]) / elem_LEN[i])

                            p1 = float(P[0]+(max(D[0],cum_LEN[i])-D[0])*(P[1]-P[0])/(D[1]-D[0]))
                            p2 = float(P[0]+(min(D[1],cum_LEN[i+1])-D[0])*(P[1]-P[0])/(D[1]-D[0]))
                            if rel2-rel1 == 0: continue
                            

                            # print(f"Loading ELEM -> {elem_IDS[i]} , D1 = {rel1} , P1 = {p1} | D2 = {rel2} , P2 = {p2}")
                            # Load.Beam(elem_IDS[i],load_case,load_group,D=[rel1,rel2],P=[p1,p2],typ=typ,direction=direction)
                            Load.Beam(element=elem_IDS[i],load_case=load_case,load_group=load_group,D=[rel1,rel2],P=[p1,p2],direction=direction,
                                            typ = "UNILOAD", use_ecc = use_ecc, use_proj = use_proj,
                                            eccn_dir = eccn_dir, eccn_type = eccn_type, ieccn = ieccn, jeccn = jeccn, adnl_h = adnl_h, adnl_h_i = adnl_h_i, adnl_h_j = adnl_h_j,id = id)
                      
    class Pressure:
        """ Assign Pressure load to plates faces.
        
        """
        data = []
        def __init__(self, element:list[int], load_case:str, load_group:str = "", D:_presDir='LZ', P:list=0, VectorDir:list = [1,0,0],bProjection:bool = False,id:int = None):


            chk = 0
            for i in Load_Case.cases:
                if load_case in i.NAME: chk = 1
            if chk == 0: Load_Case("D", load_case)
            if load_group != "":
                chk = 0
                a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                if load_group in a: chk = 1
                if chk == 0: Group.Load(load_group)


            self.ELEM = element
            self.LCN = load_case
            self.LDGR = load_group
            self.DIR = D
            self.VECTOR = VectorDir
            self.PRES = P

            if D in ['GX','GY','GZ']: self.bPROJ = bProjection
            else: self.bPROJ = False

            if id is None:
                self.ID = len(Load.Pressure.data) + 1
            else:
                self.ID = id

            if any(self.PRES):
                _ADD_PressureLoad(self)

        
        @classmethod
        def json(cls):
            json = {"Assign": {}}
            for i in cls.data:
                if i.ELEM not in list(json["Assign"].keys()):
                    json["Assign"][i.ELEM] = {"ITEMS": []}

                js = {
                    "ID": i.ID,
                    "LCNAME": i.LCN,
                    "GROUP_NAME": i.LDGR,
                    "CMD": "PRES",
                    "ELEM_TYPE": "PLATE",
                    "FACE_EDGE_TYPE": "FACE",
                    "DIRECTION": i.DIR,
                    "VECTORS" : i.VECTOR,
                    "FORCES": i.PRES
                }
                if isinstance(i.PRES,(float,int)): newP = [i.PRES,0,0,0,0]
                elif isinstance(i.PRES,list):
                    trimP = i.PRES[:4]
                    newP = [0] + trimP
                js["FORCES"] = newP
                if i.bPROJ:
                    js["OPT_PROJECTION"] = True

                json["Assign"][i.ELEM]["ITEMS"].append(js)

            return json
        
        @classmethod
        def create(cls):
            MidasAPI("PUT", "/db/PRES",cls.json())
        
        @classmethod
        def get(cls):
            return MidasAPI("GET", "/db/PRES")
        
        @classmethod
        def delete(cls):
            cls.clear()
            return MidasAPI("DELETE", "/db/PRES")
        
        @classmethod
        def clear(cls):
            cls.data=[]
        
        @classmethod
        def sync(cls):
            cls.data = []
            a = cls.get()
            if a != {'message': ''}:
                for i in a['PRES'].keys():
                    for j in range(len(a['PRES'][i]['ITEMS'])):
                        if a['PRES'][i]['ITEMS'][j]['ELEM_TYPE'] == 'PLATE' and a['PRES'][i]['ITEMS'][j]['FACE_EDGE_TYPE'] == 'FACE':

                            _defProjOpt = False
                            _defVector = [0,0,1]
                            _defLoad = 0

                            if a['PRES'][i]['ITEMS'][j]['FORCES'][0] == 0 : _defLoad = a['PRES'][i]['ITEMS'][j]['FORCES'][1:]
                            else: _defLoad = a['PRES'][i]['ITEMS'][j]['FORCES'][0]

                            
                            if 'OPT_PROJECTION' in a['PRES'][i]['ITEMS'][j]: _defProjOpt = a['PRES'][i]['ITEMS'][j]['OPT_PROJECTION']
                            if 'VECTORS' in a['PRES'][i]['ITEMS'][j]: _defVector = a['PRES'][i]['ITEMS'][j]['VECTORS']

                            Load.Pressure(
                                int(i),a['PRES'][i]['ITEMS'][j]['LCNAME'], a['PRES'][i]['ITEMS'][j]['GROUP_NAME'],
                                a['PRES'][i]['ITEMS'][j]['DIRECTION'],_defLoad,
                                _defVector,_defProjOpt,
                                a['PRES'][i]['ITEMS'][j]['ID'],
                                )
                            

    class Misc:

        class PreCompositeSection:

            loadCases = set()

            def __init__(self,*loadCase:str):
                ''' Enter Load Cases to be added in Pre-Composite Section.

                Example::

                    Load.Misc.PreCompositeSection('Self Weight','SIDL','Load Case')
                '''
                for lCase in loadCase:
                    Load.Misc.PreCompositeSection.loadCases.add(lCase)

            
            @classmethod
            def json(cls):
                jsDat = {
                        "Assign": {
                            "1": {
                                "LCNAME_ITEM": []
                            }
                        }
                    }
                jsDat['Assign']['1']['LCNAME_ITEM'] = list(cls.loadCases)
                
                return jsDat
            
            @classmethod
            def create(cls):
                MidasAPI("PUT","/db/PLCB",cls.json())

            @classmethod
            def get(cls):
                return MidasAPI("GET", "/db/PLCB")
            
            @classmethod
            def delete(cls):
                cls.clear()
                return MidasAPI("DELETE", "/db/PLCB")
            
            @classmethod
            def clear(cls):
                cls.loadCases=set()

            @classmethod
            def sync(cls):
                cls.loadCases = set()
                a = cls.get()
                if a != {'message': ''}:
                    cls.loadCases = set(a['PLCB']["1"]["LCNAME_ITEM"])

