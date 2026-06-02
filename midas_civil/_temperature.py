from ._mapi import MidasAPI
# from ._node import *
from ._group import Group
from ._load import Load_Case
from typing import Literal

#type hints for beamsection
_BeamSectionSecType = Literal['General','PSC']
_BeamSectionType = Literal['Element','Input']
_BeamSectionDir = Literal['LY','LZ']
_BeamSectionRefPos = Literal['Centroid','Top','Bot']

#helper classes
class _System():
    def __init__(self,id,lcname,group,temperature):
        self.ID = id
        self.LCNAME = lcname
        self.TEMPER = temperature
        self.GROUP = group
class _Element():
    def __init__(self,id,lcname,group,temperature,element):
        self.ID = id
        self.ELEMENT = element
        self.LCNAME = lcname
        self.TEMP = temperature
        self.GROUP_NAME = group    
class _Gradient():
    def __init__(self,id,element):
        self.ID = id
        self.ELEMENT = element
class _Nodal():
    def __init__(self,id,node,temperature,lcname,group,items):
        self.ID = id
        self.NODE = node
        self.TEMPER = temperature
        self.LCNAME = lcname
        self.GROUP_NAME = group
        self.ITEMS = items
class _BeamSection():
    def __init__(self,element,id,items):
        self.ID = id
        self.ELEMENT = element
        self.ITEMS = items
        
def convList(item):
    if type(item) != list:
        return [item]
    else:
        return item
    
