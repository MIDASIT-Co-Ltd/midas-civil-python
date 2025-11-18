from ._mapi import *
from ._model import *
from ._group import *
import numpy as np


# -----  Extend for list of nodes/elems -----

def _ADD_NodalLoad(self):
    if isinstance(self.NODE,int):
        Load.Nodal.data.append(self)
    elif isinstance(self.NODE,list):
        for nID in self.NODE:
            Load.Nodal(nID,self.LCN,self.LDGR,self.FX,self.FY,self.FZ,self.MX,self.MY,self.MZ,self.ID)


def _ADD_BeamLoad(self):
    if isinstance(self.ELEMENT,int):
        Load.Beam.data.append(self)
    elif isinstance(self.ELEMENT,list):
        for eID in self.ELEMENT:
            Load.Beam(eID,self.LCN,self.LDGR,self.VALUE,self.DIRECTION,self.ID,self.D,self.P,self.CMD,self.TYPE,self.USE_ECCEN,self.USE_PROJECTION,
                      self.ECCEN_DIR,self.ECCEN_TYPE,self.IECC,self.JECC,self.USE_H,self.I_H,self.J_H)



#11 Class to define Load Cases:
class Load_Case:
    """Type symbol (Refer Static Load Case section in the Onine API Manual, Load Case names.  
    \nSample: Load_Case("USER", "Case 1", "Case 2", ..., "Case n")"""
    maxID = 0
    maxNO = 0
    cases = []
    types = ["USER", "D", "DC", "DW", "DD", "EP", "EANN", "EANC", "EAMN", "EAMC", "EPNN", "EPNC", "EPMN", "EPMC", "EH", "EV", "ES", "EL", "LS", "LSC", 
            "L", "LC", "LP", "IL", "ILP", "CF", "BRK", "BK", "CRL", "PS", "B", "WP", "FP", "SF", "WPR", "W", "WL", "STL", "CR", "SH", "T", "TPG", "CO",
            "CT", "CV", "E", "FR", "IP", "CS", "ER", "RS", "GE", "LR", "S", "R", "LF", "RF", "GD", "SHV", "DRL", "WA", "WT", "EVT", "EEP", "EX", "I", "EE"]
    def __init__(self, type, *name):
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
        Load_Case.cases.append(self)
        Load_Case.maxID = max(max(self.ID),Load_Case.maxID)
        Load_Case.maxNO = max(max(self.NO),Load_Case.maxNO)
    
    @classmethod
    def json(cls):
        ng = []
        json = {"Assign":{}}
        for i in cls.cases:
            if i.TYPE in cls.types:
                for j in i.ID:
                    json['Assign'][j] = {
                        "NO": i.NO[i.ID.index(j)],
                        "NAME": i.NAME[i.ID.index(j)],
                        "TYPE": i.TYPE}
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
        Load_Case.maxID = 0
        Load_Case.maxNO = 0
        a = Load_Case.get()
        if a != {'message': ''}:
            if list(a['STLD'].keys()) != []:
                Load_Case.cases = []
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
        cls.cases=[]
        return MidasAPI("DELETE","/db/stld")
#---------------------------------------------------------------------------------------------------------------



