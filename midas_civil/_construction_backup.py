from ._mapi import *

class CS:

    CSA = []  

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
                 sr_stage: bool = True, 
                 ad_stage: bool = False, 
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
            sr_stage: Save results of this stage (default True)
            ad_stage: Add additional step results (default False)
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
               sr_stage=True, ad_stage=True, load_in=True, nl=6, addstp=[1, 2, 3])
            ```
        """

        self.NAME = name
        self.DURATION = duration
        self.SR_stage = sr_stage
        self.Ad_stage = ad_stage
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
            self.ID = len(CS.CSA) + 1
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
                    for stage in CS.CSA:
                        for existing_group in stage.act_structure_groups:
                            if existing_group["name"] == group:
                                raise ValueError(f"Structure group '{group}' has already been activated in stage '{stage.NAME}' (ID: {stage.ID})")
                    
                    age = s_age[i] if i < len(s_age) else 0
                    self.act_structure_groups.append({"name": group, "age": age})
                else:
                    # Deactivation: Check if activated in previous stages
                    activated = False
                    for stage in CS.CSA:
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
                    for stage in CS.CSA:
                        for existing_group in stage.act_boundary_groups:
                            if existing_group["name"] == group:
                                raise ValueError(f"Boundary group '{group}' has already been activated in stage '{stage.NAME}' (ID: {stage.ID})")
                    
                    pos = b_pos[i] if i < len(b_pos) else "DEFORMED"
                    self.act_boundary_groups.append({"name": group, "pos": pos})
                else:
                    # Deactivation: Check if activated in previous stages
                    activated = False
                    for stage in CS.CSA:
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
                    for stage in CS.CSA:
                        for existing_group in stage.act_load_groups:
                            if existing_group["name"] == group:
                                raise ValueError(f"Load group '{group}' has already been activated in stage '{stage.NAME}' (ID: {stage.ID})")
                    
                    day = l_day[i] if i < len(l_day) else "FIRST"
                    self.act_load_groups.append({"name": group, "day": day})
                else:
                    # Deactivation: Check if activated in previous stages
                    activated = False
                    for stage in CS.CSA:
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
        
        CS.CSA.append(self)
    
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
        
        for csa in cls.CSA:
            stage_data = {
                "NAME": csa.NAME,
                "DURATION": csa.DURATION,
                "bSV_RSLT": csa.SR_stage,
                "bSV_STEP": csa.Ad_stage,
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
        MidasAPI("PUT", "/db/stag", CS.json())
    
    @classmethod
    def get(cls):
        """Gets construction stage data from the database"""
        return MidasAPI("GET", "/db/stag")
    
    @classmethod
    def sync(cls):
        """Updates the CS class with data from the database"""
        cls.CSA = []
        a = CS.get()
        if a != {'message': ''}:
            if "STAG" in a:
                stag_data_dict = a["STAG"]
            else:
                return  
                
            for stag_id, stag_data in stag_data_dict.items():
                # Basic stage data
                name = stag_data.get("NAME")
                duration = stag_data.get("DURATION")
                sr_stage = stag_data.get("bSV_RSLT")
                ad_stage = stag_data.get("bSV_STEP")
                load_in = stag_data.get("bLOAD_STEP")
                nl = stag_data.get("INCRE_STEP")
                addstp = stag_data.get("ADD_STEP")
                
                # Create a new CS object with basic properties
                new_cs = CS(
                    name=name,
                    duration=duration,
                    id=int(stag_id),
                    sr_stage=sr_stage,
                    ad_stage=ad_stage,
                    load_in=load_in,
                    nl=nl,
                    addstp=addstp
                )
                
                CS.CSA.pop()
                
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
                
                CS.CSA.append(new_cs)
    
    @classmethod
    def delete(cls):
        """Deletes all construction stages from the database and resets the class"""
        cls.CSA = []
        return MidasAPI("DELETE", "/db/stag")