from ._mapi import *
from ._model import *
from ._node import *
from ._group import *

def convList(item):
        if type(item)!=list:
            return [item]
        else:
            return item


# -----  Extend for list of nodes/elems -----

def _ADD_Support(self):
    if isinstance(self.NODE,int):
        Boundary.Support.sups.append(self)
    elif isinstance(self.NODE,list):
        for nID in self.NODE:
            Boundary.Support(nID,self.CONST,self.GROUP)


class Boundary:

    @classmethod
    def create(cls):
        """Creates Boundary elements in MIDAS Civil NX"""
        if cls.Support.sups!=[]: cls.Support.create()
        if cls.ElasticLink.links!=[]: cls.ElasticLink.create()
        if cls.RigidLink.links!=[]: cls.RigidLink.create()
        if cls.MLFC.func!=[]: cls.RigidLink.create()
        if cls.PointSpring.springs!=[]: cls.PointSpring.create()

    
    @classmethod
    def delete(cls):
        """Delets Boundary elements from MIDAS Civil NX and Python"""
        cls.Support.delete()
        cls.ElasticLink.delete()
        cls.RigidLink.delete()
        cls.MLFC.delete()
        cls.PointSpring.delete()

    @classmethod
    def sync(cls):
        """Sync Boundary elements from MIDAS Civil NX to Python"""
        cls.Support.sync()
        cls.ElasticLink.sync()
        cls.RigidLink.sync()
        cls.MLFC.sync()
        cls.PointSpring.sync()


    class Support:
        """Create Support Object in Python \n\nNode ID, Constraint, Boundary Group.  Sample: Support(3, "1110000") or Support(3, "pin").  \nValid inputs for DOF are 1s and 0s or "pin", "fix", "free" (no capital letters).  
        \nIf more than 7 characters are entered, then only first 7 characters will be considered to define constraint."""
        sups = []
        def __init__(self, node, constraint, group = ""):
            if not isinstance(constraint, str): constraint = str(constraint)
            if constraint == "pin": constraint = "111"
            if constraint == "fix": constraint = "1111111"
            if constraint == "roller": constraint = "001"
            if len(constraint) < 7: constraint = constraint + '0' * (7-len(constraint))
            if len(constraint) > 7: constraint = constraint[:7]
            string = ''.join(['1' if char != '0' else '0' for char in constraint])

            # Check if group exists, create if not
            if group != "":
                chk = 0
                a = [v['NAME'] for v in Group.Boundary.json()["Assign"].values()]
                if group in a:
                    chk = 1
                if chk == 0:
                    Group.Boundary(group)

            self.NODE = node
            self.CONST = string
            self.GROUP = group
            self.ID = len(Boundary.Support.sups) + 1
            _ADD_Support(self)
    
        @classmethod
        def json(cls):
            """Creates JSON from Supports objects defined in Python"""
            json = {"Assign":{}}
            ng = []
            for i in Boundary.Support.sups:
                if i.NODE in Node.ids:
                    json["Assign"][i.NODE] = {"ITEMS":
                            [{"ID": i.ID,
                            "CONSTRAINT":i.CONST,
                            "GROUP_NAME": i.GROUP}]
                            }
                if i.NODE not in Node.ids: ng.append(i.NODE)
            if len(ng) > 0: print("These nodes are not defined: ", ng)
            return json
        
        @staticmethod
        def create():
            """Creates Supports in MIDAS Civil NX"""
            MidasAPI("PUT","/db/cons",Boundary.Support.json())
            
        @staticmethod
        def get():
            """Get the JSON of Supports from MIDAS Civil NX"""
            return MidasAPI("GET","/db/cons")
        
        @staticmethod
        def sync():
            """Sync Supports from MIDAS Civil NX to Python"""
            a = Boundary.Support.get()
            if a != {'message': ''}:
                if list(a['CONS'].keys()) != []:
                    Boundary.Support.sups = []
                    for j in a['CONS'].keys():
                        Boundary.Support(int(j),a['CONS'][j]['ITEMS'][0]['CONSTRAINT'])
        
        @staticmethod
        def delete():
            """Delete Supports from MIDAS Civil NX and Python"""
            Boundary.Support.sups=[]
            return MidasAPI("DELETE","/db/cons")




    #---------------------------------------------------------------------------------------------------------------
    #Class to define Elastic Links:
    class ElasticLink:

        # list to store all link instances
        links = []
        
        def __init__(self, 
                    i_node: int, 
                    j_node: int, 
                    group: str = "", 
                    id: int = None, 
                    link_type: str = "GEN",
                    sdx: float = 0, 
                    sdy: float = 0, 
                    sdz: float = 0, 
                    srx: float = 0, 
                    sry: float = 0, 
                    srz: float = 0, 
                    shear: bool = False, 
                    dr_y: float = 0.5, 
                    dr_z: float = 0.5, 
                    beta_angle: float = 0, 
                    dir: str = "Dy", 
                    func_id: int = 1, 
                    distance_ratio: float = 0):
            """
            Elastic link. 
            Parameters:
                i_node: The first node ID
                j_node: The second node ID
                group: The group name (default "")
                id: The link ID (optional)
                link_type: Type of link (GEN, RIGID, TENS, COMP, MULTI LINEAR, SADDLE, RAIL INTERACT) (default "GEN")
                sdx: Spring stiffness in X direction (default 0)
                sdy: Spring stiffness in Y direction (default 0)
                sdz: Spring stiffness in Z direction (default 0)
                srx: Rotational stiffness around X axis (default 0)
                sry: Rotational stiffness around Y axis (default 0)
                srz: Rotational stiffness around Z axis (default 0)
                shear: Consider shear effects (default False)
                dr_y: Distance ratio for Y direction (default 0.5)
                dr_z: Distance ratio for Z direction (default 0.5)
                beta_angle: Rotation angle in degrees (default 0)
                dir: Direction for MULTI LINEAR or RAIL INTERACT links (default "Dy")
                func_id: Function ID for MULTI LINEAR or RAIL INTERACT links (default 1)
                distance_ratio: Distance ratio for MULTI LINEAR or RAIL INTERACT links (default 0)
            
            Examples:
                ```python
                # General link with all stiffness parameters
                ElasticLink(1, 2, "Group1", 1, "GEN", 1000, 1000, 1000, 100, 100, 100)     
                # Rigid link
                ElasticLink(3, 4, "Group2", 2, "RIGID")
                # Tension-only link
                ElasticLink(5, 6, "Group3", 3, "TENS", 500)
                # Compression-only link
                ElasticLink(7, 8, "Group4", 4, "COMP", 500)
                # Rail Track Type link
                ElasticLink(9, 10, "Group5", 5, "RAIL INTERACT", dir="Dy", func_id=1)
                # Multi Linear Link
                ElasticLink(11, 12, "Group6", 6, "MULTI LINEAR", dir="Dy", func_id=1)
                # Saddle type link
                ElasticLink(13, 14, "Group7", 7, "SADDLE")
                ```
            """
            # Check if group exists, create if not
            if group != "":
                chk = 0
                a = [v['NAME'] for v in Group.Boundary.json()["Assign"].values()]
                if group in a:
                    chk = 1
                if chk == 0:
                    Group.Boundary(group)
                    
            # Validate link type
            valid_types = ["GEN", "RIGID", "TENS", "COMP", "MULTI LINEAR", "SADDLE", "RAIL INTERACT"]
            if link_type not in valid_types:
                link_type = "GEN"
                
            # Validate direction for MULTI LINEAR
            if link_type == "MULTI LINEAR":
                valid_directions = ["Dx", "Dy", "Dz", "Rx", "Ry", "Rz"]
                if dir not in valid_directions:
                    dir = "Dy"
                    
            # Validate direction for RAIL INTERACT
            if link_type == "RAIL INTERACT":
                valid_directions = ["Dy", "Dz"]
                if dir not in valid_directions:
                    dir = "Dy"
            
            self.I_NODE = i_node
            self.J_NODE = j_node
            self.GROUP_NAME = group
            self.LINK_TYPE = link_type
            self.ANGLE = beta_angle
            
            # Parameters for all link types
            self.SDx = sdx
            self.SDy = sdy
            self.SDz = sdz
            self.SRx = srx
            self.SRy = sry
            self.SRz = srz
            self.bSHEAR = shear
            self.DR_Y = dr_y
            self.DR_Z = dr_z
            
            # Parameters for MULTI LINEAR and RAIL INTERACT
            self.Direction = dir
            self.Function_ID = func_id
            self.Distance_ratio = distance_ratio
            
            # Auto-assign ID if not provided
            if id is None:
                self.ID = len(Boundary.ElasticLink.links) + 1
            else:
                self.ID = id
                
            # Add to static list
            Boundary.ElasticLink.links.append(self)
        
        @classmethod
        def json(cls):
            """
            Converts ElasticLink data to JSON format for API submission.
            Example:
                # Get the JSON data for all links
                json_data = ElasticLink.json()
                print(json_data)
            """
            data = {}
            
            for link in cls.links:
                link_data = {
                    "NODE": [link.I_NODE, link.J_NODE],
                    "LINK": link.LINK_TYPE,
                    "ANGLE": link.ANGLE,
                    "BNGR_NAME": link.GROUP_NAME
                }
                
                # Add type-specific parameters
                if link.LINK_TYPE == "GEN":
                    link_data["R_S"] = [False] * 6
                    link_data["SDR"] = [
                        link.SDx,
                        link.SDy,
                        link.SDz,
                        link.SRx,
                        link.SRy,
                        link.SRz
                    ]
                    link_data["bSHEAR"] = link.bSHEAR
                    if link.bSHEAR:
                        link_data["DR"] = [link.DR_Y, link.DR_Z]
                    else:
                        link_data["DR"] = [0.5, 0.5]
                    
                elif link.LINK_TYPE in ["TENS", "COMP"]:
                    link_data["SDR"] = [link.SDx, 0, 0, 0, 0, 0]
                    link_data["bSHEAR"] = link.bSHEAR
                    if link.bSHEAR:
                        link_data["DR"] = [link.DR_Y, link.DR_Z]
                    else:
                        link_data["DR"] = [0.5, 0.5]
                        
                elif link.LINK_TYPE == "MULTI LINEAR":
                    direction_mapping = {
                        "Dx": 0, "Dy": 1, "Dz": 2, "Rx": 3, "Ry": 4, "Rz": 5
                    }
                    link_data["DIR"] = direction_mapping.get(link.Direction, 0)
                    link_data["MLFC"] = link.Function_ID
                    link_data["DRENDI"] = link.Distance_ratio
                    
                elif link.LINK_TYPE == "RAIL INTERACT":
                    direction_mapping = {"Dy": 1, "Dz": 2}
                    link_data["DIR"] = direction_mapping.get(link.Direction, 0)
                    link_data["RLFC"] = link.Function_ID
                    link_data["bSHEAR"] = link.bSHEAR
                    if link.bSHEAR:
                        link_data["DEENDI"] = link.Distance_ratio
                    else:
                        link_data["DR"] = [0.5, 0.5]
                    
                data[link.ID] = link_data
                
            return {"Assign": data}
        
        @classmethod
        def create(cls):
            """
            Sends all ElasticLink data to Midas API.
            Example:
                ElasticLink(1, 2, "Group1", 1, "GEN", 1000, 1000, 1000, 100, 100, 100)
                # Send to the API
                ElasticLink.create()
            """
            MidasAPI("PUT", "/db/elnk", cls.json())
        
        @classmethod
        def get(cls):
            """
            Retrieves ElasticLink data from Midas API.
            Example:
                api_data = ElasticLink.get()
                print(api_data)
            """
            return MidasAPI("GET", "/db/elnk")
        
        @classmethod
        def sync(cls):
            """
            Updates the ElasticLink class with data from the Midas API.
            Example:
                ElasticLink.sync()
            """
            cls.links = []
            a = cls.get()
            
            if a != {'message': ''}:
                for link_id, link_data in a.get("ELNK", {}).items(): 
                    sdx = sdy = sdz = srx = sry = srz = 0
                    shear = False
                    dr_y = dr_z = 0.5
                    direction = "Dy"
                    func_id = 1
                    distance_ratio = 0

                    if link_data["LINK"] == "GEN" and "SDR" in link_data:
                        sdx, sdy, sdz, srx, sry, srz = link_data["SDR"]
                        shear = link_data.get("bSHEAR")
                        if shear and "DR" in link_data:
                            dr_y, dr_z = link_data["DR"]

                    elif link_data["LINK"] in ["TENS", "COMP"] and "SDR" in link_data:
                        sdx = link_data["SDR"][0]
                        shear = link_data.get("bSHEAR")
                        if shear and "DR" in link_data:
                            dr_y, dr_z = link_data["DR"]

                    elif link_data["LINK"] == "MULTI LINEAR":
                        dir_mapping = {0: "Dx", 1: "Dy", 2: "Dz", 3: "Rx", 4: "Ry", 5: "Rz"}
                        direction = dir_mapping.get(link_data.get("DIR"), "Dy")
                        func_id = link_data.get("MLFC")
                        distance_ratio = link_data.get("DRENDI")

                    elif link_data["LINK"] == "RAIL INTERACT":
                        dir_mapping = {1: "Dy", 2: "Dz"}
                        direction = dir_mapping.get(link_data.get("DIR"), "Dy")
                        func_id = link_data.get("RLFC")
                        shear = link_data.get("bSHEAR")
                        if shear and "DEENDI" in link_data:
                            distance_ratio = link_data["DEENDI"]

                    Boundary.ElasticLink(
                        link_data["NODE"][0],
                        link_data["NODE"][1],
                        link_data.get("BNGR_NAME"),
                        int(link_id),
                        link_data["LINK"],
                        sdx, sdy, sdz, srx, sry, srz,
                        shear, dr_y, dr_z,
                        link_data.get("ANGLE"),
                        direction, func_id, distance_ratio
                    )
        
        @classmethod
        def delete(cls):
            """
            Deletes all elastic links from the database and resets the class.
            Example:sss
                ElasticLink.delete()
            """
            cls.links = []
            return MidasAPI("DELETE", "/db/elnk")
    #---------------------------------------------------------------------------------------------------------------


    #Class to define Rigid  Links:
    class RigidLink:

        links = []
        
        def __init__(self, 
                    master_node: int, 
                    slave_nodes: list, 
                    group: str = "", 
                    id: int = None, 
                    dof: int = 111111,):
            """
            Rigid link. 
            Parameters:
                master_node: The first node ID
                slave_nodes: The second node ID
                group: The group name (default "")
                id: The link ID (optional)
                dof: Fixity of link (default 111111)
            
            Examples:
                ```python
                # General link with all stiffness parameters
                RigidLink(1, [2,3], "Group1", 1, 111000)
                ```
            """

            # Check if group exists, create if not
            if group != "":
                chk = 0
                a = [v['NAME'] for v in Group.Boundary.json()["Assign"].values()]
                if group in a:
                    chk = 1
                if chk == 0:
                    Group.Boundary(group)
                    
            
            self.M_NODE = master_node
            self.S_NODE = convList(slave_nodes)
            self.GROUP_NAME = group
            self.DOF = dof

            # Auto-assign ID if not provided
            if id is None:
                self.ID = len(Boundary.RigidLink.links) + 1
            else:
                self.ID = id
                
            # Add to static list
            Boundary.RigidLink.links.append(self)
        

        @classmethod
        def json(cls):
            """
            Converts RigidLink data to JSON format for API submission.
            Example:
                # Get the JSON data for all links
                json_data = RigidLink.json()
                print(json_data)
            """
            json = {"Assign": {}}
            for link in cls.links:
                if link.M_NODE not in list(json["Assign"].keys()):
                    json["Assign"][link.M_NODE] = {"ITEMS": []}

                json["Assign"][link.M_NODE]["ITEMS"].append({
                    "ID": link.ID,
                    "GROUP_NAME": link.GROUP_NAME,
                    "DOF": link.DOF,
                    "S_NODE": convList(link.S_NODE),
                })
            return json
        
        @classmethod
        def create(cls):
            """
            Sends all RigidLink data to Midas API.
            Example:
                RigidLink(1, 2, "Group1", 1, "GEN", 1000, 1000, 1000, 100, 100, 100)
                # Send to the API
                RigidLink.create()
            """
            MidasAPI("PUT", "/db/RIGD", cls.json())
        
        @classmethod
        def get(cls):
            """
            Retrieves Rigid Link data from Midas API.
            Example:
                api_data = RigidLink.get()
                print(api_data)
            """
            return MidasAPI("GET", "/db/RIGD")
        
        @classmethod
        def sync(cls):
            """
            Updates the RigidLink class with data from the Midas API.
            Example:
                RigidLink.sync()
            """
            cls.links = []
            a = cls.get()
            if a != {'message': ''}:
                for i in a['RIGD'].keys():
                    for j in range(len(a['RIGD'][i]['ITEMS'])):
                        itm = a['RIGD'][i]['ITEMS'][j]
                        Boundary.RigidLink(int(i),itm['S_NODE'],itm['GROUP_NAME'],itm['ID'],itm['DOF'])
        
        @classmethod
        def delete(cls):
            """
            Deletes all rigid links from the database and resets the class.
            Example:
                ElasticLink.delete()
            """
            cls.links = []
            return MidasAPI("DELETE", "/db/RIGD")
    #---------------------------------------------------------------------------------------------------------------

    class MLFC:

        func = []
        _id = []

        def __init__(self, name:str, type:str='FORCE', symm:bool=True, data:list=[[0,0],[1,1]], id:int=None):
            """
            Force-Deformation Function constructor.

            Parameters:
                name (str): The name for the Force-Deformation Function.
                type (str, optional): Type of function, either "FORCE" or "MOMENT". Defaults to "FORCE".
                symm (bool, optional): Defines if the function is symmetric (True) or unsymmetric (False). Defaults to True.
                data (list[list[float]], optional): A list of [X, Y] coordinate pairs defining the function curve. Required.
                    - For "FORCE" type: X is displacement, Y is force.
                    - For "MOMENT" type: X is rotation in radians, Y is moment.
                    Defaults to [[0,0],[1,1]].
                id (int, optional): The function ID. If not provided, it will be auto-assigned.

            Examples:
                ```python
                # Create a symmetric force vs. displacement function
                Boundary.MLFC(name="MyForceFunction", type="FORCE", symm=True, data=[[0,0], [0.1, 100], [0.2, 150]])

                # Create an unsymmetric moment vs. rotation function with a specific ID
                Boundary.MLFC(name="MyMomentFunction", type="MOMENT", symm=False, data=[[0,0], [0.01, 500], [0.02, 750]], id=5)
                ```
            """
            self.NAME = name
            self.TYPE = type
            self.SYMM = symm
            self.DATA = data

            self.X = [dat[0] for dat in self.DATA]
            self.Y = [dat[1] for dat in self.DATA]

            # Auto-assign ID if not provided
            if id is None:
                if __class__._id == []:
                    self.ID = 1
                else:
                    self.ID = max(__class__._id) + 1
            else:
                self.ID = id

            __class__._id.append(self.ID)
            __class__.func.append(self)
        

        
        @classmethod
        def json(cls):
           
            json = {"Assign": {}}
            for fn in cls.func:
                json["Assign"][fn.ID]={
                    "NAME": fn.NAME,
                    "TYPE": fn.TYPE,
                    "SYMM": fn.SYMM,
                    "FUNC_ID": 0,
                    "ITEMS": []
                }
                for i in range(len(fn.X)):
                    json["Assign"][fn.ID]["ITEMS"].append({"X":fn.X[i],"Y":fn.Y[i]})
            return json
        
        @classmethod
        def create(cls):
            """
            Sends all FUNC data.
            """
            MidasAPI("PUT", "/db/MLFC", cls.json())
        
        @classmethod
        def get(cls):
            """
            Retrieves data.
            """
            return MidasAPI("GET", "/db/MLFC")
        
        @classmethod
        def sync(cls):
            
            cls.links = []
            a = cls.get()
            if a != {'message': ''}:
                for i in a['MLFC'].keys():
                    name = a['MLFC'][i]["NAME"]
                    type = a['MLFC'][i]["TYPE"]
                    symm = a['MLFC'][i]["SYMM"]
                    data = []
                    for j in (a['MLFC'][i]['ITEMS']):
                        data.append([j["X"],j["Y"]])
                    Boundary.MLFC(name,type,symm,data,int(i))
        
        @classmethod
        def delete(cls):
            """
            Deletes all func from the database and resets the class.
            """
            cls.links = []
            return MidasAPI("DELETE", "/db/MLFC")

