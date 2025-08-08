from ._mapi import *
from ._node import *
from ._group import _add_elem_2_stGroup
from ._group import _add_node_2_stGroup

import numpy as np






def _ADD(self):
    """
    Adds an element to the main list. If the ID is 0, it auto-increments.
    If the ID already exists, it replaces the existing element.
    """

    # ------------  ID assignment -----------------------
    id = int(self.ID)
    if not Element.ids:
        count = 1
    else:
        count = max(Element.ids) + 1

    if id == 0:
        self.ID = count
        Element.elements.append(self)
        Element.ids.append(int(self.ID))
    elif id in Element.ids:
        self.ID = int(id)
        print(f'⚠️  Element with ID {id} already exists! It will be replaced.')
        index = Element.ids.index(id)
        Element.elements[index] = self
    else:
        self.ID = id
        Element.elements.append(self)
        Element.ids.append(int(self.ID))
    
    # ------------  Group assignment -----------------------
    if self._GROUP == "" :
        pass
    elif isinstance(self._GROUP, list):
        for gpName in self._GROUP:
            _add_elem_2_stGroup(self.ID,gpName)
            for nd in self.NODE:
                _add_node_2_stGroup(nd,gpName)
    elif isinstance(self._GROUP, str):
        _add_elem_2_stGroup(self.ID,self._GROUP)
        for nd in self.NODE:
            _add_node_2_stGroup(nd,self._GROUP)
            





def _updateElem(self):
    """Sends a PUT request to update a single element in Midas."""
    js2s = {'Assign': {self.ID: _Obj2JS(self)}}
    MidasAPI('PUT', '/db/elem', js2s)
    return js2s

def _Obj2JS(obj):
    """Converts a Python element object to its JSON dictionary representation."""
    # Base attributes common to many elements
    js = {
        "TYPE": obj.TYPE,
        "MATL": obj.MATL,
        "SECT": obj.SECT,
        "NODE": obj.NODE,
    }
    
    # Add optional attributes if they exist on the object
    if hasattr(obj, 'ANGLE'): js["ANGLE"] = obj.ANGLE
    if hasattr(obj, 'STYPE'): js["STYPE"] = obj.STYPE
    
    # Handle type-specific and subtype-specific attributes
    if obj.TYPE == 'TENSTR': # Tension/Hook/Cable
        # Tension-only (stype=1) - can have TENS parameter
        if obj.STYPE == 1:
            if hasattr(obj, 'TENS'): js["TENS"] = obj.TENS
            if hasattr(obj, 'T_LIMIT'): js["T_LIMIT"] = obj.T_LIMIT
            if hasattr(obj, 'T_bLMT'): js["T_bLMT"] = obj.T_bLMT
        
        # Hook (stype=2) - has NON_LEN parameter
        elif obj.STYPE == 2:
            if hasattr(obj, 'NON_LEN'): js["NON_LEN"] = obj.NON_LEN
        
        # Cable (stype=3) - has CABLE, NON_LEN, and TENS parameters
        elif obj.STYPE == 3:
            if hasattr(obj, 'CABLE'): js["CABLE"] = obj.CABLE
            if hasattr(obj, 'NON_LEN'): js["NON_LEN"] = obj.NON_LEN
            if hasattr(obj, 'TENS'): js["TENS"] = obj.TENS

    elif obj.TYPE == 'COMPTR': # Compression/Gap
        # Compression-only (stype=1) - can have TENS, T_LIMIT, T_bLMT
        if obj.STYPE == 1:
            if hasattr(obj, 'TENS'): js["TENS"] = obj.TENS
            if hasattr(obj, 'T_LIMIT'): js["T_LIMIT"] = obj.T_LIMIT
            if hasattr(obj, 'T_bLMT'): js["T_bLMT"] = obj.T_bLMT
        
        # Gap (stype=2) - has NON_LEN parameter
        elif obj.STYPE == 2:
            if hasattr(obj, 'NON_LEN'): js["NON_LEN"] = obj.NON_LEN
            
    return js