class Temperature:

    @classmethod
    def create(cls):
        """Creates Temperature elements in MIDAS Civil NX"""
        if cls.System.temps: cls.System.create()
        if cls.Element.temps: cls.Element.create()
        if cls.Gradient.temps: cls.Gradient.create()
        if cls.Nodal.temps: cls.Nodal.create()
        if cls.BeamSection.temps: cls.BeamSection.create()        

    @classmethod
    def delete(cls):
        """Deletes Temperature elements from MIDAS Civil NX and Python"""
        cls.System.delete()
        cls.Element.delete()
        cls.Gradient.delete()
        cls.Nodal.delete()
        cls.BeamSection.delete()
        
    @classmethod
    def clear(cls):
        """Deletes Temperature elements from MIDAS Civil NX and Python"""
        cls.System.clear()
        cls.Element.clear()
        cls.Gradient.clear()
        cls.Nodal.clear()
        cls.BeamSection.clear()

    @classmethod
    def sync(cls):
        """Sync Temperature elements from MIDAS Civil NX to Python"""
        cls.System.sync()
        cls.Element.sync()
        cls.Gradient.sync()
        cls.Nodal.sync()
        cls.BeamSection.sync()
                
    # --------------------------------------------------------------------------------------------------
    # System Temperature
    # --------------------------------------------------------------------------------------------------
    class System:
        """
        Create System Temperature Object in Python
        
        Parameters:
            temperature (float): Temperature value
            lcname (str): Load case name
            group (str): Load group name (default "")
            id (int): System ID (optional)
        
        Example:
            Temperature.System(12.5, "Temp(+)", "LoadGroup1", 1)
        """
        temps:list[_System] = []
        
        def __init__(self, temperature, lcname, group="", id=None):
            chk = 0
            for i in Load_Case.cases:
                if lcname in i.NAME: chk = 1
            if chk == 0: Load_Case("T", lcname)

            if group:
                chk = 0
                try:
                    a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                    if group in a:
                        chk = 1
                except:
                    pass
                if chk == 0:
                    Group.Load(group)
            
            self.TEMPER = temperature
            self.LCNAME = lcname
            self.GROUP_NAME = group
            
            if id is None:
                self.ID = len(Temperature.System.temps) + 1
            else:
                self.ID = id
            
            Temperature.System.temps.append(self)

        @classmethod
        def json(cls):
            """Creates JSON from System Temperature objects defined in Python"""
            json_data = {"Assign": {}}
            for temp in cls.temps:
                json_data["Assign"][str(temp.ID)] = {
                    "TEMPER": temp.TEMPER,
                    "LCNAME": temp.LCNAME,
                    "GROUP_NAME": temp.GROUP_NAME
                }
            return json_data

        @staticmethod
        def create():
            """Creates System Temperatures in MIDAS Civil NX"""
            MidasAPI("PUT", "/db/stmp", Temperature.System.json())

        @staticmethod
        def get():
            """Get the JSON of System Temperatures from MIDAS Civil NX"""
            return MidasAPI("GET", "/db/stmp")

        @staticmethod
        def sync():
            """Sync System Temperatures from MIDAS Civil NX to Python"""
            Temperature.System.temps = []
            a = Temperature.System.get()
            
            if a and 'STMP' in a:
                temp_data = a.get('STMP', {})
                for temp_id, temp_info in temp_data.items():
                    Temperature.System(
                        temp_info.get('TEMPER', 0),
                        temp_info.get('LCNAME', ''),
                        temp_info.get('GROUP_NAME', ''),
                        int(temp_id)
                    )

        @staticmethod
        def delete():
            """Delete System Temperatures from MIDAS Civil NX and Python"""
            Temperature.System.clear()
            return MidasAPI("DELETE", "/db/stmp")

        @staticmethod
        def clear():
            """Delete System Temperatures from Python"""
            Temperature.System.temps = []

    # --------------------------------------------------------------------------------------------------
    # Element Temperature
    # --------------------------------------------------------------------------------------------------
    class Element:
        """
        Create Element Temperature Object in Python
        
        Parameters:
            element (int | list): Element ID or list of Element IDs
            temperature (float): Temperature value
            lcname (str): Load case name
            group (str): Load group name (default "")
            id (int): Temperature ID (optional)
        
        Example:
            Temperature.Element([1, 2, 3], 35, "Temp(+)", "", 1)
        """
        temps:list[_Element] = []
        
        def __init__(self, element, temperature, lcname, group="", id=None):

            chk = 0
            for i in Load_Case.cases:
                if lcname in i.NAME: chk = 1
            if chk == 0: Load_Case("T", lcname)

            if group:
                chk = 0
                try:
                    a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                    if group in a:
                        chk = 1
                except:
                    pass
                if chk == 0:
                    Group.Load(group)
            
            elements = convList(element)
            if not elements:
                return
            
            for i, el in enumerate(elements):
                if id is None:
                    existing_ids = []
                    for temp in Temperature.Element.temps:
                        if temp.ELEMENT == el:
                            existing_ids.extend([item.get('ID', 0) for item in temp.ITEMS if hasattr(temp, 'ITEMS')])
                    current_id = max(existing_ids, default=0) + 1
                else:
                    current_id = id
                
                item_data = {
                    "ID": current_id, "LCNAME": lcname,
                    "GROUP_NAME": group, "TEMP": temperature
                }

                existing_temp = None
                for temp in Temperature.Element.temps:
                    if temp.ELEMENT == el:
                        existing_temp = temp
                        break
                
                if existing_temp:
                    if not hasattr(existing_temp, 'ITEMS'):
                        existing_temp.ITEMS = []
                    existing_temp.ITEMS.append(item_data)
                    
                    if i == 0:
                        self.ELEMENT = el
                        self.TEMP = temperature
                        self.LCNAME = lcname
                        self.GROUP_NAME = group
                        self.ID = current_id
                        self.ITEMS = existing_temp.ITEMS
                else:
                    if i == 0:
                        self.ELEMENT = el
                        self.TEMP = temperature
                        self.LCNAME = lcname
                        self.GROUP_NAME = group
                        self.ID = current_id
                        self.ITEMS = [item_data]
                        Temperature.Element.temps.append(self)
                    else:
                        obj = self.__class__.__new__(self.__class__)
                        obj.ELEMENT = el
                        obj.TEMP = temperature
                        obj.LCNAME = lcname
                        obj.GROUP_NAME = group
                        obj.ID = current_id
                        obj.ITEMS = [item_data]
                        Temperature.Element.temps.append(obj)

        @classmethod
        def json(cls):
            """Creates JSON from Element Temperature objects defined in Python"""
            json_data = {"Assign": {}}
            for temp in cls.temps:
                json_data["Assign"][str(temp.ELEMENT)] = {"ITEMS": temp.ITEMS}
            return json_data

        @staticmethod
        def create():
            """Creates Element Temperatures in MIDAS Civil NX"""
            MidasAPI("PUT", "/db/etmp", Temperature.Element.json())

        @staticmethod
        def get():
            """Get the JSON of Element Temperatures from MIDAS Civil NX"""
            return MidasAPI("GET", "/db/etmp")

        @staticmethod
        def sync():
            """Sync Element Temperatures from MIDAS Civil NX to Python"""
            Temperature.Element.temps = []
            a = Temperature.Element.get()
            
            if a and 'ETMP' in a:
                temp_data = a.get('ETMP', {})
                for element_id, element_data in temp_data.items():
                    element_obj = type('obj', (object,), {
                        'ELEMENT': int(element_id),
                        'ITEMS': element_data.get('ITEMS', [])
                    })()
                    Temperature.Element.temps.append(element_obj)

        @staticmethod
        def delete():
            """Delete Element Temperatures from MIDAS Civil NX and Python"""
            Temperature.Element.clear()
            return MidasAPI("DELETE", "/db/etmp")
        
        @staticmethod
        def clear():
            """Delete Element Temperatures from MIDAS Civil NX and Python"""
            Temperature.Element.temps = []

    # --------------------------------------------------------------------------------------------------
    # Temperature Gradient
    # --------------------------------------------------------------------------------------------------
    class Gradient:
        """
        Create Temperature Gradient Object in Python for Beam and Plate elements.
        
        Parameters:
            element (int | list): Element ID or list of Element IDs to apply the gradient.
            type (str): Element type, either 'Beam' or 'Plate'.
            lcname (str): Load Case Name (must exist in the model).
            tz (float): Temperature difference in the local z-direction (T2z - T1z).
            group (str, optional): Load Group Name. Defaults to "".
            id (int, optional): Gradient ID. Auto-assigned if not provided.
            hz (float, optional): Gradient value for local z-dir. If omitted, section default is used.
            ty (float, optional): Temp. diff. in local y-dir (T2y - T1y). **Required for 'Beam' type.**
            hy (float, optional): Gradient value for local y-dir. If omitted, section default is used.
        
        Example for Beam (providing gradient values):
            Temperature.Gradient(element=[2, 3], type='Beam', lcname='Temp(-)', tz=10, ty=-10, hz=1.2, hy=0.5)
        
        Example for Beam (using section defaults):
            Temperature.Gradient(element=2, type='Beam', lcname='Temp(+)', tz=10, ty=-10)
        
        Example for Plate (providing gradient value):
            Temperature.Gradient(element=21, type='Plate', lcname='Temp(-)', tz=10, hz=0.2)
        """
        temps:list[_Gradient] = []

        def __init__(self, element, type, lcname, tz, group="", hz=None, ty=0, hy=None,id=None):

            chk = 0
            for i in Load_Case.cases:
                if lcname in i.NAME: chk = 1
            if chk == 0: Load_Case("T", lcname)
            
            if group:
                chk = 0
                try:
                    a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                    if group in a:
                        chk = 1
                except:
                    pass
                if chk == 0:
                    Group.Load(group)
            
            use_hz = (hz is None)
            use_hy = (hy is None)

            elements = convList(element)
            if not elements:
                return

            for i, el in enumerate(elements):
                if id is None:
                    existing_ids = []
                    for temp in Temperature.Gradient.temps:
                        if temp.ELEMENT == el:
                            existing_ids.extend([item.get('ID', 0) for item in temp.ITEMS if hasattr(temp, 'ITEMS')])
                    current_id = max(existing_ids, default=0) + 1
                else:
                    current_id = id

                item_data = {
                    "ID": current_id,
                    "LCNAME": lcname,
                    "GROUP_NAME": group,
                    "TZ": tz,
                    "USE_HZ": use_hz,
                }

                if not use_hz:
                    item_data["HZ"] = hz

                if type.lower() == 'beam':
                    item_data["TYPE"] = 1
                    item_data["TY"] = ty
                    item_data["USE_HY"] = use_hy
                    if not use_hy:
                        item_data["HY"] = hy
                elif type.lower() == 'plate':
                    item_data["TYPE"] = 2
                else:
                    raise ValueError("Element type for Gradient must be 'Beam' or 'Plate'.")

                existing_temp = None
                for temp in Temperature.Gradient.temps:
                    if temp.ELEMENT == el:
                        existing_temp = temp
                        break

                if existing_temp:
                    if not hasattr(existing_temp, 'ITEMS'):
                        existing_temp.ITEMS = []
                    existing_temp.ITEMS.append(item_data)
                    
                    if i == 0:
                        self.ELEMENT = el
                        self.ID = current_id
                        self.ITEMS = existing_temp.ITEMS
                else:
                    if i == 0:
                        self.ELEMENT = el
                        self.ID = current_id
                        self.ITEMS = [item_data]
                        Temperature.Gradient.temps.append(self)
                    else:
                        obj = self.__class__.__new__(self.__class__)
                        obj.ELEMENT = el
                        obj.ID = current_id
                        obj.ITEMS = [item_data]
                        Temperature.Gradient.temps.append(obj)
        
        @classmethod
        def json(cls):
            """Creates JSON from Temperature Gradient objects defined in Python"""
            json_data = {"Assign": {}}
            for temp in cls.temps:
                json_data["Assign"][str(temp.ELEMENT)] = {"ITEMS": temp.ITEMS}
            return json_data

        @staticmethod
        def create():
            """Creates Temperature Gradients in MIDAS Civil NX"""
            MidasAPI("PUT", "/db/gtmp", Temperature.Gradient.json())

        @staticmethod
        def get():
            """Get the JSON of Temperature Gradients from MIDAS Civil NX"""
            return MidasAPI("GET", "/db/gtmp")

        @staticmethod
        def sync():
            """Sync Temperature Gradients from MIDAS Civil NX to Python"""
            Temperature.Gradient.temps = []
            a = Temperature.Gradient.get()
            
            if a and 'GTMP' in a:
                temp_data = a.get('GTMP', {})
                for element_id, element_data in temp_data.items():
                    element_obj = type('obj', (object,), {
                        'ELEMENT': int(element_id),
                        'ITEMS': element_data.get('ITEMS', [])
                    })()
                    Temperature.Gradient.temps.append(element_obj)

        @staticmethod
        def delete():
            """Delete Temperature Gradients from MIDAS Civil NX and Python"""
            Temperature.Gradient.clear()
            return MidasAPI("DELETE", "/db/gtmp")
        
        @staticmethod
        def clear():
            """Delete Temperature Gradients from MIDAS Civil NX and Python"""
            Temperature.Gradient.temps = []

    # --------------------------------------------------------------------------------------------------
    # Nodal Temperature
    # --------------------------------------------------------------------------------------------------
    class Nodal:
        """
        Create Nodal Temperature  
        
        Parameters:
            node (int | list): Node ID or list of Node IDs
            temperature (float): Temperature value  
            lcname (str): Load case name **(Must exist in the model)**
            group (str): Load group name (default "")
            id (int): Temperature ID (optional)
        
        Example:
            Temperature.Nodal([6, 7], 10, "Test")
        """
        temps:list[_Nodal] = []
        
        def __init__(self, node, temperature, lcname, group="", id=None):

            chk = 0
            for i in Load_Case.cases:
                if lcname in i.NAME: chk = 1
            if chk == 0: Load_Case("T", lcname)

            if group:
                chk = 0
                try:
                    a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                    if group in a:
                        chk = 1
                except:
                    pass
                if chk == 0:
                    Group.Load(group)
            
            nodes = convList(node)
            if not nodes:
                return
            
            for i, nd in enumerate(nodes):
                if id is None:
                    existing_ids = []
                    for temp in Temperature.Nodal.temps:
                        if temp.NODE == nd:
                            existing_ids.extend([item.get('ID', 0) for item in temp.ITEMS if hasattr(temp, 'ITEMS')])
                    current_id = max(existing_ids, default=0) + 1
                else:
                    current_id = id
                
                item_data = {
                    "ID": current_id, "LCNAME": lcname,
                    "GROUP_NAME": group, "TEMPER": temperature
                }

                existing_temp = None
                for temp in Temperature.Nodal.temps:
                    if temp.NODE == nd:
                        existing_temp = temp
                        break
                
                if existing_temp:
                    if not hasattr(existing_temp, 'ITEMS'):
                        existing_temp.ITEMS = []
                    existing_temp.ITEMS.append(item_data)
                    
                    if i == 0:
                        self.NODE = nd
                        self.TEMPER = temperature
                        self.LCNAME = lcname
                        self.GROUP_NAME = group
                        self.ID = current_id
                        self.ITEMS = existing_temp.ITEMS
                else:
                    if i == 0:
                        self.NODE = nd
                        self.TEMPER = temperature
                        self.LCNAME = lcname
                        self.GROUP_NAME = group
                        self.ID = current_id
                        self.ITEMS = [item_data]
                        Temperature.Nodal.temps.append(self)
                    else:
                        obj = self.__class__.__new__(self.__class__)
                        obj.NODE = nd
                        obj.TEMPER = temperature
                        obj.LCNAME = lcname
                        obj.GROUP_NAME = group
                        obj.ID = current_id
                        obj.ITEMS = [item_data]
                        Temperature.Nodal.temps.append(obj)

        @classmethod
        def json(cls):
            """Creates JSON with 'Assign' key from Nodal Temperature objects defined in Python"""
            json_data = {"Assign": {}}
            for temp in cls.temps:
                json_data["Assign"][str(temp.NODE)] = {"ITEMS": temp.ITEMS}
            return json_data

        @staticmethod
        def create():
            """Creates Nodal Temperatures in MIDAS Civil NX"""
            MidasAPI("PUT", "/db/ntmp", Temperature.Nodal.json())

        @staticmethod
        def get():
            """Get the JSON of Nodal Temperatures from MIDAS Civil NX"""
            return MidasAPI("GET", "/db/ntmp")

        @staticmethod
        def sync():
            """Sync Nodal Temperatures from MIDAS Civil NX to Python"""
            Temperature.Nodal.temps = []
            a = Temperature.Nodal.get()
            
            if a and 'NTMP' in a:
                temp_data = a.get('NTMP', {})
                for node_id, node_data in temp_data.items():
                    node_obj = type('obj', (object,), {
                        'NODE': int(node_id),
                        'ITEMS': node_data.get('ITEMS', [])
                    })()
                    Temperature.Nodal.temps.append(node_obj)

        @staticmethod
        def delete():
            """Delete Nodal Temperatures from MIDAS Civil NX and Python"""
            Temperature.Nodal.clear()
            return MidasAPI("DELETE", "/db/ntmp")
        
        @staticmethod
        def clear():
            """Delete Nodal Temperatures from MIDAS Civil NX and Python"""
            Temperature.Nodal.temps = []


    # --------------------------------------------------------------------------------------------------
    # Beam Section Temperature
    # --------------------------------------------------------------------------------------------------
    class BeamSection:
        """
        Create Beam Section Temperature Object in Python.

        Parameters:
            element (int | list): Single Element ID or list of Element IDs.
            lcname       (str)  : Load Case Name.
            section_type (str)  : 'General' or 'PSC'. Default 'General'.
            type         (str)  : 'Element' or 'Input'. Default 'Element'.
            group        (str)  : Load Group Name.
            dir          (str)  : 'LY' or 'LZ'. Default 'LZ'.
            ref_pos      (str)  : 'Centroid', 'Top', or 'Bot'. 
            b_value      (float): The `val_b` parameter. Default 0.
            value (list of lists): [val_h1, val_h2, val_t1, val_t2] per entry.
                                   PSC: val_h1/val_h2 accept 'Z1'/'Z2'/'Z3' or numeric.
                                   Short row (3 vals): [val_h1, val_h2, val_t1] → padded.
                                   Flat single entry auto-wrapped to [[...]].
            elast        (float): Required for 'Input' type.
            thermal      (float): Required for 'Input' type.
            id           (int)  : Load ID (auto-assigned if None).

        value examples:
            General  : [[0.1, 0.2, 3.0, 12.4]]
            PSC      : [["Z1", "Z2", 17.8, 4], [0.15, 0.4, 4, 0]]
                    b_value=0 (Section), val_h1="Z1"→OPT_H1=0, val_h2="Z2"→OPT_H2=1
            PSC num  : [[0.15, 0.4, 4, 0]]
                    val_h1=0.15 (numeric) → OPT_H1=3 (Value), VAL_H1=0.15
            Short    : [[0.1, 0.2, 5.0]]  →  [val_h1=0.1, val_h2=0.2, val_t1=5.0, val_t2=0]
        """
        temps:list[_BeamSection] = []

        # ── Internal mappings ──────────────────────────────────────────────────────
        _Z_MAP      = {"Z1": 0, "Z2": 1, "Z3": 2}   # Z-string → OPT_H int
        _PSC_REF_MAP = {"TOP": 0, "BOT": 1}

        @staticmethod
        def _resolve_h(val):
            """
            Resolve val_h1 or val_h2 for PSC:
            - 'Z1'/'Z2'/'Z3'  →  (opt=0/1/2,  numeric_val=0)
            - numeric          →  (opt=3,       numeric_val=val)
            Returns (opt_int, numeric_val)
            """
            if isinstance(val, str):
                opt = Temperature.BeamSection._Z_MAP.get(val.upper())
                if opt is None:
                    raise ValueError(f"Invalid Z-string '{val}'. Use 'Z1', 'Z2', or 'Z3'.")
                return opt, 0
            else:
                return 3, val   # OPT=3 means "Value" type, pass the number directly

        @staticmethod
        def _normalize_value(value):
            """
            Normalise value input:
            - flat list  [a,b,c,...]  →  [[a,b,c,...]]
            - already list of lists   →  as-is
            """
            if value and not isinstance(value[0], (list, tuple)):
                return [value]
            return value

        @staticmethod
        def _pad_row(row, is_psc, b_value):
            """
            Allow short rows (3 values) by padding defaults:
            3-value row: [val_h1, val_h2, val_t1]       → [b_value, val_h1, val_h2, val_t1, 0]
            4-value row: [val_h1, val_h2, val_t1, val_t2]  → [b_value, val_h1, val_h2, val_t1, val_t2]
            """
            if len(row) == 3:
                # user passed [val_h1, val_h2, val_t1]
                return [b_value, row[0], row[1], row[2], 0]
            elif len(row) == 4:
                return [b_value, row[0], row[1], row[2], row[3]]
            else:
                raise ValueError(
                    f"Each value entry must have 3 or 4 elements. Got {len(row)}: {row}"
                )

        def __init__(self, element, lcname,
                    section_type:_BeamSectionSecType = 'General',
                    type:_BeamSectionType         = 'Element',
                    group        = "",
                    dir:_BeamSectionDir          = 'LZ',
                    ref_pos:_BeamSectionRefPos      = 'Centroid',
                    b_value      = 0,
                    value        = None,
                    elast        = None,
                    thermal      = None,
                    id           = None):

            # ── Defaults ──────────────────────────────────────────────────────────
            if value is None:
                value = [[0, 0, 0, 0]]

            # ── Normalise & pad ───────────────────────────────────────────────────
            is_psc   = section_type.lower() == 'psc'
            value    = self._normalize_value(value)
            value    = [self._pad_row(row, is_psc, b_value) for row in value]

            # ── Validate Input type ───────────────────────────────────────────────
            if type.upper() == 'INPUT':
                if elast is None or thermal is None:
                    raise ValueError(
                        "For 'Input' type, both 'elast' and 'thermal' must be provided."
                    )

            # ── Map ref_pos string → int for PSC ──────────────────────────────────
            psc_ref_int = self._PSC_REF_MAP.get(str(ref_pos).upper(), 0)

            # ── Load Case ─────────────────────────────────────────────────────────
            chk = 0
            for i in Load_Case.cases:
                if lcname in i.NAME:
                    chk = 1
            if chk == 0:
                Load_Case("T", lcname)

            # ── Load Group ────────────────────────────────────────────────────────
            if group:
                chk = 0
                try:
                    a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                    if group in a:
                        chk = 1
                except:
                    pass
                if chk == 0:
                    Group.Load(group)

            # ── Build vSECTTMP list ───────────────────────────────────────────────
            vsect_tmp_list = []

            for row in value:
                val_b, val_h1, val_h2, val_t1, val_t2 = row

                vsec_item = {"TYPE": type.upper()}

                # ELAST / THERMAL — always include when provided (even for ELEMENT type)
                if elast is not None:
                    vsec_item["ELAST"]   = elast
                if thermal is not None:
                    vsec_item["THERMAL"] = thermal

                # PSC-specific fields
                if is_psc:
                    vsec_item["REF"] = psc_ref_int

                    # val_b → OPT_B (0=Section, 1=Value)
                    vsec_item["OPT_B"]  = int(val_b)
                    vsec_item["VAL_B"]  = 0          # VAL_B always 0 when OPT_B=0(Section)

                    # val_h1 → OPT_H1 + VAL_H1
                    opt_h1, num_h1 = self._resolve_h(val_h1)
                    vsec_item["OPT_H1"] = opt_h1
                    vsec_item["VAL_H1"] = num_h1

                    # val_h2 → OPT_H2 + VAL_H2
                    opt_h2, num_h2 = self._resolve_h(val_h2)
                    vsec_item["OPT_H2"] = opt_h2
                    vsec_item["VAL_H2"] = num_h2

                    vsec_item["VAL_T1"] = val_t1
                    vsec_item["VAL_T2"] = val_t2

                else:
                    # General section — straight values
                    vsec_item["VAL_B"]  = val_b
                    vsec_item["VAL_H1"] = val_h1
                    vsec_item["VAL_H2"] = val_h2
                    vsec_item["VAL_T1"] = val_t1
                    vsec_item["VAL_T2"] = val_t2

                vsect_tmp_list.append(vsec_item)

            # ── Handle Elements (int or list) and Auto-assign ID ──────────────────
            elements = convList(element)
            
            if not elements:
                return

            for i, el in enumerate(elements):
                if id is None:
                    existing_ids = []
                    for temp in Temperature.BeamSection.temps:
                        if temp.ELEMENT == el:
                            existing_ids.extend(
                                [item.get('ID', 0) for item in temp.ITEMS
                                if hasattr(temp, 'ITEMS')]
                            )
                    current_id = max(existing_ids, default=0) + 1
                else:
                    current_id = id

                # ── Construct item dict ───────────────────────────────────────────────
                item_data = {
                    "ID":         current_id,
                    "LCNAME":     lcname,
                    "GROUP_NAME": group,
                    "DIR":        dir,
                    "REF":        ref_pos,
                    "NUM":        len(vsect_tmp_list),
                    "bPSC":       is_psc,
                    "vSECTTMP":   vsect_tmp_list
                }

                # ── Merge or create ───────────────────────────────────────────────────
                existing_temp = None
                for temp in Temperature.BeamSection.temps:
                    if temp.ELEMENT == el:
                        existing_temp = temp
                        break

                if existing_temp:
                    if not hasattr(existing_temp, 'ITEMS'):
                        existing_temp.ITEMS = []
                    existing_temp.ITEMS.append(item_data)
                    
                    if i == 0:
                        self.ELEMENT = el
                        self.ID = current_id
                        self.ITEMS = existing_temp.ITEMS
                else:
                    if i == 0:
                        # Use the current self context for the first element
                        self.ELEMENT = el
                        self.ID = current_id
                        self.ITEMS = [item_data]
                        Temperature.BeamSection.temps.append(self)
                    else:
                        # Create an identical object instance for extra elements in list
                        obj = self.__class__.__new__(self.__class__)
                        obj.ELEMENT = el
                        obj.ID = current_id
                        obj.ITEMS = [item_data]
                        Temperature.BeamSection.temps.append(obj)

        # ── Class / static methods (unchanged) ───────────────────────────────────
        @classmethod
        def json(cls):
            json_data = {"Assign": {}}
            for temp in cls.temps:
                json_data["Assign"][str(temp.ELEMENT)] = {"ITEMS": temp.ITEMS}
            return json_data

        @staticmethod
        def create():
            MidasAPI("PUT", "/db/btmp", Temperature.BeamSection.json())

        @staticmethod
        def get():
            return MidasAPI("GET", "/db/btmp")

        @staticmethod
        def sync():
            Temperature.BeamSection.temps = []
            a = Temperature.BeamSection.get()
            if a and 'BTMP' in a:
                for element_id, element_data in a['BTMP'].items():
                    obj = type('obj', (object,), {
                        'ELEMENT': int(element_id),
                        'ITEMS':   element_data.get('ITEMS', [])
                    })()
                    Temperature.BeamSection.temps.append(obj)

        @staticmethod
        def delete():
            Temperature.BeamSection.clear()
            return MidasAPI("DELETE", "/db/btmp")

        @staticmethod
        def clear():
            Temperature.BeamSection.temps = []