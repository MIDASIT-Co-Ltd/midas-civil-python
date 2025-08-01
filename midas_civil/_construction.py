from ._mapi import *

class CS:


    class STAGE:
        stages = []  

        def __init__(self, 
                    name: str,
                    duration: float = 0, 
                    s_group: str = None, 
                    s_age: float = None, 
                    s_type: str= None, 
                    b_group: str = None, 
                    b_pos: str = None, 
                    b_type: str = None,
                    l_group: str = None, 
                    l_day: str = None, 
                    l_type: str = None, 
                    id: int = None, 
                    sv_result: bool = True, 
                    sv_step: bool = False, 
                    load_in: bool = False, 
                    nl: int = 5, 
                    addstp: list = None):
            """
            Construction Stage define.
            
            Parameters:
                name: Name of Construction Stage
                duration: Duration of Construction Stage in days (default 0)
                s_group: Structure group name or list of group names (default None)
                s_age: Age of structure group in days and Redistribution value(%) win case of Deactivation (default 0)
                s_type: Structure activation type - "A" to activate, "D" to deactivate(default A)
                b_group: Boundary group name or list of group names (default None)
                b_pos: Boundary position type - "ORIGINAL" or "DEFORMED", or list (default DEFORMED)
                b_type: Boundary activation type - "A" to activate, "D" to deactivate (default A)
                l_group: Load group name or list of group names (default None)
                l_day: Load activation day - "FIRST" or "LAST" (default "FIRST")
                l_type: Load activation type - "A" to activate, "D" to deactivate (default A)
                id: The construction stage ID (optional)
                sv_result: Save results of this stage (default True)
                sv_step: Add additional step results (default False)
                load_in: Load incremental steps for material nonlinear analysis (default False)
                nl: Number of load incremental steps (default 5)
                addstp: List of additional steps (default None)
            
            Examples:
                ```python
                # Single group activation
                CS("CS1", 7, "S1", 7, "A", "B1", "DEFORMED", "A", "L1", "FIRST", "A")
                
                # Multiple group activation
                CS("CS1", 7, ["S1", "S2"], [7, 10], ["A", "A"], ["B1", "B2"], 
                ["DEFORMED", "DEFORMED"], ["A", "A"], ["L1", "L2"], ["FIRST", "FIRST"], ["A", "A"])
                
                # Mixed activation and deactivation
                CS("CS1", 7, ["S1", "S2"], [7, 10], ["A", "D"], ["B1", "B2"], 
                ["DEFORMED", "DEFORMED"], ["A", "D"], "L1", "FIRST", "A")
                
                # With additional options
                CS("CS1", 7, "S1", 7, "A", "B1", "DEFORMED", "A", "L1", "FIRST", "A",
                sv_result=True, sv_step=True, load_in=True, nl=6, addstp=[1, 2, 3])
                ```
            """

            self.NAME = name
            self.DURATION = duration
            self.SV_Result = sv_result
            self.SV_Step = sv_step
            self.Load_IN = load_in
            self.NL = nl
            self.addstp = [] if addstp is None else addstp
            
            # Initialize group containers
            self.act_structure_groups = []  
            self.deact_structure_groups = []  
            self.act_boundary_groups = []  
            self.deact_boundary_groups = []  
            self.act_load_groups = []  
            self.deact_load_groups = []  
            

            # Set ID
            if id is None:
                self.ID = len(CS.STAGE.stages) + 1
            else:
                self.ID = id
            

            # Process structure groups
            if s_group:
                # Convert single values to lists for uniform processing
                if not isinstance(s_group, list):
                    s_group = [s_group]
                    s_age = [s_age if s_age is not None else 0]
                    s_type = [s_type if s_type is not None else "A"]
                else:
                    # Ensure other parameters are lists too
                    if s_age is None:
                        s_age = [0] * len(s_group)
                    elif not isinstance(s_age, list):
                        s_age = [s_age] * len(s_group)
                    
                    if s_type is None:
                        s_type = ["A"] * len(s_group)
                    elif not isinstance(s_type, list):
                        s_type = [s_type] * len(s_group)
                
                # Process each structure group
                for i, group in enumerate(s_group):
                    if i < len(s_type) and s_type[i] == "A":
                        # Activation: Check if already activated in previous stages
                        for stage in CS.STAGE.stages:
                            for existing_group in stage.act_structure_groups:
                                if existing_group["name"] == group:
                                    raise ValueError(f"Structure group '{group}' has already been activated in stage '{stage.NAME}' (ID: {stage.ID})")
                        
                        age = s_age[i] if i < len(s_age) else 0
                        self.act_structure_groups.append({"name": group, "age": age})
                    else:
                        # Deactivation: Check if activated in previous stages
                        activated = False
                        for stage in CS.STAGE.stages:
                            for existing_group in stage.act_structure_groups:
                                if existing_group["name"] == group:
                                    activated = True
                                    break
                            if activated:
                                break
                        
                        if not activated:
                            raise ValueError(f"Structure group '{group}' cannot be deactivated as it has not been activated in any previous stage")
                        
                        # For deactivation, s_age value is used as redist percentage
                        redist = s_age[i] if i < len(s_age) else 100
                        self.deact_structure_groups.append({"name": group, "redist": redist})
            
            # Process boundary groups
            if b_group:
                # Convert single values to lists for uniform processing
                if not isinstance(b_group, list):
                    b_group = [b_group]
                    b_pos = [b_pos if b_pos is not None else "DEFORMED"]
                    b_type = [b_type if b_type is not None else "A"]
                else:
                    # Ensure other parameters are lists too
                    if b_pos is None:
                        b_pos = ["DEFORMED"] * len(b_group)
                    elif not isinstance(b_pos, list):
                        b_pos = [b_pos] * len(b_group)
                    
                    if b_type is None:
                        b_type = ["A"] * len(b_group)
                    elif not isinstance(b_type, list):
                        b_type = [b_type] * len(b_group)
                
                # Process each boundary group
                for i, group in enumerate(b_group):
                    if i < len(b_type) and b_type[i] == "A":
                        # Activation: Check if already activated in previous stages
                        for stage in CS.STAGE.stages:
                            for existing_group in stage.act_boundary_groups:
                                if existing_group["name"] == group:
                                    raise ValueError(f"Boundary group '{group}' has already been activated in stage '{stage.NAME}' (ID: {stage.ID})")
                        
                        pos = b_pos[i] if i < len(b_pos) else "DEFORMED"
                        self.act_boundary_groups.append({"name": group, "pos": pos})
                    else:
                        # Deactivation: Check if activated in previous stages
                        activated = False
                        for stage in CS.STAGE.stages:
                            for existing_group in stage.act_boundary_groups:
                                if existing_group["name"] == group:
                                    activated = True
                                    break
                            if activated:
                                break
                        
                        if not activated:
                            raise ValueError(f"Boundary group '{group}' cannot be deactivated as it has not been activated in any previous stage")
                        
                        self.deact_boundary_groups.append(group)
            
            # Process load groups
            if l_group:
                # Convert single values to lists for uniform processing
                if not isinstance(l_group, list):
                    l_group = [l_group]
                    l_day = [l_day if l_day is not None else "FIRST"]
                    l_type = [l_type if l_type is not None else "A"]
                else:
                    # Ensure other parameters are lists too
                    if l_day is None:
                        l_day = ["FIRST"] * len(l_group)
                    elif not isinstance(l_day, list):
                        l_day = [l_day] * len(l_group)
                    
                    if l_type is None:
                        l_type = ["A"] * len(l_group)
                    elif not isinstance(l_type, list):
                        l_type = [l_type] * len(l_group)
                
                # Process each load group
                for i, group in enumerate(l_group):
                    if i < len(l_type) and l_type[i] == "A":
                        # Activation: Check if already activated in previous stages
                        for stage in CS.STAGE.stages:
                            for existing_group in stage.act_load_groups:
                                if existing_group["name"] == group:
                                    raise ValueError(f"Load group '{group}' has already been activated in stage '{stage.NAME}' (ID: {stage.ID})")
                        
                        day = l_day[i] if i < len(l_day) else "FIRST"
                        self.act_load_groups.append({"name": group, "day": day})
                    else:
                        # Deactivation: Check if activated in previous stages
                        activated = False
                        for stage in CS.STAGE.stages:
                            for existing_group in stage.act_load_groups:
                                if existing_group["name"] == group:
                                    activated = True
                                    break
                            if activated:
                                break
                        
                        if not activated:
                            raise ValueError(f"Load group '{group}' cannot be deactivated as it has not been activated in any previous stage")
                        
                        day = l_day[i] if i < len(l_day) else "FIRST"
                        self.deact_load_groups.append({"name": group, "day": day})
            
            CS.STAGE.stages.append(self)
        
        @classmethod
        def json(cls):
            """
            Converts Construction Stage data to JSON format 
            Example:
                # Get the JSON data for all construction stages
                json_data = CS.json()
                print(json_data)
            """
            json = {"Assign": {}}
            
            for csa in cls.stages:
                stage_data = {
                    "NAME": csa.NAME,
                    "DURATION": csa.DURATION,
                    "bSV_RSLT": csa.SV_Result,
                    "bSV_STEP": csa.SV_Step,
                    "bLOAD_STEP": csa.Load_IN
                }
                
                # Add incremental steps if load step is enabled
                if csa.Load_IN:
                    stage_data["INCRE_STEP"] = csa.NL
                
                # Add additional steps if specified
                if csa.addstp:
                    stage_data["ADD_STEP"] = csa.addstp
                else:
                    stage_data["ADD_STEP"] = []
                
                # Handle structure group activation
                if csa.act_structure_groups:
                    stage_data["ACT_ELEM"] = []
                    for group in csa.act_structure_groups:
                        stage_data["ACT_ELEM"].append({
                            "GRUP_NAME": group["name"],
                            "AGE": group["age"]
                        })
                
                # Handle structure group deactivation
                if csa.deact_structure_groups:
                    stage_data["DACT_ELEM"] = []
                    for group in csa.deact_structure_groups:
                        stage_data["DACT_ELEM"].append({
                            "GRUP_NAME": group["name"],
                            "REDIST": group["redist"]
                        })
                
                # Handle boundary group activation
                if csa.act_boundary_groups:
                    stage_data["ACT_BNGR"] = []
                    for group in csa.act_boundary_groups:
                        stage_data["ACT_BNGR"].append({
                            "BNGR_NAME": group["name"],
                            "POS": group["pos"]
                        })
                
                # Handle boundary group deactivation
                if csa.deact_boundary_groups:
                    stage_data["DACT_BNGR"] = []
                    for group_name in csa.deact_boundary_groups:
                        stage_data["DACT_BNGR"].append(group_name)
                
                # Handle load group activation
                if csa.act_load_groups:
                    stage_data["ACT_LOAD"] = []
                    for group in csa.act_load_groups:
                        stage_data["ACT_LOAD"].append({
                            "LOAD_NAME": group["name"],
                            "DAY": group["day"]
                        })
                
                # Handle load group deactivation
                if csa.deact_load_groups:
                    stage_data["DACT_LOAD"] = []
                    for group in csa.deact_load_groups:
                        stage_data["DACT_LOAD"].append({
                            "LOAD_NAME": group["name"],
                            "DAY": group["day"]
                        })
                
                json["Assign"][str(csa.ID)] = stage_data
            
            return json
        
        @classmethod
        def create(cls):
            """Creates construction stages in the database"""
            MidasAPI("PUT", "/db/stag", cls.json())
        
        @classmethod
        def get(cls):
            """Gets construction stage data from the database"""
            return MidasAPI("GET", "/db/stag")
        
        @classmethod
        def sync(cls):
            """Updates the CS class with data from the database"""
            cls.stages = []
            a = cls.get()
            if a != {'message': ''}:
                if "STAG" in a:
                    stag_data_dict = a["STAG"]
                else:
                    return  
                    
                for stag_id, stag_data in stag_data_dict.items():
                    # Basic stage data
                    name = stag_data.get("NAME")
                    duration = stag_data.get("DURATION")
                    sv_result = stag_data.get("bSV_RSLT")
                    sv_step = stag_data.get("bSV_STEP")
                    load_in = stag_data.get("bLOAD_STEP")
                    nl = stag_data.get("INCRE_STEP")
                    addstp = stag_data.get("ADD_STEP")
                    
                    # Create a new CS object with basic properties
                    new_cs = CS.STAGE(
                        name=name,
                        duration=duration,
                        id=int(stag_id),
                        sv_result=sv_result,
                        sv_step=sv_step,
                        load_in=load_in,
                        nl=nl,
                        addstp=addstp
                    )
                    
                    CS.STAGE.stages.pop()
                    
                    # Process activation elements
                    if "ACT_ELEM" in stag_data and stag_data["ACT_ELEM"]:
                        for elem in stag_data["ACT_ELEM"]:
                            group_name = elem.get("GRUP_NAME")
                            age = elem.get("AGE")
                            new_cs.act_structure_groups.append({"name": group_name, "age": age})
                    
                    # Process deactivation elements
                    if "DACT_ELEM" in stag_data and stag_data["DACT_ELEM"]:
                        for elem in stag_data["DACT_ELEM"]:
                            if isinstance(elem, dict):
                                group_name = elem.get("GRUP_NAME")
                                redist = elem.get("REDIST")
                            else:
                                group_name = elem
                                redist = 0
                            new_cs.deact_structure_groups.append({"name": group_name, "redist": redist})
                    
                    # Process activation boundary groups
                    if "ACT_BNGR" in stag_data and stag_data["ACT_BNGR"]:
                        for bngr in stag_data["ACT_BNGR"]:
                            group_name = bngr.get("BNGR_NAME")
                            pos = bngr.get("POS")
                            new_cs.act_boundary_groups.append({"name": group_name, "pos": pos})
                    
                    # Process deactivation boundary groups
                    if "DACT_BNGR" in stag_data and stag_data["DACT_BNGR"]:
                        for bngr in stag_data["DACT_BNGR"]:
                            new_cs.deact_boundary_groups.append(bngr)
                    
                    # Process activation loads
                    if "ACT_LOAD" in stag_data and stag_data["ACT_LOAD"]:
                        for load in stag_data["ACT_LOAD"]:
                            group_name = load.get("LOAD_NAME")
                            day = load.get("DAY")
                            new_cs.act_load_groups.append({"name": group_name, "day": day})
                    
                    # Process deactivation loads
                    if "DACT_LOAD" in stag_data and stag_data["DACT_LOAD"]:
                        for load in stag_data["DACT_LOAD"]:
                            if isinstance(load, dict):
                                group_name = load.get("LOAD_NAME")
                                day = load.get("DAY")
                            else:
                                group_name = load
                                day = "FIRST"
                            new_cs.deact_load_groups.append({"name": group_name, "day": day})
                    
                    CS.STAGE.stages.append(new_cs)
        
        @classmethod
        def delete(cls):
            """Deletes all construction stages from the database and resets the class"""
            cls.stages = []
            return MidasAPI("DELETE", "/db/stag")
        
