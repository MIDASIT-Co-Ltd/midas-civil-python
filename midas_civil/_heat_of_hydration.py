from ._mapi import MidasAPI
from ._group import Group
from typing import Literal

#Literals
_CementType = Literal['Normal', 'Moderate Heat', 'High-early-strength', 'Blast-furnace Slag', 'Fly Ash']
_Temperature = Literal[10, 20, 30]
_HoHStressCompnents = Literal['Sig_xx','Sig_yy','Sig_zz','Max','Sig_P1','Sig_P2','Sig_P3']
_Map_Stress_Components = {'Sig_xx' : 0, 'Sig_yy' : 1,'Sig_zz' : 2, 'Max' :3, 'Sig_P1' : 4, 'Sig_P2' : 5, 'Sig_P3' : 6}
_Reverse_Map_Stress_Components = {0: 'Sig_xx', 1: 'Sig_yy', 2: 'Sig_zz', 3: 'Max', 4: 'Sig_P1', 5: 'Sig_P2', 6: 'Sig_P3'}


class HoH:

    @staticmethod
    def create():
        if HoH.PipeCooling.data: HoH.PipeCooling.create()
        if HoH.PrescribedTemperature.data: HoH.PrescribedTemperature.create()
        if HoH.Ambient_Temperature_Function.functions: HoH.Ambient_Temperature_Function.create()
        if HoH.Convection.Coefficient_Function.functions: HoH.Convection.Coefficient_Function.create()
        if HoH.Convection.Boundary.data: HoH.Convection.Boundary.create()
        if HoH.HeatSource.Function.functions: HoH.HeatSource.Function.create()
        if HoH.HeatSource.AssignHeatSource.data: HoH.HeatSource.AssignHeatSource.create()
        if HoH.CS.STAGE.stages: HoH.CS.STAGE.create()

    class PipeCooling:

        data: list['HoH.PipeCooling'] = []
        ids: list[int] = []
        maxID: int = 0

        def __init__(self,
                     name: str,
                     pipe_diameter: float,
                     convection_coeff: float,
                     specific_heat: float,
                     weight_density: float,
                     inlet_temp: float,
                     flow_rate: float,
                     start_stage: str,
                     end_stage: str,
                     start_time: float,
                     end_time: float,
                     node_list: list[int],
                     id: int = 0):
            """
            Pipe Cooling constructor for reducing hydration temperature.
            
            Parameters:
                name: Name of the pipe cooling group.
                
                pipe_diameter: Cooling pipe diameter.

                convection_coeff: Convection coefficient of the cooling pipe.

                specific_heat: Specific heat of the cooling water.
                
                weight_density: Density of the cooling water.

                inlet_temp: Inlet temperature of the cooling water.

                flow_rate: Flow rate of the cooling water.

                start_stage: Starting construction stage for the application.
                
                end_stage: Ending construction stage for disengagement.
                
                start_time: Time of application (hr) relative to the start stage.
                
                end_time: Time of disengagement (hr) relative to the end stage.
                
                node_list: List of node numbers defining the path of the pipe.
                
                id: Optional ID for the pipe cooling group (default is 0 for auto-assignment).
            
            Examples:
                # Basic pipe cooling group
                HoH.PipeCooling(
                    name="PC1", pipe_diameter=3, convection_coeff=133.7, 
                    specific_heat=4186, weight_density=0.001, inlet_temp=15, 
                    flow_rate=20, start_stage="CS1", end_stage="CS1", 
                    start_time=10, end_time=100, node_list=[2809, 2810, 2811]
                )
            """
            
            self.NAME = name
            self.PIPE_DIAMETER = pipe_diameter
            self.CONVECTION_COEFF = convection_coeff
            self.SPECIFIC_HEAT = specific_heat
            self.WEIGHT_DENSITY = weight_density
            self.INLET_TEMP = inlet_temp
            self.FLOW_RATE = flow_rate
            self.START_STAGE = start_stage
            self.END_STAGE = end_stage
            self.START_TIME = start_time
            self.END_TIME = end_time
            self.NODE_LIST = node_list
            
            if id == 0:
                HoH.PipeCooling.maxID += 1
                self.ID = HoH.PipeCooling.maxID
            else:
                self.ID = id
                if id > HoH.PipeCooling.maxID:
                    HoH.PipeCooling.maxID = id
            
            HoH.PipeCooling.data.append(self)
            HoH.PipeCooling.ids.append(self.ID)

        @classmethod
        def json(cls) -> dict:
            """Generates the properly formatted JSON payload for MidasAPI."""
            json_data = {"Assign": {}}
            for item in cls.data:
                json_data["Assign"][item.ID] = {
                    "NAME": item.NAME,
                    "DIAMETER": item.PIPE_DIAMETER,
                    "COEF": item.CONVECTION_COEFF,
                    "HEAT": item.SPECIFIC_HEAT,
                    "DENSITY": item.WEIGHT_DENSITY,
                    "TEMPER": item.INLET_TEMP,
                    "FLOW_RATE": item.FLOW_RATE,
                    "START_STAGE": item.START_STAGE,
                    "END_STAGE": item.END_STAGE,
                    "START_TIME": item.START_TIME,
                    "END_TIME": item.END_TIME,
                    "ITEMS": item.NODE_LIST
                }
            return json_data

        @classmethod
        def create(cls):
            """Sends the PUT request to create all stored PipeCooling objects in Midas."""
            if cls.data:
                MidasAPI("PUT", "/db/HPCE", cls.json())

        @staticmethod
        def get():
            """Retrieves the PipeCooling configuration from Midas."""
            return MidasAPI("GET", "/db/HPCE")

        @classmethod
        def sync(cls):
            """Fetches data from Midas and reconstructs the local class instances."""
            resp = cls.get()
            if resp and 'HPCE' in resp and resp['HPCE']:
                cls.clear()
                for key_id, val in resp['HPCE'].items():
                    cls(
                        name=val.get("NAME", f"PC_{key_id}"),
                        pipe_diameter=val.get("DIAMETER", 0.0),
                        convection_coeff=val.get("COEF", 0.0),
                        specific_heat=val.get("HEAT", 0.0),
                        weight_density=val.get("DENSITY", 0.0),
                        inlet_temp=val.get("TEMPER", 0.0),
                        flow_rate=val.get("FLOW_RATE", 0.0),
                        start_stage=val.get("START_STAGE", ""),
                        end_stage=val.get("END_STAGE", ""),
                        start_time=val.get("START_TIME", 0.0),
                        end_time=val.get("END_TIME", 0.0),
                        node_list=val.get("ITEMS", []),
                        id=int(key_id)
                    )

        @staticmethod
        def delete():
            """Deletes all pipe cooling objects from the active Midas database."""
            MidasAPI("DELETE", "/db/HPCE")
            HoH.PipeCooling.clear()

        @classmethod
        def clear(cls):
            """Clears all locally stored PipeCooling objects."""
            cls.data = []
            cls.ids = []
            cls.maxID = 0

    class PrescribedTemperature:

        data:list['HoH.PrescribedTemperature'] = []
        ids = []

        def __init__(self,
                     node_id,
                     temperature: float,
                     group_name: str = "",
                     serial_id: int = 1):
            """
            Prescribed Temperature constructor for defining constant temperature limits on nodes.
            
            Parameters:
                node_id: Node number (int) or multiple nodes (list, tuple, set) to apply the temperature.
                
                temperature: The prescribed constant temperature value.
                
                group_name: Boundary Group Name which contains the entered boundary condition (default "").
                
                serial_id: Serial Number for the item within the node (default 1).
            
            Examples:
                # Apply to a single node
                PrescribedTemperature(node_id=1, temperature=25.0)
                
                # Apply to multiple nodes at once
                PrescribedTemperature(node_id=[2, 3, 4], temperature=20.0, group_name="Ground_Boundary")
            """
            
            if isinstance(node_id, (list, tuple, set)):
                for nID in node_id:
                    self.__class__(nID, temperature, group_name, serial_id)
                return
            
            self.NODE_ID = int(node_id)
            self.TEMPER = temperature
            self.GROUP_NAME = group_name
            self.SERIAL_ID = serial_id
        
            self.__class__.data.append(self)
            self.__class__.ids.append(self.NODE_ID)

        @classmethod
        def json(cls) -> dict:
            """Generates the properly formatted JSON payload for MidasAPI."""
            json_data = {"Assign": {}}
            for item in cls.data:
                node_key = str(item.NODE_ID)
  
                if node_key not in json_data["Assign"]:
                    json_data["Assign"][node_key] = {"ITEMS": []}
                
                json_data["Assign"][node_key]["ITEMS"].append({
                    "ID": item.SERIAL_ID,
                    "GROUP_NAME": item.GROUP_NAME,
                    "TEMPER": item.TEMPER
                })
            return json_data

        @classmethod
        def create(cls):
            """Sends the PUT request to create all stored PrescribedTemperature objects in Midas."""
            if cls.data:
                MidasAPI("PUT", "/db/HSPT", cls.json())

        @staticmethod
        def get():
            """Retrieves the PrescribedTemperature configuration from Midas."""
            return MidasAPI("GET", "/db/HSPT")

        @classmethod
        def sync(cls):
            """Fetches data from Midas and reconstructs the local class instances."""
            resp = cls.get()
            if resp and 'HSPT' in resp and resp['HSPT'] and resp['HSPT'] != {'message': ''}:
                cls.clear()
                for node_key, val in resp['HSPT'].items():
                    items = val.get("ITEMS", [])
                    for item_data in items:
                        cls(
                            node_id=int(node_key),
                            temperature=item_data.get("TEMPER", 0.0),
                            group_name=item_data.get("GROUP_NAME", ""),
                            serial_id=item_data.get("ID", 1)
                        )

        @staticmethod
        def delete():
            """Deletes all prescribed temperature objects from the active Midas database."""
            MidasAPI("DELETE", "/db/HSPT")
            HoH.PrescribedTemperature.clear()

        @classmethod
        def clear(cls):
            """Clears all locally stored PrescribedTemperature objects."""
            cls.data = []
            cls.ids = []

    class Ambient_Temperature_Function:

        functions: list['HoH.Ambient_Temperature_Function'] = []
        _ids = [0]

        @classmethod
        def json(cls) -> dict:
            """Generates the properly formatted JSON payload for MidasAPI."""
            js_data = {"Assign": {}}
            for func in cls.functions:
                js_data["Assign"][str(func.ID)] = func._json()
            return js_data
        
        @classmethod
        def create(cls):
            """Sends the PUT request to create all stored Ambient Temperature Functions in Midas."""
            if cls.functions:
                MidasAPI('PUT', '/db/ETFC', cls.json())  

        @staticmethod
        def get():
            """Retrieves the Ambient Temperature Functions configuration from Midas."""
            return MidasAPI('GET', '/db/ETFC')

        @classmethod
        def sync(cls):
            """Fetches data from Midas and reconstructs the local class instances."""
            resp = cls.get()
            if resp and 'ETFC' in resp and resp['ETFC']:
                cls.clear()
                for key_id, val in resp['ETFC'].items():
                    func_type = val.get("TYPE", "")
                    name = val.get("NAME", f"Func_{key_id}")
                    fid = int(key_id)
                    
                    if func_type == "CONST":
                        cls.Constant(name=name, temperature=val.get("TEMP", 0.0), id=fid)
                    elif func_type == "SINE":
                        cls.Sine(
                            name=name, 
                            max_temp=val.get("MAX_TEMP", 0.0),
                            mean_temp=val.get("MEAN_TEMP", 0.0),
                            delay_time=val.get("DELAY_TIME", 0.0),
                            id=fid
                        )
                    elif func_type == "USER":
                        items = val.get("ITEM", [])
                        time_temp_data = [(item.get("TIME", 0.0), item.get("VALUE", 0.0)) for item in items]
                        cls.User(
                            name=name,
                            scale_factor=val.get("SCALE_FACTOR", 1.0),
                            time_temp_data=time_temp_data,
                            id=fid
                        )

        @staticmethod
        def delete():
            """Deletes all Ambient Temperature Functions from the active Midas database."""
            MidasAPI("DELETE", "/db/ETFC")
            HoH.Ambient_Temperature_Function.clear()

        @classmethod
        def clear(cls):
            """Clears all locally stored function objects."""
            cls.functions = []
            cls._ids = [0]

        class Constant:
            def __init__(self, name: str, temperature: float, id: int = None):
                """
                Assign a constant ambient temperature.
                
                Parameters:
                    name: Name of the ambient temperature function.
                    temperature: Constant temperature value.
                    id: Optional identifier.
                """
                if id is None:
                    self.ID = max(HoH.Ambient_Temperature_Function._ids) + 1
                else:
                    self.ID = id
                
                self.NAME = name
                self.TYPE = "CONST"
                self.TEMP = temperature
                
                HoH.Ambient_Temperature_Function.functions.append(self)
                HoH.Ambient_Temperature_Function._ids.append(self.ID)

            def _json(self):
                return {
                    "NAME": self.NAME,
                    "TYPE": self.TYPE,
                    "TEMP": self.TEMP
                }

        class Sine:
            def __init__(self, name: str, max_temp: float, mean_temp: float, delay_time: float, id: int = None):
                """
                Ambient temperature fluctuates in a Sine function.
                
                Parameters:
                    name: Name of the ambient temperature function.
                    max_temp: Amplitude of the Sine function (T).
                    mean_temp: Initial temperature immediately after concrete casting (To).
                    delay_time: Time immediately after concrete casting in days (to).
                    id: Optional identifier.
                """
                if id is None:
                    self.ID = max(HoH.Ambient_Temperature_Function._ids) + 1
                else:
                    self.ID = id
                
                self.NAME = name
                self.TYPE = "SINE"
                self.MAX_TEMP = max_temp
                self.MEAN_TEMP = mean_temp
                self.DELAY_TIME = delay_time
                
                HoH.Ambient_Temperature_Function.functions.append(self)
                HoH.Ambient_Temperature_Function._ids.append(self.ID)

            def _json(self):
                return {
                    "NAME": self.NAME,
                    "TYPE": self.TYPE,
                    "MAX_TEMP": self.MAX_TEMP,
                    "MEAN_TEMP": self.MEAN_TEMP,
                    "DELAY_TIME": self.DELAY_TIME
                }

        class User:
            def __init__(self, name: str, scale_factor: float, time_temp_data: list[tuple[float, float]], id: int = None):
                """
                User defined variation of ambient temperature.
                
                Parameters:
                    name: Name of the ambient temperature function.
                    scale_factor: Scale factor applied to the function data.
                    time_temp_data: List of tuples specifying (Time, Temperature).
                    id: Optional identifier.
                """
                if id is None:
                    self.ID = max(HoH.Ambient_Temperature_Function._ids) + 1
                else:
                    self.ID = id
                
                self.NAME = name
                self.TYPE = "USER"
                self.SCALE_FACTOR = scale_factor
                self.ITEM = time_temp_data 
                
                HoH.Ambient_Temperature_Function.functions.append(self)
                HoH.Ambient_Temperature_Function._ids.append(self.ID)

            def _json(self):
                js_data = {
                    "NAME": self.NAME,
                    "TYPE": self.TYPE,
                    "SCALE_FACTOR": self.SCALE_FACTOR,
                    "ITEM": []
                }
                
                for item in self.ITEM:
                    js_data["ITEM"].append({
                        "TIME": item[0],
                        "VALUE": item[1]
                    })

                return js_data
            
    class Convection:

        @staticmethod
        def clear():
            HoH.Convection.Boundary.clear()
            HoH.Convection.Coefficient_Function.clear()

        @staticmethod
        def delete():
            HoH.Convection.Boundary.delete()
            HoH.Convection.Coefficient_Function.delete()

        @staticmethod
        def create():
            HoH.Convection.Coefficient_Function.create()
            HoH.Convection.Boundary.create()

        class Coefficient_Function:

            functions: list['HoH.Convection.Coefficient_Function'] = []
            _ids = [0]

            @classmethod
            def json(cls) -> dict:
                """Generates the properly formatted JSON payload for MidasAPI."""
                js_data = {"Assign": {}}
                for func in cls.functions:
                    js_data["Assign"][str(func.ID)] = func._json()
                return js_data
            
            @classmethod
            def create(cls):
                """Sends the PUT request to create all stored Convection Coefficient Functions in Midas."""
                if cls.functions:
                    MidasAPI('PUT', '/db/CCFC', cls.json())  

            @staticmethod
            def get():
                """Retrieves the Convection Coefficient Functions configuration from Midas."""
                return MidasAPI('GET', '/db/CCFC')

            @classmethod
            def sync(cls):
                """Fetches data from Midas and reconstructs the local class instances."""
                resp = cls.get()
                if resp and 'CCFC' in resp and resp['CCFC']:
                    cls.clear()
                    for key_id, val in resp['CCFC'].items():
                        func_type = val.get("TYPE", "")
                        name = val.get("NAME", f"Func_{key_id}")
                        fid = int(key_id)
                        
                        if func_type == "CONST":
                            cls.Constant(name=name, coefficient=val.get("COEF", 0.0), id=fid)
                        elif func_type == "USER":
                            items = val.get("ITEM", [])
                            time_coeff_data = [(item.get("TIME", 0.0), item.get("VALUE", 0.0)) for item in items]
                            cls.User(
                                name=name,
                                scale_factor=val.get("SCALE_FACTOR", 1.0),
                                time_coeff_data=time_coeff_data,
                                id=fid
                            )

            @staticmethod
            def delete():
                """Deletes all Convection Coefficient Functions from the active Midas database."""
                MidasAPI("DELETE", "/db/CCFC")
                HoH.Convection.Coefficient_Function.clear()

            @classmethod
            def clear(cls):
                """Clears all locally stored function objects."""
                cls.functions = []
                cls._ids = [0]

            class Constant:
                def __init__(self, name: str, coefficient: float, id: int = None):
                    """
                    Assign a constant convection coefficient.
                    
                    Parameters:
                        name: Name of the convection coefficient function.
                        coefficient: Constant convection coefficient value.
                        id: Optional identifier.
                    """
                    if id is None:
                        self.ID = max(HoH.Convection.Coefficient_Function._ids) + 1
                    else:
                        self.ID = id
                    
                    self.NAME = name
                    self.TYPE = "CONST"
                    self.COEF = coefficient
                    
                    HoH.Convection.Coefficient_Function.functions.append(self)
                    HoH.Convection.Coefficient_Function._ids.append(self.ID)

                def _json(self):
                    return {
                        "NAME": self.NAME,
                        "TYPE": self.TYPE,
                        "COEF": self.COEF
                    }

            class User:
                def __init__(self, name: str, scale_factor: float, time_coeff_data: list[tuple[float, float]], id: int = None):
                    """
                    User defined variation of convection coefficient.
                    
                    Parameters:
                        name: Name of the convection coefficient function.
                        scale_factor: Scale factor applied to the function data.
                        time_coeff_data: List of tuples specifying (Time, Value).
                        id: Optional identifier.
                    """
                    if id is None:
                        self.ID = max(HoH.Convection.Coefficient_Function._ids) + 1
                    else:
                        self.ID = id
                    
                    self.NAME = name
                    self.TYPE = "USER"
                    self.SCALE_FACTOR = scale_factor
                    self.ITEM = time_coeff_data 
                    
                    HoH.Convection.Coefficient_Function.functions.append(self)
                    HoH.Convection.Coefficient_Function._ids.append(self.ID)

                def _json(self):
                    js_data = {
                        "NAME": self.NAME,
                        "TYPE": self.TYPE,
                        "SCALE_FACTOR": self.SCALE_FACTOR,
                        "ITEM": []
                    }
                    
                    for item in self.ITEM:
                        js_data["ITEM"].append({
                            "TIME": item[0],
                            "VALUE": item[1]
                        })

                    return js_data
                
         
        class Boundary:
            
            data:list['HoH.Convection.Boundary'] = []

            def __init__(self,elmID:int,faceID:int,conv_coeff_func:str='',amb_temp_func:str='',group:str='',id:int=None):
                self.ELM = elmID
                self.FACE = faceID
                self.CONV_FUNC = conv_coeff_func
                self.AMB_FUNC = amb_temp_func
                self.GROUP = group

                if group != "":
                    chk = 0
                    a = [v['NAME'] for v in Group.Boundary.json()["Assign"].values()]
                    if group in a: chk = 1
                    if chk == 0: Group.Boundary(group)

                if id is None:
                    self.ID = len(HoH.Convection.Boundary.data) + 1
                else:
                    self.ID = id

                HoH.Convection.Boundary.data.append(self)

            @classmethod
            def json(cls):
                json = {"Assign": {}}
                for i in cls.data:
                    if i.ELM not in list(json["Assign"].keys()):
                        json["Assign"][i.ELM] = {"ITEMS": []}

                    json["Assign"][i.ELM]["ITEMS"].append({
                            "ID": i.ID,
                            "GROUP_NAME": i.GROUP,
                            "FACE_NO": i.FACE,
                            "CCFC_NAME": i.CONV_FUNC,
                            "ETFC_NAME": i.AMB_FUNC
                        })
                return json

            @classmethod
            def create(cls):
                MidasAPI("PUT", "/db/HECB",cls.json())
            
            @classmethod
            def get(cls):
                return MidasAPI("GET", "/db/HECB")
            
            @classmethod
            def delete(cls):
                cls.clear()
                return MidasAPI("DELETE", "/db/HECB")
            
            @classmethod
            def clear(cls):
                cls.data=[]
            
            @classmethod
            def sync(cls):
                cls.data = []
                a = cls.get()
                if a != {'message': ''}:
                    for i in a['HECB'].keys():
                        for j in range(len(a['HECB'][i]['ITEMS'])):
                            HoH.Convection.Boundary(int(i),a['HECB'][i]['ITEMS'][j]['FACE_NO'],
                                                    a['HECB'][i]['ITEMS'][j]['CCFC_NAME'],a['HECB'][i]['ITEMS'][j]['ETFC_NAME'],
                                                    a['HECB'][i]['ITEMS'][j]['GROUP_NAME'],a['HECB'][i]['ITEMS'][j]['ID'])
        
        
            @staticmethod
            def bySelectedNodes(nodeIDs:list,conv_coeff_func:str='',amb_temp_func:str='',group:str=''):
                from ._element import Element

                faceMapper = {
                            8: {
                                "TTTTFFFF": 1 ,
                                "FFFFTTTT": 2 ,
                                "TTFFTTFF": 3 ,
                                "FTTFFTTF": 4 ,
                                "FFTTFFTT": 5 ,
                                "TFFTTFFT": 6 ,
                            },
                            6: {
                                "TTTFFF": 1 ,
                                "FFFTTT": 2 ,
                                "TTFTTF": 3 ,
                                "FTTFTT": 4 ,
                                "TFTTFT": 5 ,
                            },
                            4: {
                                "TTTF": 1 ,
                                "TTFT": 2 ,
                                "FTTT": 3 ,
                                "TFTT": 4 ,
                            }
                        }

                for elm in Element.elements:
                    chk = ""
                    if elm.TYPE == 'SOLID':
                        n_node = len(elm.NODE)
                        for nID in elm.NODE:
                            if nID in nodeIDs:
                                chk+="T"
                            else:
                                chk+="F"
                        face_no = faceMapper[n_node].get(chk,None)
                        if face_no is not None:
                            HoH.Convection.Boundary(elm.ID ,face_no,conv_coeff_func,amb_temp_func,group,None)

        #------------------------



    class HeatSource:
        class Function:

            functions: list['HoH.HeatSource.Function'] = []
            _ids = [0]

            @classmethod
            def json(cls) -> dict:
                """Generates the properly formatted JSON payload for MidasAPI."""
                js_data = {"Assign": {}}
                for func in cls.functions:
                    js_data["Assign"][str(func.ID)] = func._json()
                return js_data
            
            @classmethod
            def create(cls):
                """Sends the PUT request to create all stored Heat Source Functions in Midas."""
                if cls.functions:
                    MidasAPI('PUT', '/db/HSFC', cls.json())  

            @staticmethod
            def get():
                """Retrieves the Heat Source Functions configuration from Midas."""
                return MidasAPI('GET', '/db/HSFC')

            @classmethod
            def sync(cls):
                """Fetches data from Midas and reconstructs the local class instances."""
                resp = cls.get()
                if resp and 'HSFC' in resp and resp['HSFC']:
                    cls.clear()
                    
                    rev_cement = {0: 'Normal', 1: 'Moderate Heat', 2: 'High-early-strength', 3: 'Blast-furnace Slag', 4: 'Fly Ash'}
                    rev_temp = {0: 10, 1: 20, 2: 30}
                    
                    for key_id, val in resp['HSFC'].items():
                        func_type = val.get("TYPE", "")
                        name = val.get("NAME", f"Func_{key_id}")
                        fid = int(key_id)
                        
                        if func_type == "CONST":
                            cls.Constant(
                                name=name, 
                                heat_source=val.get("TEMP_CONST", 0.0), 
                                id=fid
                            )
                        elif func_type == "FUNC":
                            raw_cement = val.get("CEMENT_TYPE", 0)
                            raw_temp = val.get("TEMP_FUNC", 0)
                            
                            cls.Code(
                                name=name,
                                use_concrete_data=val.get("OPT_USE_CONC_DATA", False),
                                k=val.get("K", 0.0),
                                alpha=val.get("ALPHA", 0.0),
                                cement_type=rev_cement.get(raw_cement, 'Normal'),
                                temperature=rev_temp.get(raw_temp, 10),
                                cement_content=val.get("CEMENT_CONT", 0.0),
                                id=fid
                            )
                        elif func_type == "USER":
                            items = val.get("ITEM", [])
                            time_value_data = [(item.get("TIME", 0.0), item.get("VALUE", 0.0)) for item in items]
                            cls.User(
                                name=name,
                                scale_factor=val.get("SCALE_FACTOR", 1.0),
                                time_value_data=time_value_data,
                                is_adiabatic_temp=val.get("IS_ADIABATIC_TEMP", True),
                                id=fid
                            )

            @staticmethod
            def delete():
                """Deletes all Heat Source Functions from the active Midas database."""
                MidasAPI("DELETE", "/db/HSFC")
                HoH.HeatSource.Function.clear()

            @classmethod
            def clear(cls):
                """Clears all locally stored function objects."""
                cls.functions = []
                cls._ids = [0]

            class Constant:
                def __init__(self, name: str, heat_source: float, id: int = None):
                    """
                    Assign a constant heat source.
                    
                    Parameters:
                        name: Name of the heat source function.
                        heat_source: Constant heat source value.
                        id: Optional identifier.
                    """
                    if id is None:
                        self.ID = max(HoH.HeatSource.Function._ids) + 1
                    else:
                        self.ID = id
                    
                    self.NAME = name
                    self.TYPE = "CONST"
                    self.TEMP_CONST = heat_source
                    
                    HoH.HeatSource.Function.functions.append(self)
                    HoH.HeatSource.Function._ids.append(self.ID)

                def _json(self):
                    return {
                        "NAME": self.NAME,
                        "TYPE": self.TYPE,
                        "TEMP_CONST": self.TEMP_CONST
                    }

            class Code:
                def __init__(self, name: str, use_concrete_data: bool = False,
                             k: float = None, alpha: float = None,
                             cement_type: _CementType = None,
                             temperature: _Temperature = None,
                             cement_content: float = None,
                             id: int = None):
                    """
                    Assign heat source based on Code definitions, either user-specified constants or concrete data.
                    
                    Parameters:
                        name: Name of the heat source function.
                        use_concrete_data: True to use concrete properties, False to manually input K and Alpha.
                        k: Maximize adiabatic temperature rise (K) - Only if use_concrete_data is False.
                        alpha: Reactive velocity coefficient - Only if use_concrete_data is False.
                        cement_type: 'Normal', 'Moderate Heat', 'High-early-strength', 'Blast-furnace Slag', or 'Fly Ash'.
                        temperature: 10, 20, or 30 (representing degrees Celsius).
                        cement_content: Cement content value.
                        id: Optional identifier.
                    """
                    if id is None:
                        self.ID = max(HoH.HeatSource.Function._ids) + 1
                    else:
                        self.ID = id

                    
                    if use_concrete_data and (cement_type is None or temperature is None or cement_type is None):
                        raise ValueError("cemenet_type, temperature and cemenet_type are required when use_concrete_data is True.")

                    if not use_concrete_data and (k is None or alpha is None):
                        raise ValueError("k and alpha are required when use_concrete_data is False.")                    
                    
                    self.NAME = name
                    self.TYPE = "FUNC"
                    self.OPT_USE_CONC_DATA = use_concrete_data
                    
                    self.K = k
                    self.ALPHA = alpha
                    

                    cement_mapping = {
                        'Normal': 0,
                        'Moderate Heat': 1,
                        'High-early-strength': 2,
                        'Blast-furnace Slag': 3,
                        'Fly Ash': 4
                    }
                    self.CEMENT_TYPE = cement_mapping.get(cement_type, 0)
                    
                    temp_mapping = {
                        10: 0,
                        20: 1,
                        30: 2,
                        '10': 0,
                        '20': 1,
                        '30': 2
                    }
                    self.TEMP_FUNC = temp_mapping.get(temperature, 0)
                    
                    self.CEMENT_CONT = cement_content
                    
                    HoH.HeatSource.Function.functions.append(self)
                    HoH.HeatSource.Function._ids.append(self.ID)

                def _json(self):
                    js_data = {
                        "NAME": self.NAME,
                        "TYPE": self.TYPE,
                        "OPT_USE_CONC_DATA": self.OPT_USE_CONC_DATA
                    }
                    
                    if self.OPT_USE_CONC_DATA:
                        js_data["CEMENT_TYPE"] = self.CEMENT_TYPE
                        js_data["TEMP_FUNC"] = self.TEMP_FUNC
                        js_data["CEMENT_CONT"] = self.CEMENT_CONT
                    else:
                        js_data["K"] = self.K
                        js_data["ALPHA"] = self.ALPHA
                        
                    return js_data

            class User:
                def __init__(self, name: str, scale_factor: float, time_value_data: list[tuple[float, float]],
                             is_adiabatic_temp: bool = True, id: int = None):
                    """
                    User defined variation of heat source.
                    
                    Parameters:
                        name: Name of the heat source function.
                        scale_factor: Scale factor applied to the function data.
                        time_value_data: List of tuples specifying (Time, Value).
                        is_adiabatic_temp: True for Temperature, False for Heat Source.
                        id: Optional identifier.
                    """
                    if id is None:
                        self.ID = max(HoH.HeatSource.Function._ids) + 1
                    else:
                        self.ID = id
                    
                    self.NAME = name
                    self.TYPE = "USER"
                    self.IS_ADIABATIC_TEMP = is_adiabatic_temp
                    self.SCALE_FACTOR = scale_factor
                    self.ITEM = time_value_data 
                    
                    HoH.HeatSource.Function.functions.append(self)
                    HoH.HeatSource.Function._ids.append(self.ID)

                def _json(self):
                    js_data = {
                        "NAME": self.NAME,
                        "TYPE": self.TYPE,
                        "IS_ADIABATIC_TEMP": self.IS_ADIABATIC_TEMP,
                        "SCALE_FACTOR": self.SCALE_FACTOR,
                        "ITEM": []
                    }
                    
                    for item in self.ITEM:
                        js_data["ITEM"].append({
                            "TIME": item[0],
                            "VALUE": item[1]
                        })

                    return js_data
                
        class AssignHeatSource:

            _dict = {}
            data:list['HoH.HeatSource.AssignHeatSource'] = []

            def __init__(self,element_id:int,func_name:str):
                """
                Assign a heat source function to an element.

                Parameters:
                    element_id (int or list or tuple or set): ID of the element to which the heat source is assigned.
                    func_name (str): Name of the heat source function to assign.
                """
                if isinstance(element_id, (list, tuple, set)):
                    for eID in element_id:
                        self.__class__(eID, func_name)
                    return
        
                if element_id in self.__class__._dict:
                    print(f"⚠️ Element id {element_id} already exists, overwriting")
                    self.__class__.data.remove(self.__class__._dict[element_id])
                
                self.ELEMENT_ID = element_id
                self.FUNCTION_NAME = func_name
        
                self.__class__.data.append(self)
                self.__class__._dict[self.ELEMENT_ID] = self
        
            @classmethod
            def clear(cls):
                cls.data = []
                cls._dict = {}
                
            @classmethod
            def json(cls) -> dict:
                """Generates the properly formatted JSON payload for MidasAPI."""
                json_data = {"Assign": {}}
                for item in cls.data:
                    element_key = str(item.ELEMENT_ID)
    
                    if element_key not in json_data["Assign"]:
                        json_data["Assign"][element_key] = {}
                    
                    json_data["Assign"][element_key] = {
                        "FUNC_NAME": item.FUNCTION_NAME
                    }
                return json_data

            @classmethod
            def create(cls):
                """Sends the PUT request to create all stored AssignHeatSource objects in Midas."""
                if cls.data:
                    MidasAPI("PUT", "/db/HAHS", cls.json())

            @staticmethod
            def get():
                """Retrieves the AssignHeatSource configuration from Midas."""
                return MidasAPI("GET", "/db/HAHS")

            @classmethod
            def sync(cls):
                """Fetches data from Midas and reconstructs the local class instances."""
                resp = cls.get()
                if resp and 'HAHS' in resp and resp['HAHS'] and resp['HAHS'] != {'message': ''}:
                    cls.clear()
                    for element_key, val in resp['HAHS'].items():
                        cls(
                            element_id=int(element_key),
                            func_name=val.get("FUNC_NAME", 0.0),
                        )

            @staticmethod
            def delete():
                """Deletes all AssignHeatSource objects from the active Midas database."""
                MidasAPI("DELETE", "/db/HAHS")
                HoH.PrescribedTemperature.clear()


    class HY_Result_Graph:

        _id =[0]
        data:list['HoH.HY_Result_Graph'] =[]

        def __init__(self,node_id:int,Stress_component:_HoHStressCompnents,id:int = None):
            """
            Define a Heat of Hydration result graph for a specific node and stress component.

            Parameters:
                node_id (int or list or tuple or set): Node number to be displayed in the graph.
                Stress_component (str): ('Sig_xx', 'Sig_yy', 'Sig_zz', 'Max', 'Sig_P1', 'Sig_P2', or 'Sig_P3').
                id (int): Optional identifier (default is None for auto-assignment).
            """

            if isinstance(node_id, (list, tuple, set)):
                for nID in node_id:
                    self.__class__(nID, Stress_component,id)
                return
            
            self.NODE_ID = node_id

            if _Map_Stress_Components.get(Stress_component,0) == 0:
                self.NAME = f"N{node_id} - X"
            elif _Map_Stress_Components.get(Stress_component,0) == 1:
                self.NAME = f"N{node_id} - Y"
            elif _Map_Stress_Components.get(Stress_component,0) == 2:
                self.NAME = f"N{node_id} - Z"
            elif _Map_Stress_Components.get(Stress_component,0) == 3:
                self.NAME = f"N{node_id} - Max"
            elif _Map_Stress_Components.get(Stress_component,0) == 4:
                self.NAME = f"N{node_id} - P1"            
            elif _Map_Stress_Components.get(Stress_component,0) == 5:
                self.NAME = f"N{node_id} - P2"            
            elif _Map_Stress_Components.get(Stress_component,0) == 6:
                self.NAME = f"N{node_id} - P3"            

            self.TYPE = 0
            self.ELEM_KEY = 0
            self.COMP = _Map_Stress_Components.get(Stress_component,0)

            if id is None:
                self.ID = max(self.__class__._id) + 1
            else:
                self.ID = id

            self.__class__.data.append(self)
            self.__class__._id.append(self.ID)

        @classmethod
        def clear(cls):
            cls._id = [0]
            cls.data = []
            
        @classmethod
        def json(cls) -> dict:
            """Generates the properly formatted JSON payload for MidasAPI."""
            json_data = {"Assign": {}}
            for item in cls.data:

                if str(item.ID) not in json_data["Assign"]:
                    json_data["Assign"][str(item.ID)] = {}
                
                json_data["Assign"][str(item.ID)] = {
                    "NAME" : item.NAME,
                    "TYPE": item.TYPE,
                    "NODE_KEY" : item.NODE_ID,
                    "ELEM_KEY" :  item.ELEM_KEY,
                    "COMP" : item.COMP
                }

            return json_data

        @classmethod
        def create(cls):
            """Sends the PUT request to create all stored HY_Result_Graph objects in Midas."""
            if cls.data:
                MidasAPI("PUT", "/db/HHND", cls.json())

        @staticmethod
        def get():
            """Retrieves the HY_Result_Graph configuration from Midas."""
            return MidasAPI("GET", "/db/HHND")

        @classmethod
        def sync(cls):
            """Fetches data from Midas and reconstructs the local class instances."""
            resp = cls.get()
            if resp and 'HHND' in resp and resp['HHND'] and resp['HHND'] != {'message': ''}:
                cls.clear()
                for id, val in resp['HHND'].items():
                    cls(
                        node_id=int(val.get("NODE_KEY")),
                        Stress_component=_Reverse_Map_Stress_Components.get(val.get("COMP")),
                        id = int(id)
                    )

        @staticmethod
        def delete():
            """Deletes all HY_Result_Graph objects from the active Midas database."""
            MidasAPI("DELETE", "/db/HHND")
            HoH.HY_Result_Graph.clear()

    class CS:
        @staticmethod
        def create():
            if HoH.CS.STAGE.stages != []: 
                HoH.CS.STAGE.create()
        
        @staticmethod
        def clear():
            HoH.CS.STAGE.clear()

        class STAGE:
            stages: list['HoH.CS.STAGE'] = []
            _maxID_: int = 0
            _maxNO_: int = 0
            _isSync_: bool = False

            def __init__(self, 
                         name: str,
                         initial_temp: float = None,
                         add_step: list[float] = None,
                         act_elem: list[str] = None,
                         act_bngr: list[str] = None,
                         dact_bngr: list[str] = None,
                         act_load: list[str] = None,
                         act_day: list[str] = None,
                         dact_load: list[str] = None,
                         dact_day: list[str] = None,
                         id: int = None):
                """
                Construction Stage define for Heat of Hydration.
                
                Parameters:
                    name: Hydration Stage Name
                    initial_temp: Initial temperature value. If None, bINITAL_TEMP will be False.
                    add_step: List of additional time steps (in hours).
                    act_elem: Structure group name or list to activate.
                    act_bngr: Boundary group name or list to activate.
                    dact_bngr: Boundary group name or list to deactivate.
                    act_load: Load group name or list to activate.
                    act_day: Day strings for load activation (e.g. "10.000000").
                    dact_load: Load group name or list to deactivate.
                    dact_day: Day strings for load deactivation.
                    id: The construction stage ID (optional)
                """

                self.NAME = name
                self.bINITAL_TEMP = initial_temp is not None
                self.INITIAL_TEMP = initial_temp if initial_temp is not None else 0
                self.ADD_STEP = [] if add_step is None else add_step

                if id is None:
                    self.ID = HoH.CS.STAGE._maxID_ + 1
                    self.NO = HoH.CS.STAGE._maxNO_ + 1
                else:
                    self.ID = id
                    self.NO = id
                HoH.CS.STAGE._maxNO_ = max(HoH.CS.STAGE._maxNO_, self.NO)
                HoH.CS.STAGE._maxID_ = max(HoH.CS.STAGE._maxID_, self.ID)

                self.act_structure_groups = []  
                self.act_boundary_groups = []  
                self.deact_boundary_groups = []  
                self.act_load_groups = []  
                self.deact_load_groups = []  

                if act_elem:
                    if not isinstance(act_elem, list):
                        act_elem = [act_elem]
                    self.act_structure_groups.extend(act_elem)

                if act_bngr:
                    if not isinstance(act_bngr, list):
                        act_bngr = [act_bngr]
                    self.act_boundary_groups.extend(act_bngr)

                if dact_bngr:
                    if not isinstance(dact_bngr, list):
                        dact_bngr = [dact_bngr]
                    self.deact_boundary_groups.extend(dact_bngr)

                if act_load:
                    if not isinstance(act_load, list):
                        act_load = [act_load]
                        act_day = [act_day if act_day is not None else "0.000000"]
                    else:
                        if act_day is None:
                            act_day = ["0.000000"] * len(act_load)
                        elif not isinstance(act_day, list):
                            act_day = [act_day] * len(act_load)
                    
                    for i, group in enumerate(act_load):
                        day = str(act_day[i]) if i < len(act_day) else "0.000000"
                        self.act_load_groups.append({"LOAD_NAME": group, "DAY": day})

                if dact_load:
                    if not isinstance(dact_load, list):
                        dact_load = [dact_load]
                        dact_day = [dact_day if dact_day is not None else "0.000000"]
                    else:
                        if dact_day is None:
                            dact_day = ["0.000000"] * len(dact_load)
                        elif not isinstance(dact_day, list):
                            dact_day = [dact_day] * len(dact_load)
                    
                    for i, group in enumerate(dact_load):
                        day = str(dact_day[i]) if i < len(dact_day) else "0.000000"
                        self.deact_load_groups.append({"LOAD_NAME": group, "DAY": day})

                HoH.CS.STAGE.stages.append(self)

            @classmethod
            def json(cls):
                """Converts HoH Construction Stage data to JSON format"""
                json_payload = {"Assign": {}}
                
                for csa in cls.stages:
                    stage_data = {
                        "NAME": csa.NAME,
                        "bINITAL_TEMP": csa.bINITAL_TEMP,
                        "ADD_STEP": csa.ADD_STEP
                    }
                    
                    if csa.bINITAL_TEMP:
                        stage_data["INITIAL_TEMP"] = csa.INITIAL_TEMP
                    
                    stage_data["ACT_ELEM"] = csa.act_structure_groups
                    stage_data["ACT_BNGR"] = csa.act_boundary_groups
                    stage_data["DACT_BNGR"] = csa.deact_boundary_groups
                    stage_data["ACT_LOAD"] = csa.act_load_groups
                    stage_data["DACT_LOAD"] = csa.deact_load_groups
                        
                    json_payload["Assign"][str(csa.ID)] = stage_data
                
                return json_payload

            @classmethod
            def create(cls):
                """Creates heat of hydration construction stages in the database"""
                if HoH.CS.STAGE._isSync_:
                    MidasAPI("DELETE", "/db/hstg")
                MidasAPI("PUT", "/db/hstg", cls.json())

            @classmethod
            def get(cls):
                """Gets heat of hydration construction stage data from the database"""
                return MidasAPI("GET", "/db/hstg")

            @classmethod
            def sync(cls):
                """Updates the HoH.CS class with data from the database"""
                cls.clear()
                a = cls.get()
                if a != {'message': ''}:
                    if "HSTG" in a:
                        stag_data_dict = a["HSTG"]
                    else:
                        return  
                        
                    for stag_id, stag_data in stag_data_dict.items():
                        name = stag_data.get("NAME")
                        b_init = stag_data.get("bINITAL_TEMP", False)
                        init_temp = stag_data.get("INITIAL_TEMP", None) if b_init else None
                        add_step = stag_data.get("ADD_STEP", [])
                        
                        # Create a new CS object
                        new_cs = HoH.CS.STAGE(
                            name=name,
                            initial_temp=init_temp,
                            add_step=add_step,
                            id=int(stag_id)
                        )

                        HoH.CS.STAGE.stages.pop()
                        
                        new_cs.act_structure_groups = stag_data.get("ACT_ELEM", [])
                        new_cs.act_boundary_groups = stag_data.get("ACT_BNGR", [])
                        new_cs.deact_boundary_groups = stag_data.get("DACT_BNGR", [])
                        new_cs.act_load_groups = stag_data.get("ACT_LOAD", [])
                        new_cs.deact_load_groups = stag_data.get("DACT_LOAD", [])
                        
                        HoH.CS.STAGE.stages.append(new_cs)

                    sorted_stgs = sorted(HoH.CS.STAGE.stages, key=lambda x: x.ID)
                    HoH.CS.STAGE.stages = sorted_stgs
                    HoH.CS.STAGE._isSync_ = True

            @classmethod
            def delete(cls):
                """Deletes all HoH construction stages from the database"""
                cls.clear()
                return MidasAPI("DELETE", "/db/hstg")

            @classmethod
            def clear(cls):
                """Clears all HoH construction stages locally"""
                cls.stages = []
                cls._maxID_ = 0
                cls._maxNO_ = 0
                cls._isSync_ = False

            
            

            