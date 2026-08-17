from ._mapi import MidasAPI
from typing import Literal

_DataType = Literal["Normalized Accel" ,  "Acceleration", "Force", "Moment", "Normal" ]
_runge_kuttamethod = Literal["FEHLBERG" ,  "CASHKARP" ]

class TH:

    class GroundAccel:

        data = []
        _ids = [0]

        @classmethod
        def json(cls):
            js_data = {"Assign": {}}
            for func in cls.data:
                js_data["Assign"][str(func.ID)] = func.__json()
            return js_data
        
        @classmethod
        def create(cls):
            if cls.data:
                MidasAPI('PUT', '/db/THGA', cls.json())

        def __json(self): 
            js_data = {
                "NAME": self.TH_Case 
            }
            
            if self.FUNCTION_X is not None:
                js_data["FUNCX"] = self.FUNCTION_X
                js_data["SCALEX"] = self.SCALE_X
                js_data["ATIMEX"] = self.ARRIVAL_TIME_X
            else:
                js_data["FUNCX"] = ''
                js_data["SCALEX"] = 1
                js_data["ATIMEX"] = 1        
            
            if self.FUNCTION_Y is not None:
                js_data["FUNCY"] = self.FUNCTION_Y
                js_data["SCALEY"] = self.SCALE_Y
                js_data["ATIMEY"] = self.ARRIVAL_TIME_Y
            else:
                js_data["FUNCY"] = ''
                js_data["SCALEY"] = 1
                js_data["ATIMEY"] = 1
                
            if self.FUNCTION_Z is not None:
                js_data["FUNCZ"] = self.FUNCTION_Z
                js_data["SCALEZ"] = self.SCALE_Z
                js_data["ATIMEZ"] = self.ARRIVAL_TIME_Z
            else:
                js_data["FUNCZ"] = ''
                js_data["SCALEZ"] = 1
                js_data["ATIMEZ"] = 1

            js_data["ANGLE"] = self.ANGLE

            return js_data

        @staticmethod
        def get():
            return MidasAPI("GET", "/db/THGA")

        @staticmethod
        def clear():
            """Delete data from Python"""
            TH.GroundAccel.data = []
            TH.GroundAccel._ids = [0]

        @staticmethod
        def delete():
            MidasAPI("DELETE", "/db/THGA")
            TH.GroundAccel.clear()

        def __init__(self, TH_Case, Angle, FuncX=None, ScaleX=1, ATimeX=0, FuncY=None, ScaleY=1, ATimeY=0, FuncZ=None, ScaleZ=1, ATimeZ=0, id=None):
            self.TH_Case = TH_Case 
            self.ANGLE = Angle
            
            if FuncX is not None:
                self.FUNCTION_X = FuncX
                self.SCALE_X = ScaleX
                self.ARRIVAL_TIME_X = ATimeX
            else:
                self.FUNCTION_X = None
                self.SCALE_X = None
                self.ARRIVAL_TIME_X = None               
                
            if FuncY is not None:
                self.FUNCTION_Y = FuncY         
                self.SCALE_Y = ScaleY           
                self.ARRIVAL_TIME_Y = ATimeY
            else:
                self.FUNCTION_Y = None         
                self.SCALE_Y = None           
                self.ARRIVAL_TIME_Y = None                   
                
            if FuncZ is not None:
                self.FUNCTION_Z = FuncZ         
                self.SCALE_Z = ScaleZ           
                self.ARRIVAL_TIME_Z = ATimeZ     
            else:
                self.FUNCTION_Z = None         
                self.SCALE_Z = None           
                self.ARRIVAL_TIME_Z = None   

            if id is None:
                self.ID = max(TH.GroundAccel._ids) + 1
            else:
                self.ID = id

            TH.GroundAccel.data.append(self)
            TH.GroundAccel._ids.append(self.ID)

        @classmethod
        def sync(cls):
            cls.data = []
            cls._ids = [0]
            
            a = cls.get()
            if a and 'THGA' in a and a != {'message': ''}:
                for item_id, item_data in a['THGA'].items():
                    name = item_data.get('NAME')
                    
                    func_x = item_data.get('FUNCX')
                    if not func_x: 
                        func_x, scale_x, atime_x = None, None, None
                    else:
                        scale_x = item_data.get('SCALEX')
                        atime_x = item_data.get('ATIMEX')
                        
                    func_y = item_data.get('FUNCY')
                    if not func_y:
                        func_y, scale_y, atime_y = None, None, None
                    else:
                        scale_y = item_data.get('SCALEY')
                        atime_y = item_data.get('ATIMEY')
                        
                    func_z = item_data.get('FUNCZ')
                    if not func_z:
                        func_z, scale_z, atime_z = None, None, None
                    else:
                        scale_z = item_data.get('SCALEZ')
                        atime_z = item_data.get('ATIMEZ')
                        
                    angle = item_data.get('ANGLE', 0.0)
                    
                    cls(TH_Case=name, Angle=angle,FuncX=func_x, ScaleX=scale_x,ATimeX=atime_x,FuncY=func_y,ScaleY=scale_y,ATimeY=atime_y,FuncZ=func_z,ScaleZ=scale_z,ATimeZ=atime_z,id=int(item_id))
    
    class TimeVaryingStaticLoad:
        data = []
        _ids = [0]

        @classmethod
        def json(cls):
            js_data = {"Assign": {}}
            for item in cls.data:
                js_data["Assign"][str(item.ID)] = item.__json()
            return js_data
        
        @classmethod
        def create(cls):
            if cls.data:
                MidasAPI('PUT', '/db/THSL', cls.json())

        def __json(self):
            return {
                "THIS_LCNAME": self.TH_Case,
                "SLOAD": self.STATIC_LOAD_CASE, 
                "THIS_FUNCNAME": self.THIS_FUNCNAME,
                "ATIME": self.ATIME,
                "SCALE": self.SCALE
            }

        @staticmethod
        def get():
            return MidasAPI('GET', '/db/THSL')

        @staticmethod
        def clear():
            """Delete data from Python"""
            TH.TimeVaryingStaticLoad.data = []
            TH.TimeVaryingStaticLoad._ids = [0]

        @staticmethod
        def delete():
            MidasAPI("DELETE", "/db/THSL")
            TH.TimeVaryingStaticLoad.clear()

        def __init__(self, TH_Case, StaticLoadCase, FunctionName, Scale, ArrivalTime, id=None):
            self.TH_Case = TH_Case  
            self.STATIC_LOAD_CASE = StaticLoadCase  
            self.THIS_FUNCNAME = FunctionName
            self.SCALE = Scale
            self.ATIME = ArrivalTime

            if id is None:
                self.ID = max(TH.TimeVaryingStaticLoad._ids) + 1
            else:
                self.ID = id

            TH.TimeVaryingStaticLoad.data.append(self)
            TH.TimeVaryingStaticLoad._ids.append(self.ID)

        @classmethod
        def sync(cls):
            cls.data = []
            cls._ids = [0]
            
            a = cls.get()
            
            if a and 'THSL' in a and a != {'message': ''}:
                for item_id, item_data in a['THSL'].items():
                    lc_name = item_data.get('THIS_LCNAME')
                    sload = item_data.get('SLOAD')  
                    func_name = item_data.get('THIS_FUNCNAME')
                    scale = item_data.get('SCALE')
                    atime = item_data.get('ATIME')
                    
                    cls(TH_Case=lc_name,StaticLoadCase=sload, FunctionName=func_name,Scale=scale,ArrivalTime=atime,id=int(item_id))
    
    class DynamicNodalLoad:

        data = []
        _ids = [0]

        @classmethod
        def json(cls):
            js_data = {"Assign": {}}
            for item in cls.data:
                node_key = str(item.Node)
                if node_key not in js_data["Assign"]:
                    js_data["Assign"][node_key] = {"ITEMS": []}
                
                js_data["Assign"][node_key]["ITEMS"].append(item.__json())
            return js_data
        
        @classmethod
        def create(cls):
            if cls.data:
                MidasAPI('PUT', '/db/THNL', cls.json())

        def __json(self):
            return {
                "ID": self.ID,
                "THLCNAME": self.TH_Case,
                "FUNC_NAME": self.THIS_FUNCNAME,
                "DIR": self.DIR,
                "ARRIVAL_TIME": self.ATIME,
                "SCALE_FACTOR": self.SCALE
            }

        @staticmethod
        def get():
            return MidasAPI('GET', '/db/THNL')

        @staticmethod
        def clear():
            """Delete data from Python"""
            TH.DynamicNodalLoad.data = []
            TH.DynamicNodalLoad._ids = [0]

        @staticmethod
        def delete():
            MidasAPI("DELETE", "/db/THNL")
            TH.DynamicNodalLoad.clear()

        def __init__(self, Node, TH_Case, FunctionName, Direction, ArrivalTime, ScaleFactor, id=None):

            if isinstance(Node, (list, tuple, set)):
                for nID in Node:
                    self.__class__(nID, TH_Case, FunctionName, Direction, ArrivalTime, ScaleFactor, id)
                return

            self.Node = int(Node)
            self.TH_Case = TH_Case  
            self.THIS_FUNCNAME = FunctionName
            self.DIR = Direction
            self.ATIME = ArrivalTime
            self.SCALE = ScaleFactor

            if id is None:
                self.ID = max(TH.DynamicNodalLoad._ids) + 1
            else:
                self.ID = id

            TH.DynamicNodalLoad.data.append(self)
            TH.DynamicNodalLoad._ids.append(self.ID)

        @classmethod
        def sync(cls):
            cls.data = []
            cls._ids = [0]
            
            a = cls.get()
            
            if a and 'THNL' in a and a != {'message': ''}:
                for node_id, node_data in a['THNL'].items():
                    for item_data in node_data.get('ITEMS', []):
                        item_id = item_data.get('ID', 0)
                        th_case = item_data.get('THLCNAME')
                        func_name = item_data.get('FUNC_NAME')
                        direction = item_data.get('DIR')
                        atime = item_data.get('ARRIVAL_TIME')
                        scale = item_data.get('SCALE_FACTOR')
                        
                        cls(Node=int(node_id), TH_Case=th_case, FunctionName=func_name, Direction=direction, ArrivalTime=atime, ScaleFactor=scale, id=item_id)
    
    class Damping:
    
        class Modal:
            def __init__(self, dampRatioAllMode=0.05, ModeDampingOverrides: list = None):
                """
                ModeDampingOverrides: optional list of (ModeNumber, DampingRatio) tuples,
                e.g. [(1, 0.006), (2, 0.007)] -> maps to the "aDAMP" array.
                """
                self.DAMP_RATIO = dampRatioAllMode
                self.MODE_OVERRIDES = ModeDampingOverrides

            def _json(self):
                _js = {
                    "bDAMP": True,
                    "iMDTYPE": 1,
                    "DALL": self.DAMP_RATIO,
                }

                if self.MODE_OVERRIDES:
                    _js["aDAMP"] = [
                        {"iMODE": mode, "DAMPING": ratio}
                        for mode, ratio in self.MODE_OVERRIDES
                    ]

                return _js
            
        
        class MassStiffness:
            def __init__(self, inpType: int = 1, massProp: float = None, stiffProp: float = None,
                        freq1: float = None, damp1: float = 0, freq2: float = None, damp2: float = 0,
                        period1: float = None, period2: float = None):

                self.DAMP_TYPE = inpType

                self.MASS_PROP = massProp
                self.STIFF_PROP = stiffProp

                self.__bMASS = False if self.MASS_PROP is None else True
                self.__bSTIFF = False if self.STIFF_PROP is None else True

                self.__MASS = 0 if self.MASS_PROP is None else massProp
                self.__STIFF = 0 if self.STIFF_PROP is None else stiffProp

                # --- Infer calc method from which params were passed ---
                _usesPeriod = period1 is not None or period2 is not None
                _usesFreq = freq1 is not None or freq2 is not None

                if _usesPeriod and _usesFreq:
                    raise ValueError("Provide either freq1/freq2 OR period1/period2, not both.")

                if _usesPeriod:
                    self.CALC_METHOD = 2  # Period
                    self.FREQ_1 = period1 if period1 is not None else 0
                    self.FREQ_2 = period2 if period2 is not None else 0
                else:
                    self.CALC_METHOD = 1  # Frequency (default)
                    self.FREQ_1 = freq1 if freq1 is not None else 0
                    self.FREQ_2 = freq2 if freq2 is not None else 0

                self.DAMP_1 = damp1
                self.DAMP_2 = damp2

            def _json(self):

                _js = {
                    "bDAMP": True,
                    "iMDTYPE": 2,
                    "iCOEF": self.DAMP_TYPE,
                    "bMASSP": self.__bMASS,
                    "bSTIFFP": self.__bSTIFF,
                }
                if self.DAMP_TYPE == 2:
                    _js['iCALC'] = self.CALC_METHOD
                    _js['FP1'] = self.FREQ_1
                    _js['DR1'] = self.DAMP_1
                    _js['FP2'] = self.FREQ_2
                    _js['DR2'] = self.DAMP_2
                    _js["bMASSP"] = True
                    _js["bSTIFFP"] = True

                else:
                    _js['MASSC'] = self.__MASS
                    _js['STIFFC'] = self.__STIFF

                return _js
            
        class StrainEnergy:
            def __init__(self):
                pass

            def _json(self):
                _js = {
                    "bDAMP": True,
                    "iMDTYPE": 3,
                }
                
                return _js  

        class ElementMassStiffness:
            def __init__(self):
                pass

            def _json(self):
                _js = {
                    "bDAMP": True,
                    "iMDTYPE": 4,
                }
                
                return _js      
    
    class MultipleSupportExcitation:
        
        data = []
        _ids = [0]

        @classmethod
        def json(cls):
            js_data = {"Assign": {}}
            for item in cls.data:
                node_key = str(item.Node)
                if node_key not in js_data["Assign"]:
                    js_data["Assign"][node_key] = {"ITEMS": []}
                
                js_data["Assign"][node_key]["ITEMS"].append(item.__json())
            return js_data
        
        @classmethod
        def create(cls): #has similar behaviour to MAPI 2430
            if cls.data:
                MidasAPI('PUT', '/db/THMS', cls.json())

        def __json(self):
            js_data = {
                "ID": self.ID,
                "LCNAME": self.TH_Case,
                "ANGLE": self.ANGLE
            }
            
            if self.FUNCTION_X is not None:
                js_data["FUNCX"] = self.FUNCTION_X
                js_data["SCALEX"] = self.SCALE_X
                js_data["ATIMEX"] = self.ARRIVAL_TIME_X
            else:
                js_data["FUNCX"] = ''
                js_data["SCALEX"] = 1
                js_data["ATIMEX"] = 1
                
            if self.FUNCTION_Y is not None:
                js_data["FUNCY"] = self.FUNCTION_Y
                js_data["SCALEY"] = self.SCALE_Y
                js_data["ATIMEY"] = self.ARRIVAL_TIME_Y
            else:
                js_data["FUNCY"] = ''
                js_data["SCALEY"] = 1
                js_data["ATIMEY"] = 1

            if self.FUNCTION_Z is not None:
                js_data["FUNCZ"] = self.FUNCTION_Z
                js_data["SCALEZ"] = self.SCALE_Z
                js_data["ATIMEZ"] = self.ARRIVAL_TIME_Z
            else:
                js_data["FUNCZ"] = ''
                js_data["SCALEZ"] = 1
                js_data["ATIMEZ"] = 1

            return js_data

        @staticmethod
        def get():
            return MidasAPI('GET', '/db/THMS')

        @staticmethod
        def clear():
            """Delete data from Python"""
            TH.MultipleSupportExcitation.data = []
            TH.MultipleSupportExcitation._ids = [0]

        @staticmethod
        def delete():
            MidasAPI("DELETE", "/db/THMS")
            TH.MultipleSupportExcitation.clear()

        def __init__(self, Node, TH_Case, Angle=0.0, FuncX=None, ScaleX=None, ATimeX=0.0, FuncY=None, ScaleY=None, ATimeY=0.0, FuncZ=None, ScaleZ=None, ATimeZ=0.0, id=None):
            
            if isinstance(Node, (list, tuple, set)):
                for nID in Node:
                    self.__class__(nID, TH_Case, Angle, FuncX, ScaleX, ATimeX, FuncY, ScaleY, ATimeY, FuncZ, ScaleZ, ATimeZ, id)
                return

            self.Node = int(Node)
            self.TH_Case = TH_Case
            self.ANGLE = Angle

            if FuncX is not None:
                self.FUNCTION_X = FuncX
                self.SCALE_X = ScaleX
                self.ARRIVAL_TIME_X = ATimeX
            else:
                self.FUNCTION_X = None
                self.SCALE_X = None
                self.ARRIVAL_TIME_X = None

            if FuncY is not None:
                self.FUNCTION_Y = FuncY
                self.SCALE_Y = ScaleY
                self.ARRIVAL_TIME_Y = ATimeY
            else:
                self.FUNCTION_Y = None
                self.SCALE_Y = None
                self.ARRIVAL_TIME_Y = None

            if FuncY is not None:
                self.FUNCTION_Z = FuncZ
                self.SCALE_Z = ScaleZ
                self.ARRIVAL_TIME_Z = ATimeZ
            else:
                self.FUNCTION_Z = None
                self.SCALE_Z = None
                self.ARRIVAL_TIME_Z = None    

            if id is None:
                self.ID = max(TH.MultipleSupportExcitation._ids) + 1
            else:
                self.ID = id

            TH.MultipleSupportExcitation.data.append(self)
            TH.MultipleSupportExcitation._ids.append(self.ID)

        @classmethod
        def sync(cls):
            cls.data = []
            cls._ids = [0]
            
            a = cls.get()
            
            if a and 'THMS' in a and a != {'message': ''}:
                for node_id, node_data in a['THMS'].items():
                    for item_data in node_data.get('ITEMS', []):
                        item_id = item_data.get('ID', 0)
                        th_case = item_data.get('LCNAME')
                        angle = item_data.get('ANGLE', 0.0)
                        
                        func_x = item_data.get('FUNCX')
                        scale_x = item_data.get('SCALEX')
                        atime_x = item_data.get('ATIMEX', 0.0)
                        
                        func_y = item_data.get('FUNCY')
                        scale_y = item_data.get('SCALEY')
                        atime_y = item_data.get('ATIMEY', 0.0)
                        
                        func_z = item_data.get('FUNCZ')
                        scale_z = item_data.get('SCALEZ')
                        atime_z = item_data.get('ATIMEZ', 0.0)
                        
                        cls(Node=int(node_id), TH_Case=th_case, Angle=angle, FuncX=func_x, ScaleX=scale_x, ATimeX=atime_x, FuncY=func_y, ScaleY=scale_y, ATimeY=atime_y, FuncZ=func_z, ScaleZ=scale_z, ATimeZ=atime_z, id=item_id)
    
    class InitialLoad_Control:
        """
        Initial Load (Global Control) settings for Time History Load Cases.
        """

        def __init__(
            self,
            Use_Initial_Load: bool = True,
            Cumulate_DVA_Results: bool = False,
            Keep_Final_Step_Loads_Constant: bool = False,
            Geometricnonlinearity_type: bool = False
        ):
            self.use_initial_load = Use_Initial_Load
            self.bDVA = Cumulate_DVA_Results
            self.bKEEP = Keep_Final_Step_Loads_Constant
            self.__iGEOM = 1 if Geometricnonlinearity_type else 0

        def _json(self) -> dict:
            _js = {
                "iGEOM": self.__iGEOM,
                "bSUBSEQ": False,
                "INITMETHOD": "INIT",
                # Per spec: 0 = Use Initial Load, 1 = Not use Initial Load
                "INITLOAD": 0 if self.use_initial_load else 1,
            }

            if self.use_initial_load:
                _js["bDVA"] = self.bDVA
                _js["bKEEP"] = self.bKEEP

            return _js

    class Subsequent_Control:
        """
        Subsequent control settings for Time History Load Cases.
        """

        def __init__(
            self, 
            load_case: list = None, 
            Initial_element_forces_table: bool = False, 
            Initial_forces_geometric_stiffness: bool = False, 
            Geometricnonlinearity_type: bool = False
        ):
            self.load_case = load_case
            self.init_elem_forces = Initial_element_forces_table
            self.init_geom_stiffness = Initial_forces_geometric_stiffness
            self.geom_type = Geometricnonlinearity_type
    
            self.__iGEOM = 1 if self.geom_type else 0 

        def _json(self) -> dict:
            _js = {
                "iGEOM": self.__iGEOM
            }
    
            if not any([self.load_case, self.init_elem_forces, self.init_geom_stiffness]):
                _js["bSUBSEQ"] = False
                return _js
                
            _js["bSUBSEQ"] = True
    
            if self.load_case is not None:
                _js["SUBSEQ"] = 0
                lctype = self.load_case[0]
                lcname = self.load_case[1]
                _js["LCTYPE"] = lctype
                _js["CASE"] = lcname
                if lctype == "TH":
                    _js["bDVA"] = self.load_case[2] if len(self.load_case) > 2 else False
                    _js["bKEEP"] = self.load_case[3] if len(self.load_case) > 3 else False
    
            elif self.init_elem_forces:
                if self.__iGEOM != 0:
                    raise ValueError("Initial_element_forces_table (SUBSEQ=1) can only be used when Geometricnonlinearity_type is False (iGEOM=0).")
                _js["SUBSEQ"] = 1
    
            elif self.init_geom_stiffness:
                if self.__iGEOM != 1:
                    raise ValueError("Initial_forces_geometric_stiffness (SUBSEQ=2) can only be used when Geometricnonlinearity_type is True (iGEOM=1).")
                _js["SUBSEQ"] = 2
    
            return _js

    class NonlinearIteration_Control:
        """
        Nonlinear Iteration Control settings for Time History Load Cases.
        """

        def __init__(
            self,
            Maximum_Iteration: int = 10,
            Minimum_Step_Size: float = 1e-05,
            Max_num_of_sub_steps: int = 10,
            Displacement_norm: float = None,
            Force_norm: float = None,
            Energy_norm: float = None,
            Startline_search_Iteration: int = None,
            Runge_kutta_method:_runge_kuttamethod = "FEHLBERG",
            Tolerance: float = 1e-08,
            Check_Convergence: bool = True
        ):
            self.Maximum_Iteration = Maximum_Iteration
            self.Minimum_Step_Size = Minimum_Step_Size
            self.Max_num_of_sub_steps = Max_num_of_sub_steps
            self.Tolerance = Tolerance
            self.Check_Convergence = Check_Convergence

            self.Runge_kutta_method = str(Runge_kutta_method).upper().strip()
            if self.Runge_kutta_method not in ["FEHLBERG", "CASHKARP"]:
                raise ValueError("Runge_kutta_method must be either 'FEHLBERG' or 'CASHKARP'")

            self.bDN = Displacement_norm is not None
            self.Displacement_norm = Displacement_norm if self.bDN else 0.001
            
            self.bFN = Force_norm is not None
            self.Force_norm = Force_norm if self.bFN else 0.001
            
            self.bEN = Energy_norm is not None
            self.Energy_norm = Energy_norm if self.bEN else 0.001
            
            self.bULSM = Startline_search_Iteration is not None
            self.Startline_search_Iteration = Startline_search_Iteration if self.bULSM else 5

        def _json(self, include_min_step_size: bool = True) -> dict:
            iRKM = 0 if self.Runge_kutta_method == "FEHLBERG" else 1

            _js = {
                "bITER": True,
                "bCONV": self.Check_Convergence,
                "iMAXITER": self.Maximum_Iteration,
                "iMSTEP": self.Max_num_of_sub_steps,
                "bDN": self.bDN,
                "DN": self.Displacement_norm,
                "bFN": self.bFN,
                "FN": self.Force_norm,
                "bEN": self.bEN,
                "EN": self.Energy_norm,
                "iRKM": iRKM,
                "dTOL": self.Tolerance,
                "bULSM": self.bULSM,
                "ULSM": self.Startline_search_Iteration
            }

            # MINSSS (Minimum Step Size) only applies to dynamic (Modal /
            # Direct Integration) nonlinear iteration control, not Static.
            if include_min_step_size:
                _js["MINSSS"] = self.Minimum_Step_Size

            return _js
    
    class Case:
        cases = []
        _ids = [0]

        @classmethod
        def json(cls):
            js_data = {"Assign": {}}
            for item in cls.cases:
                js_data["Assign"][str(item.ID)] = item._json()
            return js_data
        
        @classmethod
        def create(cls):
            if cls.cases:
                MidasAPI('PUT', '/db/THIS', cls.json())

        @classmethod
        def _register(cls, instance, id):
            if id is None:
                instance.ID = max(cls._ids) + 1
            else:
                instance.ID = id
            cls._ids.append(instance.ID)
            cls.cases.append(instance)

        @staticmethod
        def get():
            return MidasAPI("GET", "/db/THIS")

        @staticmethod
        def clear():
            """Delete data from Python"""
            TH.Case.cases = []
            TH.Case._ids = [0]

        @staticmethod
        def delete():
            MidasAPI("DELETE", "/db/THIS")
            TH.Case.clear()

        # ------------------------------------------------------------------
        # Helpers used by sync() to rebuild control objects from raw JSON
        # ------------------------------------------------------------------
        @staticmethod
        def _parse_load_control(common):
            if common.get('INITMETHOD') == 'INIT':
                use_initial = common.get('INITLOAD', 0) == 0
                return TH.InitialLoad_Control(
                    Use_Initial_Load=use_initial,
                    Cumulate_DVA_Results=common.get('bDVA', False),
                    Keep_Final_Step_Loads_Constant=common.get('bKEEP', False),
                    Geometricnonlinearity_type=common.get('iGEOM', 0) == 1
                )

            if not common.get('bSUBSEQ', False):
                return TH.Subsequent_Control(
                    Geometricnonlinearity_type=common.get('iGEOM', 0) == 1
                )

            subseq = common.get('SUBSEQ', 0)
            geom = common.get('iGEOM', 0) == 1

            if subseq == 1:
                return TH.Subsequent_Control(
                    Initial_element_forces_table=True,
                    Geometricnonlinearity_type=geom
                )
            elif subseq == 2:
                return TH.Subsequent_Control(
                    Initial_forces_geometric_stiffness=True,
                    Geometricnonlinearity_type=geom
                )
            else:
                lctype = common.get('LCTYPE')
                lcname = common.get('CASE')
                load_case = [lctype, lcname]
                if lctype == 'TH':
                    load_case.append(common.get('bDVA', False))
                    load_case.append(common.get('bKEEP', False))
                return TH.Subsequent_Control(
                    load_case=load_case,
                    Geometricnonlinearity_type=geom
                )

        @staticmethod
        def _parse_damping(item_data, common):
            iMDTYPE = common.get('iMDTYPE')

            if iMDTYPE == 1:
                adamp = item_data.get('aDAMP')
                overrides = None
                if adamp:
                    overrides = [(d.get('iMODE'), d.get('DAMPING')) for d in adamp]
                return TH.Damping.Modal(
                    dampRatioAllMode=item_data.get('DALL', 0.05),
                    ModeDampingOverrides=overrides
                )

            elif iMDTYPE == 2:
                iCOEF = item_data.get('iCOEF', 1)
                if iCOEF == 2:
                    return TH.Damping.MassStiffness(
                        inpType=2,
                        calcMethod=item_data.get('iCALC', 1),
                        freq1=item_data.get('FP1', 0),
                        damp1=item_data.get('DR1', 0),
                        freq2=item_data.get('FP2', 0),
                        damp2=item_data.get('DR2', 0)
                    )
                else:
                    return TH.Damping.MassStiffness(
                        inpType=1,
                        massProp=item_data.get('MASSC') if item_data.get('bMASSP') else None,
                        stiffProp=item_data.get('STIFFC') if item_data.get('bSTIFFP') else None
                    )

            elif iMDTYPE == 3:
                return TH.Damping.StrainEnergy()

            elif iMDTYPE == 4:
                return TH.Damping.ElementMassStiffness()

            return None

        @staticmethod
        def _parse_nl_iter(item_data):
            if 'iMAXITER' not in item_data and 'bITER' not in item_data:
                return None

            rkm = "CASHKARP" if item_data.get('iRKM', 0) == 1 else "FEHLBERG"

            return TH.NonlinearIteration_Control(
                Maximum_Iteration=item_data.get('iMAXITER', 10),
                Minimum_Step_Size=item_data.get('MINSSS', 1e-05),
                Max_num_of_sub_steps=item_data.get('iMSTEP', 10),
                Displacement_norm=item_data.get('DN') if item_data.get('bDN') else None,
                Force_norm=item_data.get('FN') if item_data.get('bFN') else None,
                Energy_norm=item_data.get('EN') if item_data.get('bEN') else None,
                Startline_search_Iteration=item_data.get('ULSM') if item_data.get('bULSM') else None,
                Runge_kutta_method=rkm,
                Tolerance=item_data.get('dTOL', 1e-08),
                Check_Convergence=item_data.get('bCONV', True)
            )

        @staticmethod
        def _parse_time_integration(item_data):
            iNMM = item_data.get('iNMM')
            if iNMM == 1:
                return "CONSTANT"
            elif iNMM == 3:
                return (item_data.get('GAMMA', 0.5), item_data.get('BETA', 0.25))
            return "LINEAR"

        @classmethod
        def sync(cls):
            cls.clear()

            a = cls.get()
            if not a or 'THIS' not in a or a == {'message': ''}:
                return

            for item_id, item_data in a['THIS'].items():
                common = item_data.get('COMMON', {})
                iATYPE = common.get('iATYPE')
                iAMETHOD = common.get('iAMETHOD')

                subsequent_control = cls._parse_load_control(common)

                if iATYPE == 1 and iAMETHOD == 1:
                    damping = cls._parse_damping(item_data, common)
                    th_type = 'Transient' if common.get('iTHTYPE', 1) == 1 else 'Periodic'
                    cls.LinearModal(
                        Name=common.get('NAME'),
                        THtype=th_type,
                        endTime=common.get('ENDTIME'),
                        timeIncrement=common.get('INC'),
                        stepIncOutput=common.get('iOUT'),
                        subsequent_control=subsequent_control,
                        damping_control=damping,
                        id=int(item_id)
                    )

                elif iATYPE == 2 and iAMETHOD == 1:
                    damping = cls._parse_damping(item_data, common)
                    nl_iter = cls._parse_nl_iter(item_data)
                    cls.NonLinearModal(
                        Name=common.get('NAME'),
                        endTime=common.get('ENDTIME'),
                        timeIncrement=common.get('INC'),
                        stepIncOutput=common.get('iOUT'),
                        subsequent_control=subsequent_control,
                        damping_control=damping,
                        NonlinearIteration_Control=nl_iter,
                        id=int(item_id)
                    )

                elif iATYPE == 1 and iAMETHOD == 2:
                    damping = cls._parse_damping(item_data, common)
                    tip = cls._parse_time_integration(item_data)
                    cls.LinearDirectInt(
                        Name=common.get('NAME'),
                        endTime=common.get('ENDTIME'),
                        timeIncrement=common.get('INC'),
                        stepIncOutput=common.get('iOUT'),
                        subsequent_control=subsequent_control,
                        damping_control=damping,
                        time_integration_params=tip,
                        id=int(item_id)
                    )

                elif iATYPE == 2 and iAMETHOD == 2:
                    damping = cls._parse_damping(item_data, common)
                    tip = cls._parse_time_integration(item_data)
                    nl_iter = cls._parse_nl_iter(item_data)
                    dm_update = "YES" if item_data.get("DMUPDATE") else "NO"
                    cls.NonLinearDirectInt(
                        Name=common.get('NAME'),
                        endTime=common.get('ENDTIME'),
                        timeIncrement=common.get('INC'),
                        stepIncOutput=common.get('iOUT'),
                        subsequent_control=subsequent_control,
                        damping_control=damping,
                        time_integration_params=tip,
                        NonlinearIteration_Control=nl_iter,
                        damping_matrix_update=dm_update,
                        id=int(item_id)
                    )

                elif iATYPE == 2 and iAMETHOD == 3:
                    nl_iter = cls._parse_nl_iter(item_data)

                    master_node = None
                    global_disp = 0
                    load_scale = 1

                    if item_data.get('iINCCTRL') == 1:
                        if item_data.get('iCTRL') == 1:
                            master_node = (
                                item_data.get('MNODE'),
                                item_data.get('MDIR'),
                                item_data.get('TINC')
                            )
                        else:
                            global_disp = item_data.get('TINC', 0)
                    else:
                        load_scale = item_data.get('SCALE', 1)

                    cls.NonLinearStatic(
                        Name=common.get('NAME'),
                        endTime=common.get('ENDTIME', 1),
                        incrementSteps=common.get('iISTEP', 1),
                        subsequent_control=subsequent_control,
                        load_control_scale_factor=load_scale,
                        global_control_maximum_translation_displacement=global_disp,
                        master_node_control=master_node,
                        load_output_option=item_data.get('bCUMULATE', False),
                        NonlinearIteration_Control=nl_iter,
                        id=int(item_id)
                    )
                # Any other iATYPE/iAMETHOD combination is not currently
                # represented by a Case subclass and is skipped.

        class LinearModal:
            def __init__(self, Name, THtype='Transient', endTime=1, timeIncrement=0.01, stepIncOutput=1, subsequent_control=None, damping_control=None, id=None):
                self.NAME = Name
                self.THtype = THtype
                self.endTime = endTime
                self.timeIncrement = timeIncrement
                self.stepIncOutput = stepIncOutput
                self.subsequent_control = subsequent_control
                self.damping_control = damping_control
                
                # Fixed line
                TH.Case._register(self, id)

            def _json(self):
                js = {
                    "COMMON": {
                        "NAME": self.NAME,
                        "DESC": "",
                        "iATYPE": 1,
                        "iAMETHOD": 1,
                        "iTHTYPE": 1 if self.THtype.upper() == 'TRANSIENT' else 2,
                        "ENDTIME": self.endTime,
                        "INC": self.timeIncrement,
                        "iOUT": self.stepIncOutput,
                        "INITLOAD": 0,
                        "INITMETHOD": "ORDER"
                    }
                }
                
                if self.subsequent_control:
                    js["COMMON"].update(self.subsequent_control._json())
                else:
                    js["COMMON"]["bSUBSEQ"] = False
                    js["COMMON"]["iGEOM"] = 0
                    
                if self.damping_control:
                    d_js = self.damping_control._json()
                    if "iMDTYPE" in d_js:
                        js["COMMON"]["iMDTYPE"] = d_js.pop("iMDTYPE")
                    if "bDAMP" in d_js: 
                        d_js.pop("bDAMP")
                    js.update(d_js)
                    
                return js

        class NonLinearModal:
            def __init__(self, Name, endTime=1, timeIncrement=0.01, stepIncOutput=1, subsequent_control=None, damping_control=None, NonlinearIteration_Control=None, id=None):
                self.NAME = Name
                self.endTime = endTime
                self.timeIncrement = timeIncrement
                self.stepIncOutput = stepIncOutput
                self.subsequent_control = subsequent_control
                self.damping_control = damping_control
                self.NonlinearIteration_Control = NonlinearIteration_Control
                
                # Fixed line
                TH.Case._register(self, id)

            def _json(self):
                js = {
                    "COMMON": {
                        "NAME": self.NAME,
                        "DESC": "",
                        "iATYPE": 2,
                        "iAMETHOD": 1,
                        "iTHTYPE": 1,
                        "ENDTIME": self.endTime,
                        "INC": self.timeIncrement,
                        "iOUT": self.stepIncOutput,
                        "INITLOAD": 0,
                        "INITMETHOD": "ORDER"
                    },
                    "DMUPDATE": False
                }
                
                if self.subsequent_control:
                    js["COMMON"].update(self.subsequent_control._json())
                else:
                    js["COMMON"]["bSUBSEQ"] = False
                    js["COMMON"]["iGEOM"] = 0
                    
                if self.damping_control:
                    d_js = self.damping_control._json()
                    if "iMDTYPE" in d_js:
                        js["COMMON"]["iMDTYPE"] = d_js.pop("iMDTYPE")
                    if "bDAMP" in d_js: 
                        d_js.pop("bDAMP")
                    js.update(d_js)
                    
                if self.NonlinearIteration_Control:
                    js.update(self.NonlinearIteration_Control._json())
                    
                return js

        class LinearDirectInt:
            def __init__(self, Name, endTime=1, timeIncrement=0.01, stepIncOutput=1, subsequent_control=None, damping_control=None, time_integration_params="LINEAR", id=None):
                self.NAME = Name
                self.endTime = endTime
                self.timeIncrement = timeIncrement
                self.stepIncOutput = stepIncOutput
                self.subsequent_control = subsequent_control
                self.damping_control = damping_control
                self.tip = time_integration_params
                
                # Fixed line
                TH.Case._register(self, id)

            def _json(self):
                js = {
                    "COMMON": {
                        "NAME": self.NAME,
                        "DESC": "",
                        "iATYPE": 1,
                        "iAMETHOD": 2,
                        "iTHTYPE": 1,
                        "ENDTIME": self.endTime,
                        "INC": self.timeIncrement,
                        "iOUT": self.stepIncOutput,
                        "INITLOAD": 0,
                        "INITMETHOD": "ORDER"
                    }
                }
                
                if self.subsequent_control:
                    js["COMMON"].update(self.subsequent_control._json())
                else:
                    js["COMMON"]["bSUBSEQ"] = False
                    js["COMMON"]["iGEOM"] = 0
                    
                if self.damping_control:
                    d_js = self.damping_control._json()
                    if "iMDTYPE" in d_js:
                        js["COMMON"]["iMDTYPE"] = d_js.pop("iMDTYPE")
                    if "bDAMP" in d_js: 
                        d_js.pop("bDAMP")
                    js.update(d_js)
                    
                if isinstance(self.tip, str):
                    val = self.tip.upper()
                    if val == "CONSTANT":
                        js["iNMM"] = 1
                    elif val == "LINEAR":
                        js["iNMM"] = 2
                elif isinstance(self.tip, (list, tuple)) and len(self.tip) == 2:
                    js["iNMM"] = 3
                    js["GAMMA"] = self.tip[0]
                    js["BETA"] = self.tip[1]
                    
                return js

        class NonLinearDirectInt:
            def __init__(self, Name, endTime=1, timeIncrement=0.01, stepIncOutput=1, subsequent_control=None, damping_control=None, time_integration_params="LINEAR", NonlinearIteration_Control=None, damping_matrix_update="NO", id=None):
                self.NAME = Name
                self.endTime = endTime
                self.timeIncrement = timeIncrement
                self.stepIncOutput = stepIncOutput
                self.subsequent_control = subsequent_control
                self.damping_control = damping_control
                self.tip = time_integration_params
                self.nl_iter = NonlinearIteration_Control
                self.dm_update = damping_matrix_update
                
                # Fixed line
                TH.Case._register(self, id)

            def _json(self):
                js = {
                    "COMMON": {
                        "NAME": self.NAME,
                        "DESC": "",
                        "iATYPE": 2,
                        "iAMETHOD": 2,
                        "iTHTYPE": 1,
                        "ENDTIME": self.endTime,
                        "INC": self.timeIncrement,
                        "iOUT": self.stepIncOutput,
                        "INITLOAD": 0,
                        "INITMETHOD": "ORDER"
                    },
                    "DMUPDATE": True if str(self.dm_update).upper() == "YES" else False
                }
                
                if self.subsequent_control:
                    js["COMMON"].update(self.subsequent_control._json())
                else:
                    js["COMMON"]["bSUBSEQ"] = False
                    js["COMMON"]["iGEOM"] = 0
                    
                if self.damping_control:
                    d_js = self.damping_control._json()
                    if "iMDTYPE" in d_js:
                        js["COMMON"]["iMDTYPE"] = d_js.pop("iMDTYPE")
                    if "bDAMP" in d_js: 
                        d_js.pop("bDAMP")
                    js.update(d_js)
                    
                if isinstance(self.tip, str):
                    val = self.tip.upper()
                    if val == "CONSTANT":
                        js["iNMM"] = 1
                    elif val == "LINEAR":
                        js["iNMM"] = 2
                elif isinstance(self.tip, (list, tuple)) and len(self.tip) == 2:
                    js["iNMM"] = 3
                    js["GAMMA"] = self.tip[0]
                    js["BETA"] = self.tip[1]
                    
                if self.nl_iter:
                    js.update(self.nl_iter._json())
                    
                return js

        class NonLinearStatic:
            def __init__(self, Name, endTime=1, incrementSteps=1, subsequent_control=None, load_control_scale_factor=1, global_control_maximum_translation_displacement=0, master_node_control=None, load_output_option=False, NonlinearIteration_Control=None, id=None):
                self.NAME = Name
                self.endTime = endTime
                self.incrementSteps = incrementSteps
                self.subsequent_control = subsequent_control
                self.load_scale = load_control_scale_factor
                self.global_disp = global_control_maximum_translation_displacement
                self.master_node = master_node_control
                self.load_output = load_output_option
                self.nl_iter = NonlinearIteration_Control
                
                # Fixed line
                TH.Case._register(self, id)

            def _json(self):
                js = {
                    "COMMON": {
                        "NAME": self.NAME,
                        "DESC": "",
                        "iATYPE": 2,
                        "iAMETHOD": 3,
                        "iTHTYPE": 1,
                        "ENDTIME": self.endTime,
                        "iISTEP": self.incrementSteps,
                        "iOUT": 1,
                        "INITLOAD": 0,
                        "INITMETHOD": "ORDER"
                    },
                    "bCUMULATE": self.load_output,
                    "DMUPDATE": False
                }
                
                if self.subsequent_control:
                    js["COMMON"].update(self.subsequent_control._json())
                else:
                    js["COMMON"]["bSUBSEQ"] = False
                    js["COMMON"]["iGEOM"] = 0
                    
                if self.master_node and len(self.master_node) == 3:
                    js["iINCCTRL"] = 1
                    js["iCTRL"] = 1
                    js["MNODE"] = self.master_node[0]
                    js["MDIR"] = self.master_node[1]
                    js["TINC"] = self.master_node[2]
                elif self.global_disp != 0:
                    js["iINCCTRL"] = 1
                    js["iCTRL"] = 0
                    js["TINC"] = self.global_disp
                else:
                    js["iINCCTRL"] = 0
                    js["SCALE"] = self.load_scale
                    
                if self.nl_iter:
                    if hasattr(self.nl_iter, '_json'):
                        # MINSSS does not apply to the Static nonlinear iteration control
                        js.update(self.nl_iter._json(include_min_step_size=False))
                    else:
                        default_iter = {
                            "bITER": True, "bCONV": True, "iMSTEP": 10, "iMAXITER": 10,
                            "bDN": True, "DN": 0.001, "bFN": True, "FN": 0.001,
                            "bEN": True, "EN": 0.001, "DMUPDATE": False, "iRKM": 0,
                            "dTOL": 1e-08, "bULSM": True, "ULSM": 5
                        }
                        js.update(default_iter)
                        
                return js
            
    class Function:
        functions = []
        _ids = [0]

        @classmethod
        def json(cls):
            js_data = {"Assign" : {}}
            for func in cls.functions:
                js_data["Assign"][func.ID] = func.__json()
            return js_data
        
        @classmethod
        def create(cls):
            if cls.functions:
                MidasAPI('PUT','/db/THFC',cls.json())

        def __init__(self,name,FuncData = [(0,0),(0.1,0.1)],data_type:_DataType='Normal',scaling=1,max_value=None,gravity=None,desc="",id=None):
            
            if gravity==None:
                from ._model import Model
                gravity = Model.gravity()
            
            
            if isinstance(data_type,str):
                _mapping = {
                    "Normalized Accel" : 1,
                    "Acceleration" : 2,
                    "Force" : 3,
                    "Moment" : 4,
                    "Normal" : 5
                }
                data_type = _mapping.get(data_type,1)

            if id is None:
                self.ID = max(TH.Function._ids)+1
            else:
                self.ID = id
            
            self.NAME = name
            self.TYPE = data_type
            self.CODE = "USER"
            self.SCALE_FACTOR = scaling
            self.MAX_VALUE = max_value
            self.GRAVITY = gravity
            self.DATA = FuncData
            self.DESC = desc

            TH.Function.functions.append(self)
            TH.Function._ids.append(self.ID)

        def __json(self):
            js_data = {
                    "NAME": self.NAME,
                    "FUNCTYPE" : 1,
                    "iTYPE": self.TYPE,
                    "DESC": self.DESC,
                    }
            if self.MAX_VALUE != None:
                js_data["iMETHOD"] = 1
                js_data["SCALE"] = self.MAX_VALUE
            else:
                js_data["iMETHOD"] = 0
                js_data["SCALE"] = self.SCALE_FACTOR
            
            js_data["GRAV"] = self.GRAVITY
            
            _aFunc = []
            for i in self.DATA:
                _aFunc.append({"TIME" : i[0] , "VALUE" : i[1]})
            js_data["aFUNCDATA"] = _aFunc

            return js_data