#-----------------------------------------------------------Comp Section for CS--------------------------------------------------------------

    class CompSec:
        compsecs = []

        def __init__(self, 
                    activation_stage: str,
                    section_id: int,
                    comp_type: str = "GENERAL",
                    tapered_type: bool = False,
                    partinfo: list = None,
                    id: int = None):
            """
            Parameters:
                activation_stage: Active Stage name (required)
                section_id: Section ID (required)
                comp_type: Composite Type - "GENERAL" or "USER" (default "GENERAL")
                tapered_type: Tapered Type - True or False (default False)
                partinfo: List of part information lists (required)
                id: The composite section ID (optional)
            
            Part Info Format:
                Each part should be a list with elements in order:
                [part_number, material_type, material_id, composite_stage, age, 
                 height, volume_surface_ratio, module_exposed_surface, area, 
                 asy, asz, ixx, iyy, izz, warea, iw]
                
                - part_number: Integer (required)
                - material_type: "ELEM" or "MATL" (required)
                - material_id: String (optional, blank for ELEM)
                - composite_stage: String (optional, blank for active stage)
                - age: Number (default 0)
                - height: Number (default AUTO)
                - volume_surface_ratio: Number (default 0)
                - module_exposed_surface: Number (default 0)
                - area: Number (default 1)
                - asy: Number (default 1)
                - asz: Number (default 1)
                - ixx: Number (default 1)
                - iyy: Number (default 1)
                - izz: Number (default 1)
                - warea: Number (default 1)
                - iw: Number (default 1)
            
            Examples:
                ```python
                # Basic composite section
                CompSec("CS1", 1, "GENERAL", False, [
                    [1, "ELEM", "", "", 2, 1.5, 1.5, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [2, "MATL", "3", "CS2", 5, 0.245, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
                ])
                
                # With minimal part info (using defaults)
                CompSec("CS1", 2, "GENERAL", False, [
                    [1, "ELEM"],
                    [2, "MATL", "2","CS2"]
                ])
                ```
            """
            
            self.ASTAGE = activation_stage
            self.SEC = section_id
            self.TYPE = comp_type
            self.bTAP = tapered_type
            
            # Set ID
            if id is None:
                self.ID = len(CS.CompSec.compsecs) + 1
            else:
                self.ID = id
            
            # Process part information
            self.vPARTINFO = []
            
            if partinfo is None:
                raise ValueError("Part information is required")
            
            if not isinstance(partinfo, list):
                raise ValueError("Part information must be a list of lists")
            
            for part_data in partinfo:
                if not isinstance(part_data, list) or len(part_data) < 2:
                    raise ValueError("Each part must be a list with at least part number and material type")
                
                # Default values for part info
                defaults = [
                    None,  # PART (required)
                    None,  # MTYPE (required)
                    "",    # MAT
                    "",    # CSTAGE
                    0,     # AGE
                    "AUTO", # PARTINFO_H
                    0,     # PARTINFO_VS
                    0,     # PARTINFO_M
                    1,     # AREA
                    1,     # ASY
                    1,     # ASZ
                    1,     # IXX
                    1,     # IYY
                    1,     # IZZ
                    1,     # WAREA
                    1      # IW
                ]
                
                # Fill in provided values
                for i, value in enumerate(part_data):
                    if i < len(defaults):
                        defaults[i] = value
                
                # Validate required fields
                if defaults[0] is None:
                    raise ValueError("Part number is required")
                if defaults[1] is None:
                    raise ValueError("Material type is required")
                if defaults[1] not in ["ELEM", "MATL"]:
                    raise ValueError("Material type must be 'ELEM' or 'MATL'")
                
                # Create part info dictionary
                part_info = {
                    "PART": defaults[0],
                    "MTYPE": defaults[1],
                    "MAT": defaults[2],
                    "CSTAGE": defaults[3],
                    "AGE": defaults[4],
                    "PARTINFO_H": defaults[5],
                    "PARTINFO_VS": defaults[6],
                    "PARTINFO_M": defaults[7],
                    "AREA": defaults[8],
                    "ASY": defaults[9],
                    "ASZ": defaults[10],
                    "IXX": defaults[11],
                    "IYY": defaults[12],
                    "IZZ": defaults[13],
                    "WAREA": defaults[14],
                    "IW": defaults[15]
                }
                
                self.vPARTINFO.append(part_info)
            
            CS.CompSec.compsecs.append(self)
        
        @classmethod
        def json(cls):
            """
            Converts Composite Section data to JSON format 
            Example:
                # Get the JSON data for all composite sections
                json_data = CS.CompSec.json()
                print(json_data)
            """
            json_data = {"Assign": {}}
            
            for compsec in cls.compsecs:
                section_data = {
                    "SEC": compsec.SEC,
                    "ASTAGE": compsec.ASTAGE,
                    "TYPE": compsec.TYPE,
                    "bTAP": compsec.bTAP,
                    "vPARTINFO": compsec.vPARTINFO
                }
                
                json_data["Assign"][str(compsec.ID)] = section_data
            
            return json_data
        
        @classmethod
        def create(cls):
            """Creates composite sections in the database"""
            return MidasAPI("PUT", "/db/cscs", cls.json())
        
        @classmethod
        def get(cls):
            """Gets composite section data from the database"""
            return MidasAPI("GET", "/db/cscs")
        
        @classmethod
        def sync(cls):
            """Updates the CompSec class with data from the database"""
            cls.compsecs = []
            response = cls.get()
            
            if response != {'message': ''}:
                if "CSCS" in response:
                    cscs_data_dict = response["CSCS"]
                else:
                    return
                
                for cscs_id, cscs_data in cscs_data_dict.items():
                    # Basic section data
                    astage = cscs_data.get("ASTAGE")
                    sec = cscs_data.get("SEC")
                    comp_type = cscs_data.get("TYPE", "GENERAL")
                    tapered_type = cscs_data.get("bTAP", False)
                    partinfo_data = cscs_data.get("vPARTINFO", [])
                    
                    # Convert partinfo from dict format to list format
                    partinfo = []
                    for part in partinfo_data:
                        part_list = [
                            part.get("PART"),
                            part.get("MTYPE"),
                            part.get("MAT", ""),
                            part.get("CSTAGE", ""),
                            part.get("AGE", 0),
                            part.get("PARTINFO_H", "AUTO"),
                            part.get("PARTINFO_VS", 0),
                            part.get("PARTINFO_M", 0),
                            part.get("AREA", 1),
                            part.get("ASY", 1),
                            part.get("ASZ", 1),
                            part.get("IXX", 1),
                            part.get("IYY", 1),
                            part.get("IZZ", 1),
                            part.get("WAREA", 1),
                            part.get("IW", 1)
                        ]
                        partinfo.append(part_list)
                    
                    # Create a new CompSec object
                    new_compsec = CS.CompSec(
                        activation_stage=astage,
                        section_id=sec,
                        comp_type=comp_type,
                        tapered_type=tapered_type,
                        partinfo=partinfo,
                        id=int(cscs_id)
                    )
                    
                    # Remove the automatically added instance and replace with synced data
                    CS.CompSec.compsecs.pop()
                    CS.CompSec.compsecs.append(new_compsec)
        
        @classmethod
        def delete(cls):
            """Deletes all composite sections from the database and resets the class"""
            cls.compsecs = []
            return MidasAPI("DELETE", "/db/cscs")


