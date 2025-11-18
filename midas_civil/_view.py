from ._mapi import *
from ._model import *
import base64

class View:
    '''
    Contains option for Viewport display

    **Hidden** - View.Hidden   
    **Active** - View.Active   
    **Angle** - View.Angle   
    '''

    Hidden:bool = False
    '''Toggle Hidden mode ie. 3D section display or line'''

    class __ActiveMeta__(type):
        @property
        def mode(cls) :
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

        def __init__(self,mode:str='All',node_list:list=[],elem_list:list=[],ident_type='Group',ident_list:list=[]):
            '''Sets Elements to be Active for View.Capture() or View.CaptureResults()

            **Mode** - "All" , "Active" , "Identity"   
            **Node_List** - Nodes to be active when Mode is "Active"   
            **Elem_List** - Elements to be active when Mode is "Active"   
            **Identity_Type** - "Group" , "Boundary Group" , "Load Group" , "Named Plane"   
            **Identity_List** - String list of all the idenity items  
            '''
            View.Active.mode = mode
            View.Active.node_list = node_list
            View.Active.elem_list = elem_list
            View.Active.ident_type = ident_type
            View.Active.ident_list = ident_list
            

        

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
        '''
        **Horizontal** - Horizontal angle of the Viewport  
        **Vertical** - Vertical angle of the Viewport  
        '''
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
    '''
    Contains Result Graphics type and options for Result Graphics display   

    **Contour** - ResultGraphic.Contour   
    **Legend** - ResultGraphic.Legend   
    **Values** - ResultGraphic.Values   
    **Deform** - ResultGraphic.Deform  
    **Results images** - ResultGraphic.BeamDiagram ,  ResultGraphic.DisplacementContour , ...   
    '''

    class Contour:
        '''
        **use** - ( True or False ) Shows contour in the Result Image
        **num_Color** (default - 12) - Number of colors in Contours 6, 12, 18, 24
        **color** (default - "rgb") - Color Table - "vrgb" | "rgb" | "rbg" | "gray scaled"  
        '''
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
        '''
        **use** - ( True or False ) Shows Legend in the Result Image  
        **position**  - Position of Legend - "left" | "right"  
        **bExponent** - True -> Shows exponential values in legend  | False -> Shows fixed values in legend  
        **num_decimal**  -  Number of decimal values shown in legend  
        '''
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
        '''
        **use** - ( True or False ) Shows result Values in the Result Image  
        **orient_angle**  - Orientation angle of Values (0,15,30,45,60,75,90)
        **bExpo** - True -> Shows exponential values in viewport  | False -> Shows fixed values in viewport  
        **num_decimal**  -  Number of decimal values shown in viewport  
        '''
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
        '''
        **use** - ( True or False ) Shows Deformation in the Result Image   
        **scale**  - Deformation scale factor  
        **bRealDeform** - False -> Shows Nodal Deform  | True -> Shows Real Deform  
        **bRealDisp**  -  Shows real displacement (Auto-Scale Off)  
        **bRelativeDisp**  -  The structure's deformation is shown graphically in relation to a minimum nodal displacement set at 0  
        '''
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
    def BeamDiagram(lcase_type:str,lcase_name:str,lcase_minmax:str="max",part:str='total',component:str='My') -> dict:

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
    def DisplacementContour(lcase_type:str,lcase_name:str,lcase_minmax:str="max",component:str='DXYZ') -> dict:

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

    @staticmethod
    def Reaction(lcase_type:str,lcase_name:str,lcase_minmax:str="max",component:str='FXYZ') -> dict:

        json_body = {
                "CURRENT_MODE":"ReactionForces/Moments",
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

    @staticmethod
    def DeformedShap(lcase_type:str,lcase_name:str,lcase_minmax:str="max",component:str='FXYZ') -> dict:

        json_body = {
                "CURRENT_MODE":"DeformedShap",
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

class Image:
    @staticmethod
    def Capture(location:str,img_w:int = 1280 , img_h:int = 720,view:str='pre',CS_StageName:str='') -> None:
        ''' 
        Capture the image in the viewport and saves at shown location
            Location - image location
            Image height and width
            View - 'pre' or 'post'
            stage - CS name
        '''
        json_body = {
                "Argument": {
                    "SET_MODE":"pre",
                    "SET_HIDDEN":View.Hidden,
                    "HEIGHT": img_h,
                    "WIDTH": img_w
                }
            }
        
        if View.Angle.__newH__ == True or View.Angle.__newV__ == True:
            json_body['Argument']['ANGLE'] = View.Angle._json()

        if View.Active.__default__ ==False:
            json_body['Argument']['ACTIVE'] = View.Active._json()
        
        if view=='post':
            json_body['Argument']['SET_MODE'] = 'post'
        elif view=='pre':
            json_body['Argument']['SET_MODE'] = 'pre'

        if CS_StageName != '':
            json_body['Argument']['STAGE_NAME'] = CS_StageName

        resp = MidasAPI('POST','/view/CAPTURE',json_body)

        bs64_img = resp["base64String"]
        decode = open(location, 'wb')  # Open image file to save.
        decode.write(base64.b64decode(bs64_img))  # Decode and write data.
        decode.close()

    @staticmethod
    def CaptureResults(ResultGraphic:ResultGraphic,location:str,img_w:int = 1280 , img_h:int = 720,CS_StageName:str=''):
        ''' 
        Capture Result Graphic in CIVIL NX   
            Result Graphic - ResultGraphic JSON (ResultGraphic.BeamDiagram())
            Location - image location
            Image height and width
            Construction stage Name (default = "") if desired
        '''
        json_body = {
                "Argument":{
                    "SET_MODE":"post",
                    "SET_HIDDEN":View.Hidden,
                    "HEIGHT":img_h,
                    "WIDTH":img_w,
                    "RESULT_GRAPHIC": ResultGraphic
                }
                }
        if View.Angle.__newH__ == True or View.Angle.__newV__ == True:
            json_body['Argument']['ANGLE'] = View.Angle._json()

        if View.Active.__default__ ==False:
            json_body['Argument']['ACTIVE'] = View.Active._json()

        if CS_StageName != '':
            json_body['Argument']['STAGE_NAME'] = CS_StageName
        
        resp = MidasAPI('POST','/view/CAPTURE',json_body)

        bs64_img = resp["base64String"]
        decode = open(location, 'wb')  # Open image file to save.
        decode.write(base64.b64decode(bs64_img))  # Decode and write data.
        decode.close()