def _JS2Obj(id, js):
    """Converts a JSON dictionary back into a Python element object during sync."""
    elem_type = js.get('TYPE')
    
    # Prepare arguments for constructors
    args = {
        'id': int(id),
        'mat': js.get('MATL'),
        'sect': js.get('SECT'),
        'node': js.get('NODE'),
        'angle': js.get('ANGLE'),
        'stype': js.get('STYPE')
    }
    
    # Prepare individual parameters for optional/subtype-specific parameters
    non_len = js.get('NON_LEN')
    cable_type = js.get('CABLE')
    tens = js.get('TENS')
    t_limit = js.get('T_LIMIT')

    if elem_type == 'BEAM':
        Element.Beam(args['node'][0], args['node'][1], args['mat'], args['sect'], args['angle'], '', args['id'])
    elif elem_type == 'TRUSS':
        Element.Truss(args['node'][0], args['node'][1], args['mat'], args['sect'], args['angle'],'',  args['id'])
    elif elem_type == 'PLATE':
        Element.Plate(args['node'], args['stype'], args['mat'], args['sect'], args['angle'], '', args['id'])
    elif elem_type == 'TENSTR':
        Element.Tension(args['node'][0], args['node'][1], args['stype'], args['mat'], args['sect'], args['angle'], '', args['id'], non_len, cable_type, tens, t_limit)
    elif elem_type == 'COMPTR':
        Element.Compression(args['node'][0], args['node'][1], args['stype'], args['mat'], args['sect'], args['angle'], '', args['id'], tens, t_limit, non_len)
    elif elem_type == 'SOLID':
        Element.Solid(nodes=args['node'], mat=args['mat'], sect=args['sect'],group='', id=args['id'])


class _common:
    """Common base class for all element types."""
    def __str__(self):
        return str(f'ID = {self.ID} \nJSON : {_Obj2JS(self)}\n')

    def update(self):
        return _updateElem(self)