#--------------------------------------------------------------------------------------------------------------------------------------


    class PointSpring:
        """Create Point Spring Object in Python"""
        springs = []
        
        def __init__(self, 
                    node: int,
                    spring_type: str = "LINEAR",
                    group: str = "",
                    id: int = None,
                    stiffness: list = None,
                    fixed_option: list = None,
                    damping: list = None,
                    direction: str = "Dx+",
                    normal_vector: list = None,
                    function_id: int = 1):
            """
            Point Spring constructor.
            
            Parameters:
                node: Node ID where spring is applied
                spring_type: Type of spring ("LINEAR", "COMP", "TENS", "MULTI")
                group: Group name (default "")
                id: Spring ID (optional, auto-assigned if None)
                stiffness: Spring stiffness values [SDx, SDy, SDz, SRx, SRy, SRz] or single value for COMP/TENS
                fixed_option: Fixed option array [Boolean, 6] for LINEAR type
                damping: Damping values [Cx, Cy, Cz, CRx, CRy, CRz] (if provided, damping is enabled)
                direction: Direction string ("Dx+", "Dx-", "Dy+", "Dy-", "Dz+", "Dz-", "Vector")
                normal_vector: Normal vector [x, y, z] when direction is "Vector"
                function_id: Function ID for MULTI type
            
            Examples:
                # Linear spring
                PointSpring(1, "LINEAR", "Group1", stiffness=[1000, 1000, 1000, 100, 100, 100])
                
                # Compression only spring
                PointSpring(2, "COMP", "Group2", stiffness=5000, direction="Dz+")
                
                # Tension only spring with vector direction
                PointSpring(3, "TENS", "Group3", stiffness=3000, direction="Vector", normal_vector=[0, -1, -1])
                
                # Multi-linear spring
                PointSpring(4, "MULTI", "Group4", direction="Dz+", function_id=1)
            """
            
            # Check if group exists, create if not
            if group != "":
                chk = 0
                a = [v['NAME'] for v in Group.Boundary.json()["Assign"].values()]
                if group in a:
                    chk = 1
                if chk == 0:
                    Group.Boundary(group)
            
            # Validate spring type
            valid_types = ["LINEAR", "COMP", "TENS", "MULTI"]
            if spring_type not in valid_types:
                spring_type = "LINEAR"
            
            self.NODE = node
            self.TYPE = spring_type
            self.GROUP_NAME = group
            
            # Convert direction string to integer
            direction_map = {
                "Dx+": 0, "Dx-": 1, "Dy+": 2, "Dy-": 3, 
                "Dz+": 4, "Dz-": 5, "Vector": 6
            }
            self.DIR = direction_map.get(direction, 0)
            
            # Auto-assign ID if not provided
            if id is None:
                self.ID = len(Boundary.PointSpring.springs) + 1
            else:
                self.ID = id
            
            # Type-specific parameters
            if spring_type == "LINEAR":
                self.SDR = stiffness if stiffness else [0, 0, 0, 0, 0, 0]
                self.F_S = fixed_option if fixed_option else [False] * 6
                # Damping logic: if damping values provided, enable damping
                self.DAMPING = damping is not None and any(d != 0 for d in damping) if damping else False
                self.Cr = damping if damping else [0, 0, 0, 0, 0, 0]
                
            elif spring_type in ["COMP", "TENS"]:
                self.STIFF = stiffness if stiffness else 0
                self.DV = normal_vector if normal_vector else [0, 0, 0]
                
            elif spring_type == "MULTI":
                self.DV = normal_vector if normal_vector else [0, 0, 0]
                self.FUNCTION = function_id
            
            # Add to static list
            Boundary.PointSpring.springs.append(self)
        
        @classmethod
        def json(cls):
            """
            Converts PointSpring data to JSON format for API submission.
            """
            json_data = {"Assign": {}}
            
            for spring in cls.springs:
                spring_data = {
                    "ID": spring.ID,
                    "TYPE": spring.TYPE,
                    "GROUP_NAME": spring.GROUP_NAME
                }
                
                # Add type-specific parameters
                if spring.TYPE == "LINEAR":
                    spring_data["SDR"] = spring.SDR
                    spring_data["F_S"] = spring.F_S
                    spring_data["DAMPING"] = spring.DAMPING
                    if spring.DAMPING:
                        spring_data["Cr"] = spring.Cr
                        
                elif spring.TYPE in ["COMP", "TENS"]:
                    spring_data["STIFF"] = spring.STIFF
                    spring_data["DIR"] = spring.DIR
                    spring_data["DV"] = spring.DV
                    
                elif spring.TYPE == "MULTI":
                    spring_data["DIR"] = spring.DIR
                    spring_data["DV"] = spring.DV
                    spring_data["FUNCTION"] = spring.FUNCTION
                
                json_data["Assign"][spring.NODE] = {"ITEMS": [spring_data]}
            
            return json_data
        
        @classmethod
        def create(cls):
            """
            Sends all PointSpring data
            """
            MidasAPI("PUT", "/db/nspr", cls.json())
        
        @classmethod
        def get(cls):
            """
            Retrieves PointSpring data
            """
            return MidasAPI("GET", "/db/nspr")
        
        @classmethod
        def sync(cls):
            """
            Updates the PointSpring class with data 
            """
            cls.springs = []
            a = cls.get()
            
            if a != {'message': ''}:
                for node_id, node_data in a.get("NSPR", {}).items():
                    for item in node_data.get("ITEMS"):
                        spring_type = item.get("TYPE")
                        group_name = item.get("GROUP_NAME")
                        spring_id = item.get("ID", 1)
                        
                        # Extract type-specific parameters
                        if spring_type == "LINEAR":
                            stiffness = item.get("SDR")
                            fixed_option = item.get("F_S")
                            damping = item.get("Cr") if item.get("DAMPING", False) else None
                            
                            # Convert direction back to string
                            dir_map = {0: "Dx+", 1: "Dx-", 2: "Dy+", 3: "Dy-", 4: "Dz+", 5: "Dz-", 6: "Vector"}
                            direction_str = dir_map.get(0, "Dx+")  # Default for LINEAR
                            
                            Boundary.PointSpring(
                                int(node_id), spring_type, group_name, spring_id,
                                stiffness, fixed_option, damping, direction_str
                            )
                            
                        elif spring_type in ["COMP", "TENS"]:
                            stiffness = item.get("STIFF")
                            direction_int = item.get("DIR")
                            normal_vector = item.get("DV")
                            
                            # Convert direction back to string
                            dir_map = {0: "Dx+", 1: "Dx-", 2: "Dy+", 3: "Dy-", 4: "Dz+", 5: "Dz-", 6: "Vector"}
                            direction_str = dir_map.get(direction_int, "Dx+")
                            
                            Boundary.PointSpring(
                                int(node_id), spring_type, group_name, spring_id,
                                stiffness, None, None, direction_str, normal_vector
                            )
                            
                        elif spring_type == "MULTI":
                            direction_int = item.get("DIR")
                            normal_vector = item.get("DV")
                            function_id = item.get("FUNCTION")
                            
                            # Convert direction back to string
                            dir_map = {0: "Dx+", 1: "Dx-", 2: "Dy+", 3: "Dy-", 4: "Dz+", 5: "Dz-", 6: "Vector"}
                            direction_str = dir_map.get(direction_int, "Dx+")
                            
                            Boundary.PointSpring(
                                int(node_id), spring_type, group_name, spring_id,
                                None, None, None, direction_str, normal_vector, function_id
                            )
        
        @classmethod
        def delete(cls):
            """
            Deletes all point springs from the database and resets the class.
            """
            cls.springs = []
            return MidasAPI("DELETE", "/db/nspr")