#-----------------------------------------------------------------------------------------------------------------------------------

    class TimeLoad:
        timeloads = []

        def __init__(self, 
                    element_id: int,
                    day: int,
                    group: str = "",
                    id: int = None):
            """
            Time Loads for Construction Stage define.
            
            Parameters:
                element_id: Element ID (required)
                day: Time Loads in days (required)
                group: Load Group Name (optional, default blank)
                id: The time loads ID (optional)
            
            Examples:
                ```python
                CS.TimeLoad(10, 35, "DL")
                ```
            """
            
            self.ELEMENT_ID = element_id
            self.DAY = day
            self.GROUP_NAME = group
            
            # Set ID
            if id is None:
                self.ID = len(CS.TimeLoad.timeloads) + 1
            else:
                self.ID = id
            
            CS.TimeLoad.timeloads.append(self)
        
        @classmethod
        def json(cls):
            """
            Converts Time Loads data to JSON format 
            Example:
                # Get the JSON data for all time loads
                json_data = CS.TimeLoad.json()
                print(json_data)
            """
            json_data = {"Assign": {}}
            
            for timeload in cls.timeloads:
                items_data = {
                    "ITEMS": [
                        {
                            "ID": 1,
                            "GROUP_NAME": timeload.GROUP_NAME,
                            "DAY": timeload.DAY
                        }
                    ]
                }
                
                json_data["Assign"][str(timeload.ELEMENT_ID)] = items_data
            
            return json_data
        
        @classmethod
        def create(cls):
            """Creates time loads in the CIVIL NX"""
            return MidasAPI("PUT", "/db/tmld", cls.json())
        
        @classmethod
        def get(cls):
            """Gets time loads data from the CIVIL NX"""
            return MidasAPI("GET", "/db/tmld")
        
        @classmethod
        def sync(cls):
            """Updates the TimeLoad class with data from the CIVIL NX"""
            cls.timeloads = []
            response = cls.get()
            
            if response != {'message': ''}:
                if "TMLD" in response:
                    stbk_data_dict = response["TMLD"]
                else:
                    return
                
                for element_id, stbk_data in stbk_data_dict.items():
                    items = stbk_data.get("ITEMS", [])
                    
                    for item in items:
                        group_name = item.get("GROUP_NAME", "")
                        day = item.get("DAY", 0)
                        item_id = item.get("ID", 1)
                        
                        # Create a new TimeLoad object
                        new_timeload = CS.TimeLoad(
                            element_id=int(element_id),
                            day=day,
                            group=group_name,
                            id=item_id
                        )
                        
                        # Remove the automatically added instance and replace with synced data
                        CS.TimeLoad.timeloads.pop()
                        CS.TimeLoad.timeloads.append(new_timeload)
        
        @classmethod
        def delete(cls):
            """Deletes all time loads from the CIVIL NX and python class"""
            cls.timeloads = []
            return MidasAPI("DELETE", "/db/tmld")

    class CreepCoeff:
        creepcoeffs = []

        def __init__(self, 
                    element_id: int,
                    creep: float,
                    group: str = "",
                    id: int = None):
            """
            Creep Coefficient for Construction Stage define.
            
            Parameters:
                element_id: Element ID (required)
                creep: Creep Coefficient value (required)
                group: Load Group Name (optional, default blank)
                id: The creep coefficient ID (optional)
            
            Examples:
                ```python
                # Basic creep coefficient
                CS.CreepCoeff(25, 1.2)   

                # With specific ID & Group
                CS.CreepCoeff(26, 1.5, "GR", id=2)
                ```
            """
            
            self.ELEMENT_ID = element_id
            self.CREEP = creep
            self.GROUP_NAME = group
            
            # Set ID
            if id is None:
                self.ID = len(CS.CreepCoeff.creepcoeffs) + 1
            else:
                self.ID = id
            
            CS.CreepCoeff.creepcoeffs.append(self)
        
        @classmethod
        def json(cls):
            """
            Converts Creep Coefficient data to JSON format 
            Example:
                # Get the JSON data for all creep coefficients
                json_data = CS.CreepCoeff.json()
                print(json_data)
            """
            json_data = {"Assign": {}}
            
            for creepcoeff in cls.creepcoeffs:
                items_data = {
                    "ITEMS": [
                        {
                            "ID": 1,
                            "GROUP_NAME": creepcoeff.GROUP_NAME,
                            "CREEP": creepcoeff.CREEP
                        }
                    ]
                }
                
                json_data["Assign"][str(creepcoeff.ELEMENT_ID)] = items_data
            
            return json_data
        
        @classmethod
        def create(cls):
            """Creates creep coefficients in the database"""
            return MidasAPI("PUT", "/db/crpc", cls.json())
        
        @classmethod
        def get(cls):
            """Gets creep coefficient data from the database"""
            return MidasAPI("GET", "/db/crpc")
        
        @classmethod
        def sync(cls):
            """Updates the CreepCoeff class with data from the database"""
            cls.creepcoeffs = []
            response = cls.get()
            
            if response != {'message': ''}:
                if "CRPC" in response:
                    crpc_data_dict = response["CRPC"]
                else:
                    return
                
                for element_id, crpc_data in crpc_data_dict.items():
                    items = crpc_data.get("ITEMS", [])
                    
                    for item in items:
                        group_name = item.get("GROUP_NAME", "")
                        creep = item.get("CREEP", 0.0)
                        item_id = item.get("ID", 1)
                        
                        # Create a new CreepCoeff object
                        new_creepcoeff = CS.CreepCoeff(
                            element_id=int(element_id),
                            creep=creep,
                            group=group_name,
                            id=item_id
                        )
                        
                        # Remove the automatically added instance and replace with synced data
                        CS.CreepCoeff.creepcoeffs.pop()
                        CS.CreepCoeff.creepcoeffs.append(new_creepcoeff)
        
        @classmethod
        def delete(cls):
            """Deletes all creep coefficients from the database and resets the class"""
            cls.creepcoeffs = []
            return MidasAPI("DELETE", "/db/crpc")

    class Camber:
        cambers = []

        def __init__(self, 
                    node_id: int,
                    camber: float,
                    deform: float,
                    id: int = None):
            """
            Camber for Construction Stage define.
            
            Parameters:
                node_id: Node ID (required)
                camber: User camber value (required)
                deform: Deformation value (required)
                id: The camber ID (optional)
            
            Examples:
                ```python
                
                CS.Camber(25, 0.17, 0.1)
                ```
            """
            
            self.NODE_ID = node_id
            self.USER = camber
            self.DEFORM = deform
            
            # Set ID
            if id is None:
                self.ID = len(CS.Camber.cambers) + 1
            else:
                self.ID = id
            
            CS.Camber.cambers.append(self)
        
        @classmethod
        def json(cls):
            """
            Converts Camber data to JSON format 
            Example:
                # Get the JSON data for all cambers
                json_data = CS.Camber.json()
                print(json_data)
            """
            json_data = {"Assign": {}}
            
            for camber in cls.cambers:
                camber_data = {
                    "DEFORM": camber.DEFORM,
                    "USER": camber.USER
                }
                
                json_data["Assign"][str(camber.NODE_ID)] = camber_data
            
            return json_data
        
        @classmethod
        def create(cls):
            """Creates cambers in the database"""
            return MidasAPI("PUT", "/db/cmcs", cls.json())
        
        @classmethod
        def get(cls):
            """Gets camber data from the database"""
            return MidasAPI("GET", "/db/cmcs")
        
        @classmethod
        def sync(cls):
            """Updates the Camber class with data from the database"""
            cls.cambers = []
            response = cls.get()
            
            if response != {'message': ''}:
                if "CMCS" in response:
                    cmcs_data_dict = response["CMCS"]
                else:
                    return
                
                for node_id, cmcs_data in cmcs_data_dict.items():
                    deform = cmcs_data.get("DEFORM", 0.0)
                    user = cmcs_data.get("USER", 0.0)
                    
                    # Create a new Camber object
                    new_camber = CS.Camber(
                        node_id=int(node_id),
                        camber=user,
                        deform=deform,
                        id=len(cls.cambers) + 1
                    )
                    
                    # Remove the automatically added instance and replace with synced data
                    CS.Camber.cambers.pop()
                    CS.Camber.cambers.append(new_camber)
        
        @classmethod
        def delete(cls):
            """Deletes all cambers from the database and resets the class"""
            cls.cambers = []
            return MidasAPI("DELETE", "/db/cmcs")