# --- Main Element Class ---
class Element:
    """
    Main class to create and manage structural elements like Beams, Trusses,
    Plates, Tension/Compression-only elements, and Solids.
    """
    elements = []
    ids = []

    @classmethod
    def json(cls):
        json_data = {"Assign": {}}
        for elem in cls.elements:
            js = _Obj2JS(elem)
            json_data["Assign"][elem.ID] = js
        return json_data

    @classmethod
    def create(cls):
        if cls.elements:
            MidasAPI("PUT", "/db/ELEM", Element.json())

    @staticmethod
    def get():
        return MidasAPI("GET", "/db/ELEM")

    @staticmethod
    def sync():
        a = Element.get()
        if a and 'ELEM' in a and a['ELEM']:
            Element.elements = []
            Element.ids = []
            for elem_id, data in a['ELEM'].items():
                _JS2Obj(elem_id, data)

    @staticmethod
    def delete():
        MidasAPI("DELETE", "/db/ELEM")
        Element.elements = []
        Element.ids = []

    # --- Element Type Subclasses ---

    class Beam(_common):

        def __init__(self, i: int, j: int, mat: int = 1, sect: int = 1, angle: float = 0, group = "" , id: int = 0):
            """
            Creates a BEAM element for frame analysis.
            
            Parameters:
                i: Start node ID
                j: End node ID  
                mat: Material property number (default 1)
                sect: Section property number (default 1)
                angle: Beta angle for section orientation in degrees (default 0.0)
                group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
                id: Element ID (default 0 for auto-increment)
            
            Examples:
                ```python
                # Simple beam with default properties
                Element.Beam(1, 2)
                
                # Beam with specific material and section
                Element.Beam(1, 2, mat=2, sect=3)
                
                # Beam with 90° rotation (strong axis vertical)
                Element.Beam(1, 2, mat=1, sect=1, angle=90.0)
                
                # Beam with specific ID
                Element.Beam(1, 2, mat=1, sect=1, angle=0.0, id=100)
                ```
            """
            self.ID = id
            self.TYPE = 'BEAM'
            self.MATL = mat
            self.SECT = sect
            self.NODE = [i, j]
            self.ANGLE = angle
            self._GROUP = group
            _ADD(self)

        @staticmethod
        def SDL(s_loc:list|Node,dir:list,l:float,n:int=1,mat:int=1,sect:int=1,angle:float=0, group = "" , id: int = 0): #CHANGE TO TUPLE
                if isinstance(s_loc,Node):
                    s_loc = (s_loc.X,s_loc.Y,s_loc.Z)

                beam_nodes =[]
                beam_obj = []
                s_locc = np.array(s_loc)
                unit_vec = np.array(dir)/np.linalg.norm(dir)

                for i in range(n+1):
                    locc = s_locc+i*l*unit_vec/n
                    Enode=Node(locc[0].item(),locc[1].item(),locc[2].item())
                    beam_nodes.append(Enode.ID)
                
                for i in range(n):
                    if id == 0 : id_new = 0
                    else: id_new = id+i
                    beam_obj.append(Element.Beam(beam_nodes[i],beam_nodes[i+1],mat,sect,angle,group,id_new))
                
                return beam_obj
                    

        @staticmethod
        def SE(s_loc:list|Node,e_loc:list|Node,n:int=1,mat:int=1,sect:int=1,angle:float=0, group = "" , id: int = 0):
                if isinstance(s_loc,Node):
                    s_loc = (s_loc.X,s_loc.Y,s_loc.Z)
                if isinstance(e_loc,Node):
                    s_loc = (e_loc.X,e_loc.Y,e_loc.Z)

                beam_nodes =[]
                beam_obj = []
                i_loc = np.linspace(s_loc,e_loc,n+1)
                for i in range(n+1):
                    Enode=Node(i_loc[i][0].item(),i_loc[i][1].item(),i_loc[i][2].item())
                    beam_nodes.append(Enode.ID)
                
                for i in range(n):
                    if id == 0 : id_new = 0
                    else: id_new = id+i
                    beam_obj.append(Element.Beam(beam_nodes[i],beam_nodes[i+1],mat,sect,angle,group,id_new))
                
                return beam_obj

    class Truss(_common):
        def __init__(self, i: int, j: int, mat: int = 1, sect: int = 1, angle: float = 0, group = "" , id: int = 0):
            """
            Creates a TRUSS element
            
            Parameters:
                i: Start node ID
                j: End node ID
                mat: Material property number (default 1)
                sect: Section property number (default 1)
                angle: Beta angle for section orientation in degrees (default 0.0)
                group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
                id: Element ID (default 0 for auto-increment)
            
            Examples:
                ```python
                # Simple truss member
                Element.Truss(1, 2)
                
                # Truss with specific material and section
                Element.Truss(1, 2, mat=3, sect=2)
                
                # Diagonal truss member
                Element.Truss(3, 4, mat=1, sect=1, id=50)
                ```
            """
            self.ID = id
            self.TYPE = 'TRUSS'
            self.MATL = mat
            self.SECT = sect
            self.NODE = [i, j]
            self.ANGLE = angle
            self._GROUP = group
            _ADD(self)

        @staticmethod
        def SDL(s_loc:list|Node,dir:list,l:float,n:int=1,mat:int=1,sect:int=1,angle:float=0, group = "" , id: int = 0):
            if isinstance(s_loc,Node):
                    s_loc = (s_loc.X,s_loc.Y,s_loc.Z)

            beam_nodes =[]
            beam_obj =[]
            s_locc = np.array(s_loc)
            unit_vec = np.array(dir)/np.linalg.norm(dir)

            for i in range(n+1):
                locc = s_locc+i*l*unit_vec/n
                Enode=Node(locc[0].item(),locc[1].item(),locc[2].item())
                beam_nodes.append(Enode.ID)
            
            for i in range(n):
                if id == 0 : id_new = 0
                else: id_new = id+i
                beam_obj.append(Element.Truss(beam_nodes[i],beam_nodes[i+1],mat,sect,angle,group,id_new))
            
            return beam_obj
                

        @staticmethod
        def SE(s_loc:list|Node,e_loc:list|Node,n:int=1,mat:int=1,sect:int=1,angle:float=0, group = "" , id: int = 0):
            
            if isinstance(s_loc,Node):
                s_loc = (s_loc.X,s_loc.Y,s_loc.Z)
            if isinstance(e_loc,Node):
                s_loc = (e_loc.X,e_loc.Y,e_loc.Z)

            beam_nodes =[]
            beam_obj = []
            i_loc = np.linspace(s_loc,e_loc,n+1)
            for i in range(n+1):
                Enode=Node(i_loc[i][0].item(),i_loc[i][1].item(),i_loc[i][2].item())
                beam_nodes.append(Enode.ID)
            
            for i in range(n):
                if id == 0 : id_new = 0
                else: id_new = id+i
                beam_obj.append(Element.Truss(beam_nodes[i],beam_nodes[i+1],mat,sect,angle,group,id_new))
            
            return beam_obj 
          
    class Plate(_common):
        def __init__(self, nodes: list, stype: int = 1, mat: int = 1, sect: int = 1, angle: float = 0, group = "" , id: int = 0):
            """
            Creates a PLATE element.
            
            Parameters:
                nodes: List of node IDs [n1, n2, n3] for triangular or [n1, n2, n3, n4] for quadrilateral
                stype: Plate subtype (1=Thick plate, 2=Thin plate, 3=With drilling DOF) (default 1)
                mat: Material property number (default 1)
                sect: Section (thickness) property number (default 1)
                angle: Material angle for orthotropic materials in degrees (default 0.0)
                group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
                id: Element ID (default 0 for auto-increment)
            
            Examples:
                ```python
                # Triangular thick plate
                Element.Plate([1, 2, 3], stype=1, mat=1, sect=1)
                
                # Quadrilateral thin plate
                Element.Plate([1, 2, 3, 4], stype=2, mat=2, sect=1)
                
                # Plate with drilling DOF for shell analysis
                Element.Plate([5, 6, 7, 8], stype=3, mat=1, sect=2, angle=45.0)
                ```
            """
            self.ID = id
            self.TYPE = 'PLATE'
            self.MATL = mat
            self.SECT = sect
            self.NODE = nodes
            self.ANGLE = angle
            self.STYPE = stype
            self._GROUP = group
            _ADD(self)
            
    class Tension(_common):
     def __init__(self, i: int, j: int, stype: int, mat: int = 1, sect: int = 1, angle: float = 0, group = "" , id: int = 0, non_len: float = None, cable_type: int = None, tens: float = None, t_limit: float = None):
        """
        Creates a TENSTR (Tension-only) element.
        
        Parameters:
            i: Start node ID
            j: End node ID
            stype: Tension element subtype (1=Tension-only, 2=Hook, 3=Cable)
            mat: Material property number (default 1)
            sect: Section property number (default 1)
            angle: Beta angle for section orientation in degrees (default 0.0)
            group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
            id: Element ID (default 0 for auto-increment)
            non_len: Non-linear length parameter for Hook/Cable (default None)
            cable_type: Cable type for stype=3 (1=Pretension, 2=Horizontal, 3=Lu) (default None)
            tens: Initial tension force or allowable compression (default None)
            t_limit: Tension limit value. If provided, the tension limit flag is set to True. (default None)
        
        Examples:
            ```python
            # Simple tension-only member
            Element.Tension(1, 2, stype=1)
            
            # Tension-only with allowable compression and a tension limit
            Element.Tension(1, 2, stype=1, tens=0.5, t_limit=-15)
            
            # Hook element with slack length
            Element.Tension(3, 4, stype=2, non_len=0.5)
            
            # Cable with initial tension and catenary effects
            Element.Tension(5, 6, stype=3, cable_type=3, tens=1000.0, non_len=0.1)
            ```
        """
        self.ID = id
        self.TYPE = 'TENSTR'
        self.MATL = mat
        self.SECT = sect
        self.NODE = [i, j]
        self.ANGLE = angle
        self.STYPE = stype
        self._GROUP = group
        
        # Handle subtype-specific parameters
        if stype == 1:  # Tension-only specific
            if tens is not None:
                self.TENS = tens
            if t_limit is not None:
                self.T_LIMIT = t_limit
                self.T_bLMT = True
                
        elif stype == 2:  # Hook specific
            if non_len is not None:
                self.NON_LEN = non_len
                
        elif stype == 3:  # Cable specific
            if cable_type is not None:
                self.CABLE = cable_type
            if non_len is not None:
                self.NON_LEN = non_len
            if tens is not None:
                self.TENS = tens
        _ADD(self)

    class Compression(_common):
        def __init__(self, i: int, j: int, stype: int, mat: int = 1, sect: int = 1, angle: float = 0, group = "" , id: int = 0, tens: float = None, t_limit: float = None, non_len: float = None):
            """
            Creates a COMPTR (Compression-only) element.
            
            Parameters:
                i: Start node ID
                j: End node ID
                stype: Compression element subtype (1=Compression-only, 2=Gap)
                mat: Material property number (default 1)
                sect: Section property number (default 1)
                angle: Beta angle for section orientation in degrees (default 0.0)
                group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
                id: Element ID (default 0 for auto-increment)
                tens: Allowable tension or initial compression force (default None)
                t_limit: Compression limit value. If provided, the compression limit flag is set to True. (default None)
                non_len: Non-linear length parameter for gap (default None)
            
            Examples:
                ```python
                # Simple compression-only member
                Element.Compression(1, 2, stype=1)
                
                # Compression-only with tension limit and buckling limit
                Element.Compression(1, 2, stype=1, tens=27, t_limit=-15)
                
                # Gap element with initial gap
                Element.Compression(3, 4, stype=2, non_len=0.25)
                ```
            """
            self.ID = id
            self.TYPE = 'COMPTR'
            self.MATL = mat
            self.SECT = sect
            self.NODE = [i, j]
            self.ANGLE = angle
            self.STYPE = stype
            self._GROUP = group
            
            # Handle subtype-specific parameters
            if stype == 1:  # Compression-only specific
                if tens is not None:
                    self.TENS = tens
                if t_limit is not None:
                    self.T_LIMIT = t_limit
                    self.T_bLMT = True
                    
            elif stype == 2:  # Gap specific
                if non_len is not None:
                    self.NON_LEN = non_len
            _ADD(self)

    class Solid(_common):
        def __init__(self, nodes: list, mat: int = 1, sect: int = 0, group = "" , id: int = 0):
            """
            Creates a SOLID element for 3D analysis.
            
            Parameters:
                nodes: List of node IDs defining the solid element
                       - 4 nodes: Tetrahedral element
                       - 6 nodes: Pentahedral element  
                       - 8 nodes: Hexahedral element
                mat: Material property number (default 1)
                group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
                id: Element ID (default 0 for auto-increment)
            
            Examples:
                ```python
                # Tetrahedral solid element
                Element.Solid([1, 2, 3, 4], mat=1)
                
                # Wedge solid element
                Element.Solid([1, 2, 3, 4, 5, 6], mat=2)
                
                # Hexahedral solid element
                Element.Solid([1, 2, 3, 4, 5, 6, 7, 8], mat=1, id=200)
                ```
            """
            if len(nodes) not in [4, 6, 8]:
                raise ValueError("Solid element must have 4, 6, or 8 nodes.")
            self.ID = id
            self.TYPE = 'SOLID'
            self.MATL = mat
            self.SECT = sect # Solid elements don't use section properties
            self.NODE = nodes
            self._GROUP = group
            _ADD(self)

    
