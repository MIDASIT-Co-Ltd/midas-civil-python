from ._mapi import *
from ._model import *

class Display:

    Hidden = False
    '''Toggle Hidden mode ie. 3D section display or line'''

    class __ActiveMeta__(type):
        @property
        def mode(cls):
            ''' Mode - > "All" , "Active" , "Identity" '''
            return cls.__mode__

        @mode.setter
        def mode(cls, value):
            cls.__mode__ = value
            cls.__default__ = False
    
    class Active(metaclass = __ActiveMeta__ ):
        '''Sets Elements to be Active for View.Capture() or View.CaptureResults()

        **Mode** - "All" , "Active" , "Identity"   
        **Node_List** - Node to be active when Mode is "Active"   
        **Elem_List** - Element to be active when Mode is "Active"   
        **Identity_Type** - "Group" , "Boundary Group" , "Load Group" , "Named Plane"   
        **Identity_List** - String list of all the idenity items   
        '''
        __mode__ = "All"
        __default__ = True
        node_list = []
        elem_list = []
        ident_type = "Group"
        ident_list = []

        

        @classmethod
        def _json(cls):
            if cls.__default__: json_body = {}
            else:
                json_body = {
                    "ACTIVE_MODE": cls.__mode__
                }

                if cls.mode == "Active" :
                    json_body["N_LIST"] = cls.node_list
                    json_body["E_LIST"] = cls.elem_list
                elif cls.mode == "Identity" :
                    json_body["IDENTITY_TYPE"] = cls.ident_type
                    json_body["IDENTITY_LIST"] = cls.ident_list

            return json_body
    

    class __AngleMeta__(type):
        @property
        def Horizontal(cls):
            return cls.__horizontal__

        @Horizontal.setter
        def Horizontal(cls, value):
            cls.__horizontal__ = value
            cls.__newH__ = True

        @property
        def Vertical(cls):
            return cls.__vertical__

        @Vertical.setter
        def Vertical(cls, value):
            cls.__vertical__ = value
            cls.__newV__ = True

    class Angle(metaclass = __AngleMeta__) :
        __horizontal__ = 30
        __vertical__ = 15
        __newH__ = False
        __newV__ = False

        @classmethod
        def _json(cls):

            json_body = {}
            if cls.__newH__ : json_body["HORIZONTAL"] = cls.__horizontal__
            if cls.__newV__ : json_body["VERTICAL"] = cls.__vertical__

            return json_body



class ResultGraphic:

    class Contour:
        use = True
        num_color = 12
        color = "rgb"

        @classmethod
        def _json(cls):
            json_body = {
                "OPT_CHECK": cls.use,
                "NUM_OF_COLOR": cls.num_color,
                "COLOR_TYPE": cls.color
            }
            return json_body
        
    class Legend:
        use = True
        position = "right"
        bExponent = False
        num_decimal = 2

        @classmethod
        def _json(cls):
            json_body = {
                "OPT_CHECK":cls.use,
                "POSITION": cls.position,
                "VALUE_EXP":cls.bExponent,
                "DECIMAL_PT": cls.num_decimal
            }
            return json_body
        
    class Values:
        use = False
        bExpo = False
        num_decimal = 2
        orient_angle = 0

        @classmethod
        def _json(cls):
            json_body = {
                "OPT_CHECK":cls.use,
                "VALUE_EXP": cls.bExpo,
                "DECIMAL_PT":cls.num_decimal,
                "SET_ORIENT": cls.orient_angle,
            }
            return json_body
        
    class Deform:
        use = False
        scale = 1.0
        bRealDeform = False
        bRealDisp = False
        bRelativeDisp = False

        @classmethod
        def _json(cls):
            json_body = {
                "OPT_CHECK":cls.use,
                "SCALE_FACTOR": cls.scale,
                "REL_DISP":cls.bRelativeDisp,
                "REAL_DISP": cls.bRealDisp,
                "REAL_DEFORM": cls.bRealDeform
            }
            return json_body
    
    @staticmethod
    def BeamDiagram(lcase_type,lcase_name,lcase_minmax="max",part='total',component='My') -> dict:

        json_body = {
                "CURRENT_MODE":"BeamDiagrams",
                "LOAD_CASE_COMB":{
                    "TYPE":lcase_type,
                    "NAME":lcase_name,
                    "MINMAX" : lcase_minmax
                },
                "COMPONENTS":{
                    "PART":part,
                    "COMP":component
                },
                "DISPLAY_OPTIONS":{
                    "FIDELITY":"5 Points",
                    "FILL":"Line",
                    "SCALE":1.0
                },
                "TYPE_OF_DISPLAY":{
                    "CONTOUR": ResultGraphic.Contour._json(),
                    "DEFORM":ResultGraphic.Deform._json(),
                    "LEGEND":ResultGraphic.Legend._json(),
                    "VALUES":{
                        "OPT_CHECK":False
                    }
                }
            }
        return json_body
    
    @staticmethod
    def DisplacementContour(lcase_type,lcase_name,lcase_minmax="max",component='DXYZ') -> dict:

        json_body = {
                "CURRENT_MODE":"DisplacementContour",
                "LOAD_CASE_COMB":{
                    "TYPE":lcase_type,
                    "NAME":lcase_name,
                    "MINMAX" : lcase_minmax
                },
                "COMPONENTS":{
                    "COMP":component,
                    "OPT_LOCAL_CHECK" : False
                },
                "TYPE_OF_DISPLAY":{
                    "CONTOUR": ResultGraphic.Contour._json(),
                    "DEFORM":ResultGraphic.Deform._json(),
                    "LEGEND":ResultGraphic.Legend._json(),
                    "VALUES":{
                        "OPT_CHECK":False
                    }
                }
            }
        
        return json_body

class View:
    @staticmethod
    def Capture(location="D:\\API_temp\\img3.jpg",img_w = 1280 , img_h = 720,view='pre',stage:str=''):
        ''' Location - image location
            Image height and width
            View - 'pre' or 'post'
            stage - CS name
        '''
        json_body = {
                "Argument": {
                    "SET_MODE":"pre",
                    "SET_HIDDEN":Display.Hidden,
                    "EXPORT_PATH": location,
                    "HEIGHT": img_h,
                    "WIDTH": img_w,
                    "ACTIVE" : Display.Active._json(),
                    "ANGLE":Display.Angle._json()
                }
            }
        
        if view=='post':
            json_body['Argument']['SET_MODE'] = 'post'
        elif view=='pre':
            json_body['Argument']['SET_MODE'] = 'pre'

        if stage != '':
            json_body['Argument']['STAGE_NAME'] = stage

        MidasAPI('POST','/view/CAPTURE',json_body)

    @staticmethod
    def CaptureResults(ResultGraphic:dict,location:str="D:\\API_temp\\img3.jpg",img_w:int = 1280 , img_h:int = 720,CS_StageName:str=''):
        ''' 
            Result Graphic - ResultGraphic JSON (ResultGraphic.BeamDiagram())
            Location - image location
            Image height and width
            Construction stage Name (default = "") if desired
        '''
        json_body = {
                "Argument":{
                    "SET_MODE":"post",
                    "SET_HIDDEN":Display.Hidden,
                    "EXPORT_PATH":location,
                    "HEIGHT":img_h,
                    "WIDTH":img_w,
                    "ACTIVE":Display.Active._json(),
                    "ANGLE":Display.Angle._json(),
                    "RESULT_GRAPHIC": ResultGraphic
                }
                }
        if CS_StageName != '':
            json_body['Argument']['STAGE_NAME'] = CS_StageName
        MidasAPI('POST','/view/CAPTURE',json_body)