class Load:

    @classmethod
    def create(cls):
        if Load_Case.cases!=[]: Load_Case.create()
        if cls.SW.data!=[]: cls.SW.create()
        if cls.Nodal.data!=[]: cls.Nodal.create()
        if cls.Beam.data!=[]: cls.Beam.create()
        

    class SW:
        """Load Case Name, direction, Value, Load Group.\n
        Sample: Load_SW("Self-Weight", "Z", -1, "DL")"""
        data = []
        def __init__(self, load_case, dir = "Z", value = -1, load_group = ""):

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
            else: fv = [0,0,-1]


            self.LC = load_case
            self.DIR = dir
            self.FV = fv
            self.LG = load_group
            self.ID = len(Load.SW.data) + 1
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
            cls.data=[]
            return MidasAPI("DELETE","/db/BODF")
        
        @staticmethod
        def sync():
            a = Load.SW.get()
            if a != {'message': ''}:
                for i in list(a['BODF'].keys()):
                    if a['BODF'][i]['FV'][0] != 0:
                        di = "X"
                        va = a['BODF'][i]['FV'][0]
                    elif a['BODF'][i]['FV'][1] != 0:
                        di = "Y"
                        va = a['BODF'][i]['FV'][1]
                    else:
                        di = "Z"
                        va = a['BODF'][i]['FV'][2]
                    Load.SW(a['BODF'][i]['LCNAME'], di, va, a['BODF'][i]['GROUP_NAME'])
    
    
    #--------------------------------   NODAL LOADS  ------------------------------------------------------------

    #18 Class to add Nodal Loads:
    class Nodal:
        """Creates node loads and converts to JSON format.
        Example: Load_Node(101, "LC1", "Group1", FZ = 10)
        """
        data = []
        def __init__(self, node, load_case, load_group = "", FX:float = 0, FY:float = 0, FZ:float= 0, MX:float =0, MY:float =0, MZ:float=0, id = ""):


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
            if id == "": id = len(Load.Nodal.data) + 1
            self.ID = id

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
            cls.data=[]
            return MidasAPI("DELETE", "/db/CNLD")
        
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
        def __init__(self, element, load_case: str, load_group: str = "", value: float=0, direction: str = "GZ",
            id = "", D = [0, 1, 0, 0], P = [0, 0, 0, 0], cmd = "BEAM", typ = "UNILOAD", use_ecc = False, use_proj = False,
            eccn_dir = "LY", eccn_type = 1, ieccn = 0, jeccn = 0, adnl_h = False, adnl_h_i = 0, adnl_h_j = 0): 
            """
            element: Element Number 
            load_case (str): Load case name
            load_group (str, optional): Load group name. Defaults to ""
            value (float): Load value
            direction (str): Load direction (e.g., "GX", "GY", "GZ", "LX", "LY", "LZ"). Defaults to "GZ"
            id (str, optional): Load ID. Defaults to auto-generated
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
            adnl_h_i, adnl_h_j: Additional H values at i-end and j-end of the beam.  Defaults to 0.\n
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
            
            if id == "":
                id = len(Load.Beam.data) + 1
            self.ID = id
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
            cls.data=[]
            return MidasAPI("DELETE", "/db/bmld")
        
        @classmethod
        def sync(cls):
            cls.data = []
            a = cls.get()
            if a != {'message': ''}:
                for i in a['BMLD'].keys():
                    for j in range(len(a['BMLD'][i]['ITEMS'])):
                        if a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'] == True and a['BMLD'][i]['ITEMS'][j]['USE_ADDITIONAL'] == True:
                            Load.Beam(i,a['BMLD'][i]['ITEMS'][j]['LCNAME'], a['BMLD'][i]['ITEMS'][j]['GROUP_NAME'], a['BMLD'][i]['ITEMS'][j]['P'][0],
                                a['BMLD'][i]['ITEMS'][j]['DIRECTION'], a['BMLD'][i]['ITEMS'][j]['ID'], a['BMLD'][i]['ITEMS'][j]['D'], a['BMLD'][i]['ITEMS'][j]['P'],
                                a['BMLD'][i]['ITEMS'][j]['CMD'], a['BMLD'][i]['ITEMS'][j]['TYPE'], a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'], a['BMLD'][i]['ITEMS'][j]['USE_PROJECTION'],
                                a['BMLD'][i]['ITEMS'][j]['ECCEN_DIR'], a['BMLD'][i]['ITEMS'][j]['ECCEN_TYPE'], a['BMLD'][i]['ITEMS'][j]['I_END'], a['BMLD'][i]['ITEMS'][j]['J_END'],
                                a['BMLD'][i]['ITEMS'][j]['USE_ADDITIONAL'], a['BMLD'][i]['ITEMS'][j]['ADDITIONAL_I_END'], a['BMLD'][i]['ITEMS'][j]['ADDITIONAL_J_END'])
                        elif a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'] == False and a['BMLD'][i]['ITEMS'][j]['USE_ADDITIONAL'] == True:
                            Load.Beam(i,a['BMLD'][i]['ITEMS'][j]['LCNAME'], a['BMLD'][i]['ITEMS'][j]['GROUP_NAME'], a['BMLD'][i]['ITEMS'][j]['P'][0],
                                a['BMLD'][i]['ITEMS'][j]['DIRECTION'], a['BMLD'][i]['ITEMS'][j]['ID'], a['BMLD'][i]['ITEMS'][j]['D'], a['BMLD'][i]['ITEMS'][j]['P'],
                                a['BMLD'][i]['ITEMS'][j]['CMD'], a['BMLD'][i]['ITEMS'][j]['TYPE'], a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'], a['BMLD'][i]['ITEMS'][j]['USE_PROJECTION'],
                                adnl_h = a['BMLD'][i]['ITEMS'][j]['USE_ADDITIONAL'], adnl_h_i = a['BMLD'][i]['ITEMS'][j]['ADDITIONAL_I_END'], adnl_h_j = a['BMLD'][i]['ITEMS'][j]['ADDITIONAL_J_END'])
                        elif a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'] == True and a['BMLD'][i]['ITEMS'][j]['USE_ADDITIONAL'] == False:
                            Load.Beam(i,a['BMLD'][i]['ITEMS'][j]['LCNAME'], a['BMLD'][i]['ITEMS'][j]['GROUP_NAME'], a['BMLD'][i]['ITEMS'][j]['P'][0],
                                a['BMLD'][i]['ITEMS'][j]['DIRECTION'], a['BMLD'][i]['ITEMS'][j]['ID'], a['BMLD'][i]['ITEMS'][j]['D'], a['BMLD'][i]['ITEMS'][j]['P'],
                                a['BMLD'][i]['ITEMS'][j]['CMD'], a['BMLD'][i]['ITEMS'][j]['TYPE'], a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'], a['BMLD'][i]['ITEMS'][j]['USE_PROJECTION'],
                                a['BMLD'][i]['ITEMS'][j]['ECCEN_DIR'], a['BMLD'][i]['ITEMS'][j]['ECCEN_TYPE'], a['BMLD'][i]['ITEMS'][j]['I_END'], a['BMLD'][i]['ITEMS'][j]['J_END'])
                        else:
                            Load.Beam(i,a['BMLD'][i]['ITEMS'][j]['LCNAME'], a['BMLD'][i]['ITEMS'][j]['GROUP_NAME'],a['BMLD'][i]['ITEMS'][j]['P'][0],
                                a['BMLD'][i]['ITEMS'][j]['DIRECTION'], a['BMLD'][i]['ITEMS'][j]['ID'], a['BMLD'][i]['ITEMS'][j]['D'], a['BMLD'][i]['ITEMS'][j]['P'],
                                a['BMLD'][i]['ITEMS'][j]['CMD'], a['BMLD'][i]['ITEMS'][j]['TYPE'], a['BMLD'][i]['ITEMS'][j]['USE_ECCEN'], a['BMLD'][i]['ITEMS'][j]['USE_PROJECTION'])
  
  
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
                    floor_load=True, pressure=True, gravity=9.806):

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
    #21NodalMass

    class NodalMass:
        """Creates nodal mass and converts to JSON format.
        Example: NodalMass(1, 1.5, 2.0, 3.0, 0.1, 0.2, 0.3)
        """
        data = []

        def __init__(self, node_id, mX, mY=0, mZ=0, rmX=0, rmY=0, rmZ=0):
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
            
            Load.NodalMass.data.append(self)
        
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

#-----------------------------------------------------------Specified Displacement-------------------------------------------------
    class SpDisp:
        """Creates specified displacement loads and converts to JSON format.
        Example: SpDisp(10, "LL", "Group1", [1.5, 1.5, 1.5, 1.5, 0.5, 0.5])
        """
        data = []
        
        def __init__(self, node, load_case, load_group="", values=[0, 0, 0, 0, 0, 0], id=""):
            """
            node (int): Node number (Required)
            load_case (str): Load case name (Required)
            load_group (str, optional): Load group name. Defaults to ""
            values (list): Displacement values [Dx, Dy, Dz, Rx, Ry, Rz]. Defaults to [0, 0, 0, 0, 0, 0]
            id (str, optional): Load ID. Defaults to auto-generated
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
            
            if id == "":
                id = len(Load.SpDisp.data) + 1
            self.ID = id
            
            Load.SpDisp.data.append(self)
        
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
        def __init__(self, element_ids, load_case: str, load_group: str = "", D = [0, 1, 0, 0], P = [0, 0, 0, 0], direction: str = "GZ",
            id = "", typ = "CONLOAD", use_ecc = False, use_proj = False,
            eccn_dir = "LY", eccn_type = 1, ieccn = 0, jeccn = 0, adnl_h = False, adnl_h_i = 0, adnl_h_j = 0) :

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


            if typ == 'CONLOAD':
                for i in range(len(D)):
                    for q in range(len(cum_LEN)):
                        if D[i] >= 0:
                            if D[i] < cum_LEN[q] :
                                # print(f'LOADING ELEMENT at {D[i]}m = {elem_IDS[q-1]}')
                                rel_loc = (D[i] - cum_LEN[q-1]) / elem_LEN[q-1]
                                # print(f"Relative location = {rel_loc}")
                                Load.Beam(element=elem_IDS[q-1],load_case=load_case,load_group=load_group,D=[rel_loc],P=[P[i]],direction=direction,
                                        id = id, typ = "CONLOAD", use_ecc = use_ecc, use_proj = use_proj,
                                        eccn_dir = eccn_dir, eccn_type = eccn_type, ieccn = ieccn, jeccn = jeccn, adnl_h = adnl_h, adnl_h_i = adnl_h_i, adnl_h_j = adnl_h_j)
                                break 
            
            if typ == 'UNILOAD':
                D = D[:2]
                P = P[:2]
                elms_indx = []
                for i in range(2):
                    for q in range(len(cum_LEN)):
                        if D[i] < cum_LEN[q] :
                            # print(f'LOADING ELEMENT at {D[i]}m = {elem_IDS[q-1]}')
                            elms_indx.append(q-1)
                            # rel_loc = (D[i] - cum_LEN[q-1]) / elem_LEN[q-1]
                            break 
                if len(elms_indx)==1: elms_indx.append(len(cum_LEN)-2)
                # print(f"INDEXs = {elms_indx}")
                # print("-"*10)
                # print(f"INDEXs = {elms_indx}")
                # print("-"*10)
                if elms_indx != []:
                    for i in range(elms_indx[0],elms_indx[1]+1):

                        rel1 = (max(D[0],cum_LEN[i]) - cum_LEN[i]) / elem_LEN[i]
                        rel2 = (min(D[1],cum_LEN[i+1]) - cum_LEN[i]) / elem_LEN[i]

                        p1 = P[0]+(max(D[0],cum_LEN[i])-D[0])*(P[1]-P[0])/(D[1]-D[0])
                        p2 = P[0]+(min(D[1],cum_LEN[i+1])-D[0])*(P[1]-P[0])/(D[1]-D[0])
                        if rel2-rel1 == 0: continue
                        

                        # print(f"Loading ELEM -> {elem_IDS[i]} , D1 = {rel1} , P1 = {p1} | D2 = {rel2} , P2 = {p2}")
                        # Load.Beam(elem_IDS[i],load_case,load_group,D=[rel1,rel2],P=[p1,p2],typ=typ,direction=direction)
                        Load.Beam(element=elem_IDS[i],load_case=load_case,load_group=load_group,D=[rel1,rel2],P=[p1,p2],direction=direction,
                                        id = id, typ = "UNILOAD", use_ecc = use_ecc, use_proj = use_proj,
                                        eccn_dir = eccn_dir, eccn_type = eccn_type, ieccn = ieccn, jeccn = jeccn, adnl_h = adnl_h, adnl_h_i = adnl_h_i, adnl_h_j = adnl_h_j)

                        

                
                