#-----------------------------------------------Stiffness Scale Factor------------------------------

    class StiffnessScaleFactor:
    
        data = []
        
        def __init__(self, 
                    element_id,
                    area_sf: float = 1.0,
                    asy_sf: float = 1.0,
                    asz_sf: float = 1.0,
                    ixx_sf: float = 1.0,
                    iyy_sf: float = 1.0,
                    izz_sf: float = 1.0,
                    wgt_sf: float = 1.0,
                    group: str = "",
                    id: int = None):
            """
                element_id: Element ID(s) where scale factor is applied (can be int or list)
                area_sf: Cross-sectional area scale factor
                asy_sf: Effective Shear Area scale factor (y-axis)
                asz_sf: Effective Shear Area scale factor (z-axis)
                ixx_sf: Torsional Resistance scale factor (x-axis)
                iyy_sf: Area Moment of Inertia scale factor (y-axis)
                izz_sf: Area Moment of Inertia scale factor (z-axis)
                wgt_sf: Weight scale factor
                group: Group name (default "")
                id: Scale factor ID (optional, auto-assigned if None)
            
            Examples:
                StiffnessScaleFactor(908, area_sf=0.5, asy_sf=0.6, asz_sf=0.7, 
                                ixx_sf=0.8, iyy_sf=0.8, izz_sf=0.9, wgt_sf=0.95)
                
            """
            
            # Check if group exists, create if not
            if group != "":
                chk = 0
                a = [v['NAME'] for v in Group.Boundary.json()["Assign"].values()]
                if group in a:
                    chk = 1
                if chk == 0:
                    Group.Boundary(group)
            
            # Handle element_id as single int or list
            if isinstance(element_id, (list, tuple)):
                self.ELEMENT_IDS = list(element_id)
            else:
                self.ELEMENT_IDS = [element_id]
            
            self.AREA_SF = area_sf
            self.ASY_SF = asy_sf
            self.ASZ_SF = asz_sf
            self.IXX_SF = ixx_sf
            self.IYY_SF = iyy_sf
            self.IZZ_SF = izz_sf
            self.WGT_SF = wgt_sf
            self.GROUP_NAME = group
            
            # Auto-assign ID if not provided
            if id is None:
                self.ID = len(Element.StiffnessScaleFactor.data) + 1
            else:
                self.ID = id
            
            # Add to static list
            Element.StiffnessScaleFactor.data.append(self)
        
        @classmethod
        def json(cls):
            """
            Converts StiffnessScaleFactor data to JSON format
            """
            json_data = {"Assign": {}}
            
            for scale_factor in cls.data:
                # Create scale factor item
                scale_factor_item = {
                    "ID": scale_factor.ID,
                    "AREA_SF": scale_factor.AREA_SF,
                    "ASY_SF": scale_factor.ASY_SF,
                    "ASZ_SF": scale_factor.ASZ_SF,
                    "IXX_SF": scale_factor.IXX_SF,
                    "IYY_SF": scale_factor.IYY_SF,
                    "IZZ_SF": scale_factor.IZZ_SF,
                    "WGT_SF": scale_factor.WGT_SF,
                    "GROUP_NAME": scale_factor.GROUP_NAME
                }
                
                # Assign to each element ID
                for element_id in scale_factor.ELEMENT_IDS:
                    if str(element_id) not in json_data["Assign"]:
                        json_data["Assign"][str(element_id)] = {"ITEMS": []}
                    
                    json_data["Assign"][str(element_id)]["ITEMS"].append(scale_factor_item)
            
            return json_data
        
        @classmethod
        def create(cls):
            """
            Sends all StiffnessScaleFactor data to the API
            """
            MidasAPI("PUT", "/db/essf", cls.json())
        
        @classmethod
        def get(cls):
            """
            Retrieves StiffnessScaleFactor data from the API
            """
            return MidasAPI("GET", "/db/essf")
        
        @classmethod
        def sync(cls):
            """
            Updates the StiffnessScaleFactor class with data from the API
            """
            cls.data = []
            response = cls.get()
            
            if response != {'message': ''}:
                processed_ids = set()  # To avoid duplicate processing
                
                for element_data in response.get("ESSF", {}).items():
                    for item in element_data.get("ITEMS", []):
                        scale_factor_id = item.get("ID", 1)
                        
                        # Skip if already processed (for multi-element scale factors)
                        if scale_factor_id in processed_ids:
                            continue
                        
                        # Find all elements with the same scale factor ID
                        element_ids = []
                        for eid, edata in response.get("ESSF", {}).items():
                            for eitem in edata.get("ITEMS", []):
                                if eitem.get("ID") == scale_factor_id:
                                    element_ids.append(int(eid))
                        
                        # Create StiffnessScaleFactor object
                        Element.StiffnessScaleFactor(
                            element_id=element_ids if len(element_ids) > 1 else element_ids[0],
                            area_sf=item.get("AREA_SF", 1.0),
                            asy_sf=item.get("ASY_SF", 1.0),
                            asz_sf=item.get("ASZ_SF", 1.0),
                            ixx_sf=item.get("IXX_SF", 1.0),
                            iyy_sf=item.get("IYY_SF", 1.0),
                            izz_sf=item.get("IZZ_SF", 1.0),
                            wgt_sf=item.get("WGT_SF", 1.0),
                            group=item.get("GROUP_NAME", ""),
                            id=scale_factor_id
                        )
                        
                        processed_ids.add(scale_factor_id)
        
        @classmethod
        def delete(cls):
            """
            Deletes all stiffness scale factors from the database and resets the class.
            """
            cls.data = []
            return MidasAPI("DELETE", "/db/essf")




# ---- GET ELEMENT OBJECT FROM ID ----------

def elemByID(elemID:int) -> Element:
    ''' Return Element object with the input ID '''
    for elem in Element.elements:
        if elem.ID == elemID:
            return elem
        
    print(f'There is no element with ID {elemID}')
    return None

