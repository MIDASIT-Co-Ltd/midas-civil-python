from ._mapi import MidasAPI
from ._model import Model
from typing import Literal

_SpecType = Literal["Normalized Accel" ,  "Acceleration", "Velocity", "Displacement" ]

_ModalCombType = Literal['CQC','SRSS','ABS','Linear']
_InterpType = Literal['LINEAR','LOG']
_RSDir = Literal['XY','Z']

_INCode = Literal['IS1893(2016)','IS1893(2002)','IRC:SP114(2018)']
_INSoil = Literal['Hard','Medium','Soft']
_INZone = Literal['II','III','IV','V']

class _RSCase:
    ID :int = 0
    NAME: str = 0
    DIR: str = 0
    ANGLE: float = 0
    SCALE: float = 0
    RS_FUNCTIONS: list[str] = 0
    PM_FACTOR: float = 0
    INTERP: str = 0
    COMBINATION_CONTROL: int = 0
    DAMPING_CONTROL: int = 0
    DESC: str = 0

class RS:

    @staticmethod
    def create():
        RS.Function.create()
        RS.Case.create()

    class ModalCombination:
        def __init__(self,combType:_ModalCombType='CQC',bAddSign:bool=False,AddSignType:int=0,ModeShapeFactor:list[float]=None):
            self.TYPE = combType
            self.bADD_SIGN = bAddSign
            self.SIGN_TYPE = AddSignType
            self.bSELECT_MODE = False
            self.SELECTED_MODES = []

            if ModeShapeFactor !=None:
                self.bSELECT_MODE = True
                self.SELECTED_MODES = ModeShapeFactor

        def _json(self):
            _js = {
                "COMTYPE": self.TYPE,
                "bADDSIGN": self.bADD_SIGN,
                "iSIGNTYPE": self.SIGN_TYPE,
                "bMODE": self.bSELECT_MODE,
                }
            
            if self.bSELECT_MODE:
                _USEMODE = []
                for fac in self.SELECTED_MODES:
                    if fac:
                        _USEMODE.append({"bUSE":True,"MSFACTOR":fac})
                    else:
                        _USEMODE.append({"bUSE":False,"MSFACTOR":0})
                _js["aUSEMODE"] = _USEMODE
            return _js

    class Damping:

        class Modal:
            def __init__(self,dampRatioAllMode=0.05):
                self.DAMP_RATIO = dampRatioAllMode

            def _json(self):
                _js = {
                    "bDAMP": True,
                    "iMDTYPE": 1,
                    "DALL": self.DAMP_RATIO,
                    
                }

                return _js
            
        
        class MassStiffness:
            def __init__(self,inpType:int=1,massProp:float=None,stiffProp:float=None,freq1:float=0,damp1:float=0,freq2:float=0,damp2:float=0):
                self.DAMP_TYPE = inpType

                self.MASS_PROP = massProp
                self.STIFF_PROP = stiffProp

                self.__bMASS = False if self.MASS_PROP == None else True
                self.__bSTIFF = False if self.STIFF_PROP == None else True

                self.__MASS = 0 if self.MASS_PROP == None else massProp
                self.__STIFF = 0 if self.STIFF_PROP == None else stiffProp

                self.FREQ_1 = freq1
                self.DAMP_1 = damp1
                self.FREQ_2 = freq2
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
                    _js['iCALC'] = 1
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

    class Case:
        cases:list[_RSCase] = []
        _ids = [0]
        def __init__(self,name:str,direction:_RSDir="XY",excitation_angle:float=0,scale_factor:float=1,period_modify_factor:float = 1 ,spectrum_functions:list[str]=['RS_FUNC'],interpolation:_InterpType='LINEAR',modal_combination_control=None,damping_control=None,bDampCorrection:bool=False,desc:str='',id:int=None):
            self.NAME= name
            self.DIR = direction
            self.ANGLE = excitation_angle
            self.SCALE = scale_factor
            self.PM_FACTOR = period_modify_factor
            self.RS_FUNCTIONS = spectrum_functions
            self.INTERP = interpolation
            self.COMBINATION_CONTROL = modal_combination_control
            self.DAMPING_CONTROL = damping_control
            self.DESC = desc
            self.bDAMP_CORRECTION = bDampCorrection

            if id is None:
                self.ID = len(RS.Case.cases) + 1
            else:
                self.ID = id
            
            RS.Case.cases.append(self)
        
        @staticmethod
        def json():
            """Creates JSON from System Temperature objects defined in Python"""
            json_data = {"Assign": {}}
            for case in RS.Case.cases:
                json_data["Assign"][str(case.ID)] = {
                    "NAME": case.NAME,
                    "DIR": case.DIR,
                    "ANGLE": case.ANGLE,
                    "SCALE": case.SCALE,
                    "PMFT": case.PM_FACTOR,
                    "INTERP": case.INTERP,
                    "aFUNCNAME": case.RS_FUNCTIONS,
                    "DESC": case.DESC,
                    "bDAMP": False,
                    "bCDAMP" : case.bDAMP_CORRECTION
                }

                if case.DAMPING_CONTROL !=None: # DAMPING
                    json_data["Assign"][str(case.ID)].update(case.DAMPING_CONTROL._json())

                if case.COMBINATION_CONTROL !=None: # DAMPING
                    json_data["Assign"][str(case.ID)].update(case.COMBINATION_CONTROL._json())


            return json_data
        
        @staticmethod
        def get():
            """Get the JSON of RS Cases from MIDAS Civil NX"""
            return MidasAPI("GET", "/db/SPLC")
        
        @staticmethod
        def create():
            """Creates RS CASE in MIDAS Civil NX"""
            if RS.Case.cases:
                MidasAPI("PUT", "/db/SPLC", RS.Case.json())

        @staticmethod
        def delete():
            """Delete RS CASE in MIDAS Civil NX"""
            RS.Case.clear()
            MidasAPI("DELETE", "/db/SPLC")

        @staticmethod
        def clear():
            """Clears RS CASE"""
            RS.Case.cases = []
            RS.Case.ids = [0]

        @classmethod
        def sync(cls):
            """Sync RS Cases from MIDAS Civil NX to Python"""
            cls.clear()
            a = cls.get()
            
            if a and 'SPLC' in a:
                data = a.get('SPLC', {})
                for id, jsData in data.items():
                    RS.Case(jsData['NAME'],jsData['DIR'],jsData['ANGLE'],jsData['SCALE'],jsData['PMFT'],
                                          jsData['aFUNCNAME'],jsData['INTERP'],None,None,jsData['DESC']
                                          ,id=int(id))


    class Function:
        functions = []
        _ids = [0]

        @classmethod
        def json(cls):
            js_data = {"Assign" : {}}
            for func in cls.functions:
                js_data["Assign"][func.ID] = func._json()
            return js_data
        
        @classmethod
        def create(cls):
            if RS.Function.functions:
                MidasAPI('PUT','/db/SPFC',cls.json())


        class USER:
            def __init__(self,name,RSdata = [(0,0),(0.1,0.1)],spectral_type:_SpecType='Normalized Accel',scaling=1,max_value=None,gravity=None,damping_rat = 0.05,desc="",id=None):
                
                if gravity==None:
                    gravity = Model.gravity()
                
                

                if isinstance(spectral_type,str):
                    _mapping = {
                        "Normalized Accel" : 1,
                        "Acceleration" : 2,
                        "Velocity" : 3,
                        "Displacement" : 4
                    }
                    spectral_type = _mapping.get(spectral_type,1)

                if id is None:
                    self.ID = max(RS.Function._ids)+1
                else:
                    self.ID = id
                
                self.NAME = name
                self.TYPE = spectral_type
                self.CODE = "USER"
                self.SCALE_FACTOR = scaling
                self.MAX_VALUE = max_value
                self.GRAVITY = gravity
                self.DAMP = damping_rat
                self.DATA = RSdata
                self.DESC = desc

                RS.Function.functions.append(self)
                RS.Function._ids.append(self.ID)

            def _json(self):
                js_data = {
                        "NAME": self.NAME,
                        "iTYPE": self.TYPE,
                        "DRATIO": self.DAMP,
                        "DESC": self.DESC,
                        }
                if self.MAX_VALUE != None:
                    js_data["iMETHOD"] = 1
                    js_data["SCALE"] = self.MAX_VALUE
                else:
                    js_data["iMETHOD"] = 0
                    js_data["SCALE"] = self.SCALE_FACTOR
                
                if self.TYPE == 1:
                    js_data["GRAV"] = self.GRAVITY
                
                _aFunc = []
                for i in self.DATA:
                    _aFunc.append({"PERIOD" : i[0] , "VALUE" : i[1]})
                js_data["aFUNC"] = _aFunc

                return js_data

        class India:
            def __init__(self,name,code:_INCode='IS1893(2002)',soilType:_INSoil='Hard',zone:_INZone='IV',imp_factor=1.0,RRF=1.5,max_period=6,spectral_type='Normalized Accel',scaling=1,max_value=None,gravity=None,damping_rat = 0.05,desc="",id=None):
                
                if gravity==None:
                    gravity = Model.gravity()

                if isinstance(spectral_type,str):
                    _mapping = {
                        "Normalized Accel" : 1,
                        "Acceleration" : 2,
                        "Velocity" : 3,
                        "Displacement" : 4
                    }
                    spectral_type = _mapping.get(spectral_type,1)

                if id is None:
                    self.ID = max(RS.Function._ids)+1
                else:
                    self.ID = id
                if desc == "":
                    desc = f"{code}: Zone = {zone}  |  Soil = {soilType} | Damping = {round(damping_rat*100,2)} % | I = {imp_factor} | R = {RRF} "
                
                self.NAME = name

                _CodeMapping = {
                    'IS1893(2016)' : 'IS1893(2016)',
                    'IS1893(2002)' : 'IS2002',
                    'IRC:SP114(2018)' : 'IRC:SP:114-2018'
                }
                code = _CodeMapping.get(code,'IS2002')
                self.CODE = code



                _SoilMapping = {
                    'Hard':0,
                    'Medium':1,
                    'Soft':2
                }
                soilType = _SoilMapping.get(soilType,'IS2002')
                self.SOIL_TYPE = soilType


                _ZoneMapping = {
                    'II':0,'III':1,'IV':2,'V':3
                }
                zone = _ZoneMapping.get(zone,'IS2002')
                self.SEIS_ZONE = zone

                self.IMP_FACTOR = imp_factor
                self.RRF = RRF
                self.MAX_PERIOD = max_period


                
                self.TYPE = spectral_type
                self.SCALE_FACTOR = scaling
                self.MAX_VALUE = max_value
                self.GRAVITY = gravity
                self.DAMP = damping_rat

                

                self.DESC = desc


                RS.Function.functions.append(self)
                RS.Function._ids.append(self.ID)

            def _json(self):
                js_data = {
                        "NAME": self.NAME,
                        "iTYPE": self.TYPE,
                        "DRATIO": self.DAMP,
                        "DESC": self.DESC,
                        }
                if self.MAX_VALUE != None:
                    js_data["iMETHOD"] = 1
                    js_data["SCALE"] = self.MAX_VALUE
                else:
                    js_data["iMETHOD"] = 0
                    js_data["SCALE"] = self.SCALE_FACTOR
                
                if self.TYPE == 1:
                    js_data["GRAV"] = self.GRAVITY
                
                js_data["STR"] = {"SPEC_CODE": self.CODE}
                js_data["OPT"]= {
                            "SOILCLASS": self.SOIL_TYPE,
                            "iSEISZONE": self.SEIS_ZONE
                        }
                js_data["VAL"] =  {
                            "DP": self.DAMP*100,
                            "PERIOD": self.MAX_PERIOD,
                            "IE": self.IMP_FACTOR,
                            "R_": self.RRF,
                            "DPFAC": 1
                        }
                js_data["CALC_OPT"] = True

                return js_data

                
            

            
