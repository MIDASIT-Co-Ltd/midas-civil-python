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

        def __init__(self,mode='All',node_list=[],elem_list=[],ident_type='Group',ident_list=[]):
            '''Sets Elements to be Active for View.Capture() or View.CaptureResults()

            **Mode** - "All" , "Active" , "Identity"   
            **Node_List** - Node to be active when Mode is "Active"   
            **Elem_List** - Element to be active when Mode is "Active"   
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
        **position** - Position of Legend - "left" | "right"  
        **bExponent** - True -> Shows exponential values in legend  | False -> Shows fixed values in legend  
        **num_decimal** -  Number of decimal values shown in legend  
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
        **orient_angle** - Orientation angle of Values (0,15,30,45,60,75,90)
        **bExpo** - True -> Shows exponential values in viewport  | False -> Shows fixed values in viewport  
        **num_decimal** -  Number of decimal values shown in viewport  
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
        **scale** - Deformation scale factor  
        **bRealDeform** - False -> Shows Nodal Deform  | True -> Shows Real Deform  
        **bRealDisp** -  Shows real displacement (Auto-Scale Off)  
        **bRelativeDisp** -  The structure's deformation is shown graphically in relation to a minimum nodal displacement set at 0  
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
    def BeamDiagram(lcase_type:str, lcase_name:str, lcase_minmax:str="Max",
                    part:str="total", component:str="My",
                    fidelity:str="Exact", fill:str="Solid", scale:float=1.0) -> dict:
        '''
        Generates JSON for Beam Diagrams Result Graphic.
        
        Args:
            lcase_type (str): Load Case Type ("ST", "CS", "RS", "TH", "MV", "SM", "CB").
            lcase_name (str): Load Case/Combination Name (e.g., "DL").
            lcase_minmax (str): Load Type ("Max", "Min", "All"). Defaults to "Max".
            part (str): Component Part ("total", ...). Defaults to "total".
            component (str): Component Name ("Fx", "Fy", "Fz", "Mx", "My", "Mz"). Defaults to "My".
            fidelity (str): Fidelity of the diagram ("Exact", "5 Points", ...). Defaults to "Exact".
            fill (str): Fill of Diagram ("No", "Line", "Solid"). Defaults to "Solid".
            scale (float): Scale of Diagram. Defaults to 1.0.

        '''
        json_body = {
                "CURRENT_MODE":"BeamDiagrams",
                "LOAD_CASE_COMB":{
                    "TYPE":lcase_type,
                    "NAME":lcase_name,
                    "MINMAX" : lcase_minmax,
                    "STEP_INDEX": 1,
                    "OPT_MAXMIN_DIAGRAM": False
                },
                "COMPONENTS":{
                    "PART":part,
                    "COMP":component,
                    "OPT_SHOW_TRUSS_FORCES": True,
                    "OPT_ONLY_TRUSS_FORCES": False
                },
                "DISPLAY_OPTIONS":{
                    "FIDELITY": fidelity,
                    "FILL": fill,
                    "SCALE": scale
                },
                "TYPE_OF_DISPLAY":{
                    "CONTOUR": ResultGraphic.Contour._json(),
                    "DEFORM":ResultGraphic.Deform._json(),
                    "LEGEND":ResultGraphic.Legend._json(),
                    "VALUES": ResultGraphic.Values._json(),
                    "UNDEFORMED": { "OPT_CHECK": False },
                    "MIRRORED": { "OPT_CHECK": False },
                    "OPT_CUR_STEP_FORCE": False
                }
            }
        return json_body
    
    @staticmethod
    def DisplacementContour(lcase_type:str, lcase_name:str, lcase_minmax:str="Max", component:str="DXYZ", 
                            th_option:str="Displacement", opt_local_check:bool=False) -> dict:
        '''
        Generates JSON for Displacement Contour Result Graphic.
        
        Args:
            lcase_type (str): Load Case Type ("ST", "CS", "RS", "TH", "MV", "SM", "CB").
            lcase_name (str): Load Case/Combination Name (e.g., "DL").
            lcase_minmax (str): Load Type ("Max", "Min", "All"). Defaults to "Max".
            component (str): Component Name ("DX", "DY", "DZ", "DXY", "DYZ", "DXZ", "DXYZ", "RX", "RY", "RZ", "RW"). Defaults to "DXYZ".
            th_option (str): Time History Function Type ("Displacement", "Velocity", "Acceleration"). Defaults to "Displacement".
            opt_local_check (bool): Use Node Local Axis (True) or Global Coord System (False). Defaults to False.

        '''
        json_body = {
                "CURRENT_MODE":"DisplacementContour",
                "LOAD_CASE_COMB":{
                    "TYPE":lcase_type,
                    "NAME":lcase_name,
                    "MINMAX" : lcase_minmax,
                    "STEP_INDEX": 1,
                    "TH_OPTION": th_option
                },
                "COMPONENTS":{
                    "COMP":component,
                    "OPT_LOCAL_CHECK" : opt_local_check
                },
                "TYPE_OF_DISPLAY":{
                    "CONTOUR": ResultGraphic.Contour._json(),
                    "DEFORM":ResultGraphic.Deform._json(),
                    "LEGEND":ResultGraphic.Legend._json(),
                    "VALUES": ResultGraphic.Values._json(),
                    "UNDEFORMED": { "OPT_CHECK": False },
                    "MIRRORED": { "OPT_CHECK": False },
                    "CUTTING_DIAGRAM": { "OPT_CHECK": False },
                    "OPT_CUR_STEP_DISPLACEMENT": True,
                    "OPT_STAGE_STEP_REAL_DISPLACEMENT": True,
                    "OPT_INCLUDING_CAMBER_DISPLACEMENT": True
                }
            }
        
        return json_body

    @staticmethod
    def ReactionForcesMoments(lcase_type:str, lcase_name:str, lcase_minmax:str="Max", component:str="FXYZ", 
                                opt_local_check:bool=False, arrow_scale_factor:float=1.0) -> dict:
        '''
        Generates JSON for Reaction Forces/Moments Result Graphic.
        
        Args:
            lcase_type (str): Load Case Type ("ST", "CS", "RS", "TH", "MV", "SM", "CB").
            lcase_name (str): Load Case/Combination Name (e.g., "DL").
            lcase_minmax (str): Load Type ("Max", "Min", "All"). Defaults to "Max".
            component (str): Component Name ("FX", "FY", "FZ", "FXYZ", "MX", "MY", "MZ", "MXYZ", "Mb"). Defaults to "FXYZ".
            opt_local_check (bool): Use Node Local Axis (True) or Global Coord System (False). Defaults to False.
            arrow_scale_factor (float): Scale factor for reaction arrows. Defaults to 1.0.

        '''
        json_body = {
                "CURRENT_MODE":"ReactionForces/Moments",
                "LOAD_CASE_COMB":{
                    "TYPE":lcase_type,
                    "NAME":lcase_name,
                    "MINMAX" : lcase_minmax,
                    "STEP_INDEX": 1
                },
                "COMPONENTS":{
                    "COMP":component,
                    "OPT_LOCAL_CHECK" : opt_local_check
                },
                "TYPE_OF_DISPLAY":{
                    "LEGEND":ResultGraphic.Legend._json(),
                    "VALUES": ResultGraphic.Values._json(),
                    "ARROW_SCALE_FACTOR": arrow_scale_factor
                }
            }
        
        return json_body

    @staticmethod
    def DeformedShape(lcase_type:str, lcase_name:str, lcase_minmax:str="Max", component:str="DZ", 
                    th_option:str="Displacement", opt_local_check:bool=False) -> dict:
        '''
        Generates JSON for Deformed Shape Result Graphic.
        
        Args:
            lcase_type (str): Load Case Type ("ST", "CS", "RS", "TH", "MV", "SM", "CB").
            lcase_name (str): Load Case/Combination Name (e.g., "DL").
            lcase_minmax (str): Load Type ("Max", "Min", "All"). Defaults to "Max".
            component (str): Component Name ("DX", "DY", "DZ", "DXY", "DYZ", "DXZ", "DXYZ"). Defaults to "DZ".
            th_option (str): Time History Function Type ("Displacement", "Velocity", "Acceleration"). Defaults to "Displacement".
            opt_local_check (bool): Use Node Local Axis (True) or Global Coord System (False). Defaults to False.

        '''
        json_body = {
                "CURRENT_MODE":"DeformedShape",
                "LOAD_CASE_COMB":{
                    "TYPE":lcase_type,
                    "NAME":lcase_name,
                    "MINMAX" : lcase_minmax,
                    "STEP_INDEX": 1,
                    "TH_OPTION": th_option
                },
                "COMPONENTS":{
                    "COMP":component,
                    "OPT_LOCAL_CHECK" : opt_local_check
                },
                "TYPE_OF_DISPLAY":{
                    "DEFORM":ResultGraphic.Deform._json(),
                    "VALUES": ResultGraphic.Values._json(),
                    "LEGEND":ResultGraphic.Legend._json(),
                    "MIRRORED": { "OPT_CHECK": False },
                    "UNDEFORMED": { "OPT_CHECK": True },
                    "OPT_CUR_STEP_DISPLACEMENT": True,
                    "OPT_STAGE_STEP_REAL_DISPLACEMENT": True,
                    "OPT_INCLUDING_CAMBER_DISPLACEMENT": True
                }
            }
        
        return json_body

    @staticmethod
    def BeamForcesMoments(lcase_type:str, lcase_name:str, lcase_minmax:str="Max",
                          part:str="total", component:str="Fx") -> dict:
        '''
        Generates JSON for Beam Forces/Moments Result Graphic.
        
        Args:
            lcase_type (str): Load Case Type ("ST", "CS", "RS", "TH", "MV", "SM", "CB").
            lcase_name (str): Load Case/Combination Name (e.g., "dl").
            lcase_minmax (str): Load Type ("Max", "Min", "All"). Defaults to "Max".
            part (str): Component Part ("total", ...). Defaults to "total".
            component (str): Component Name ("Fx", "Fy", "Fz", "Mx", "My", "Mz"). Defaults to "Fx".

        '''
        json_body = {
            "CURRENT_MODE": "BeamForces/Moments",
            "LOAD_CASE_COMB": {
                "TYPE": lcase_type,
                "MINMAX": lcase_minmax,
                "NAME": lcase_name,
                "STEP_INDEX": 1
            },
            "COMPONENTS": {
                "PART": part,
                "COMP": component,
                "OPT_SHOW_TRUSS_FORCES": True
            },
            "TYPE_OF_DISPLAY": {
                "CONTOUR": ResultGraphic.Contour._json(),
                "DEFORM": ResultGraphic.Deform._json(),
                "VALUES": ResultGraphic.Values._json(),
                "LEGEND": ResultGraphic.Legend._json(),
                "MIRRORED": { "OPT_CHECK": False },
                "UNDEFORMED": { "OPT_CHECK": True },
                "OPT_CUR_STEP_FORCE": False,
                "YIELD_POINT": { "OPT_CHECK": False }
            },
            "OUTPUT_SECT_LOCATION": {
                "OPT_I": True,
                "OPT_CENTER_MID": True,
                "OPE_J": True,
                "OPT_BY_MEMBER": True
            }
        }
        return json_body

    @staticmethod
    def MovingTracer_Reactions(lcase_name:str, key_node_elem:int, lcase_minmax:str="Max", 
                         component:str="Fz", opt_local_check:bool=False) -> dict:
        '''
        Generates JSON for Moving Tracer Reactions Result Graphic.
        
        Args:
            lcase_name (str): Load Case Name (e.g., "DB").
            key_node_elem (int): Key Node or Element ID.
            lcase_minmax (str): Load Type ("Max", "Min", "All"). Defaults to "Max".
            component (str): Component Name ("FX", "FY", "FZ", "MX", "MY", "MZ", "Mb"). Defaults to "Fz".
            opt_local_check (bool): Use Node Local Axis (True). Defaults to False.

        '''
        json_body = {
            "CURRENT_MODE": "MVLTRC_Reactions",
            "LOAD_CASE_COMB": {
                "TYPE": "MV",
                "MINMAX": lcase_minmax,
                "NAME": lcase_name,
                "KEY_NODE_ELEM": key_node_elem
            },
            "COMPONENTS": {
                "COMP": component,
                "OPT_LOCAL_CHECK": opt_local_check
            },
            "TYPE_OF_DISPLAY": {
                "CONTOUR": ResultGraphic.Contour._json(),
                "LEGEND": ResultGraphic.Legend._json(),
                "APPLIED_LOADS": {
                    "OPT_CHECK": True,
                    "SCALE_FACTOR": 1.0,
                    "OPT_LOAD_VALUES": False,
                    "VALUE_TYPE": "Exponential",
                    "VALUE_DECIMAL_PT": 1
                },
                "OPT_INCLUDE_IMPACT_FACTOR": True
            }
        }
        return json_body

    @staticmethod
    def MovingTracer_Displacements(lcase_name:str, key_node_elem:int, lcase_minmax:str="Max",component:str="Dz") -> dict:
        '''
        Generates JSON for Moving Tracer Displacements Result Graphic.
        
        Args:
            lcase_name (str): Load Case Name (e.g., "DB").
            key_node_elem (int): Key Node or Element ID.
            lcase_minmax (str): Load Type ("Max", "Min", "All"). Defaults to "Max".
            component (str): Component Name ("DX", "DY", "DZ", "RX", "RY", "RZ", "RW"). Defaults to "Dz".
        '''
        json_body = {
            "CURRENT_MODE": "MVLTRC_Displacements",
            "LOAD_CASE_COMB": {
                "TYPE": "MV",
                "MINMAX": lcase_minmax,
                "NAME": lcase_name,
                "KEY_NODE_ELEM": key_node_elem
            },
            "COMPONENTS": {
                "COMP": component
            },
            "TYPE_OF_DISPLAY": {
                "CONTOUR": ResultGraphic.Contour._json(),
                "LEGEND": ResultGraphic.Legend._json(),
                "APPLIED_LOADS": {
                    "OPT_CHECK": True,
                    "SCALE_FACTOR": 1.0,
                    "OPT_LOAD_VALUES": False,
                    "VALUE_TYPE": "Exponential",
                    "VALUE_DECIMAL_PT": 1
                },
                "OPT_INCLUDE_IMPACT_FACTOR": True
            }
        }
        return json_body

    @staticmethod
    def MovingTracer_BeamForcesMoments(lcase_name:str, key_node_elem:int, lcase_minmax:str="Max", 
                                 part:str="1/4", component:str="My") -> dict:
        '''
        Generates JSON for Moving Tracer Beam Forces/Moments Result Graphic.
        
        Args:
            lcase_name (str): Load Case Name (e.g., "DB").
            key_node_elem (int): Key Node or Element ID.
            lcase_minmax (str): Load Type ("Max", "Min", "All"). Defaults to "Max".
            part (str): Part location ("I", "1/4", "1/2", "3/4", "J"). Defaults to "1/4".
            component (str): Component Name ("FX", "FY", "FZ", "MX", "MY", "MZ", "Mb", "Mt", "Mw"). Defaults to "My".

        '''
        json_body = {
            "CURRENT_MODE": "MVLTRC_BeamForces/Moments",
            "LOAD_CASE_COMB": {
                "TYPE": "MV",
                "MINMAX": lcase_minmax,
                "NAME": lcase_name,
                "KEY_NODE_ELEM": key_node_elem
            },
            "COMPONENTS": {
                "PART": part,
                "COMP": component
            },
            "TYPE_OF_DISPLAY": {
                "CONTOUR": ResultGraphic.Contour._json(),
                "LEGEND": ResultGraphic.Legend._json(),
                "APPLIED_LOADS": {
                    "OPT_CHECK": True,
                    "SCALE_FACTOR": 1.0,
                    "OPT_LOAD_VALUES": False,
                    "VALUE_TYPE": "Exponential",
                    "VALUE_DECIMAL_PT": 1
                },
                "OPT_INCLUDE_IMPACT_FACTOR": True
            }
        }
        return json_body

    @staticmethod
    def VibrationModeShapes(mode_name:str, component:str="Md-XZ") -> dict:
        '''
        Generates JSON for Vibration Mode Shapes Result Graphic.
        
        Args:
            mode_name (str): Mode Name (e.g., "Mode6").
            component (str): Component Name ("Md-X", "Md-Y", "Md-Z", "Md-XY", "Md-YZ", "Md-XZ", "Md-XYZ"). Defaults to "Md-XZ".
        '''
        json_body = {
            "CURRENT_MODE": "VibrationModeShapes",
            "LOAD_CASE_COMB": {
                "NAME": mode_name
            },
            "COMPONENTS": {
                "COMP": component
            },
            "TYPE_OF_DISPLAY": {
                "VALUES": ResultGraphic.Values._json(),
                "MODE_SHAPE": { "OPT_CHECK": True },
                "UNDEFORMED": { "OPT_CHECK": True },
                "LEGEND": ResultGraphic.Legend._json(),
                "CONTOUR": ResultGraphic.Contour._json()
            }
        }
        return json_body

    @staticmethod
    def BucklingModeShapes(mode_name:str, component:str="Md-XYZ") -> dict:
        '''
        Generates JSON for Buckling Mode Shapes Result Graphic.
        
        Args:
            mode_name (str): Mode Name (e.g., "Mode 2").
            component (str): Component Name ("Md-X", "Md-Y", "Md-Z", "Md-XY", "Md-YZ", "Md-XZ", "Md-XYZ"). Defaults to "Md-XYZ".
        '''
        json_body = {
            "CURRENT_MODE": "Buckling Mode Shapes",
            "LOAD_CASE_COMB": {
                "NAME": mode_name
            },
            "COMPONENTS": {
                "COMP": component
            },
            "TYPE_OF_DISPLAY": {
                "MODE_SHAPE": { "OPT_CHECK": True },
                "VALUES": ResultGraphic.Values._json(),
                "LEGEND": ResultGraphic.Legend._json(),
                "CONTOUR": ResultGraphic.Contour._json() 
            }
        }
        return json_body

    @staticmethod
    def PlateForcesMoments(lcase_type:str, lcase_name:str, lcase_minmax:str="Max",
                           component:str="MMax", local_ucs_type:str="Local", avg_nodal_type:str="Element",
                           wood_armer_pos:str="Top", wood_armer_dir:str="Dir.1",
                           vector_opt_pos:bool=True, vector_opt_neg:bool=False) -> dict:
        '''
        Generates JSON for Plate Forces/Moments Result Graphic.

        Args:
            lcase_type (str): Load Case Type ("ST", "CS", ...).
            lcase_name (str): Load Case/Combination Name.
            lcase_minmax (str): Load Type ("Max", "Min", "All"). Defaults to "Max".
            component (str): Component ("Fxx", "Mxx", "MMax", "WoodArmerMoment", "Mvector"). Defaults to "MMax".
            local_ucs_type (str): Coordinate System ("Local", "UCS"). Defaults to "Local".
            avg_nodal_type (str): Avg. Calculation ("Element", "Avg.Nodal"). Defaults to "Element".
            wood_armer_pos (str): For "WoodArmerMoment" ("Top", "Bottom"). Defaults to "Top".
            wood_armer_dir (str): For "WoodArmerMoment" ("Dir.1", "Dir.2"). Defaults to "Dir.1".
            vector_opt_pos (bool): For "Mvector"/"Fvector" (Display Positive). Defaults to True.
            vector_opt_neg (bool): For "Mvector"/"Fvector" (Display Negative). Defaults to False.

        '''
        
        components_json = {"COMP": component}
        if component == "WoodArmerMoment":
            components_json["WOOD_ARMER_MOMENT_OPTION"] = {
                "POSITION": wood_armer_pos,
                "DIRECTION": wood_armer_dir
            }
        elif component in ["Mvector", "Fvector"]:
            components_json["VECTOR_OPTION"] = {
                "OPT_POSITIVE": vector_opt_pos,
                "OPT_NEGATIVE": vector_opt_neg,
                "SCALE_FACTOR_LENGTH": 1.0,
                "SCALE_FACTOR_THICKNESS": 1
            }

        json_body = {
            "CURRENT_MODE": "PlateForces/Moments",
            "LOAD_CASE_COMB": {
                "TYPE": lcase_type,
                "MINMAX": lcase_minmax,
                "NAME": lcase_name,
                "STEP_INDEX": 1
            },
            "OPTIONS": {
                "LOCAL_UCS": {
                    "TYPE": local_ucs_type
                    # Can be expanded to include UCS_NAME, OPT_PRINT_UCS_AXIS
                },
                "AVERAGE_NODAL": {
                    "TYPE": avg_nodal_type
                    # Can be expanded to include OPT_ACTIVE_ONLY
                }
            },
            "COMPONENTS": components_json,
            "TYPE_OF_DISPLAY": {
                "CONTOUR": ResultGraphic.Contour._json(),
                "DEFORM": ResultGraphic.Deform._json(),
                "UNDEFORMED": { "OPT_CHECK": True },
                "VALUES": ResultGraphic.Values._json(),
                "LEGEND": ResultGraphic.Legend._json()
            }
        }
        return json_body

    @staticmethod
    def TrussStresses(lcase_type:str, lcase_name:str, component:str="All",
                      output_loc:str="All") -> dict:
        '''
        Generates JSON for Truss Stresses Result Graphic.
        
        Args:
            lcase_type (str): Load Case Type ("ST", "CS", ...).
            lcase_name (str): Load Case/Combination Name.
            component (str): Component ("All", "Tens.", "Comp."). Defaults to "All".
            output_loc (str): Output Section Location ("I", "J", "Max", "All"). Defaults to "All".
        '''
        json_body = {
            "CURRENT_MODE": "TrussStresses",
            "LOAD_CASE_COMB": {
                "TYPE": lcase_type,
                "NAME": lcase_name,
                "STEP_INDEX": 1
            },
            "COMPONENTS": {
                "COMP": component
            },
            "TYPE_OF_DISPLAY": {
                "CONTOUR": ResultGraphic.Contour._json(),
                "VALUES": ResultGraphic.Values._json(),
                "DEFORM": ResultGraphic.Deform._json(),
                "LEGEND": ResultGraphic.Legend._json()
            },
            "OUTPUT_SECT_LOCATION": {
                "OPT_I_J_MAX_ALL": output_loc
            }
        }
        return json_body

    @staticmethod
    def BeamStresses(lcase_type:str, lcase_name:str, part:str="Total", 
                     component:str="Combined", comp_sub:str="Maximum", output_loc:str="Max",
                     comp_7th_dof:str="Combined(Ssy)") -> dict:
        '''
        Generates JSON for Beam Stresses Result Graphic.
        
        Args:
            lcase_type (str): Load Case Type ("ST", "CS", ...).
            lcase_name (str): Load Case/Combination Name.
            part (str): Part Name. Defaults to "Total".
            component (str): Component ("Sax", "Ssy", "Ssz", "Sby", "Sbz", "Combined", "7thDOF"). Defaults to "Combined".
            comp_sub (str): Sub-component ("Maximum", "1(-y,+z)", ...). Defaults to "Maximum".
            output_loc (str): Output Section Location ("Max", "All"). Defaults to "Max".
            comp_7th_dof (str): 7th DOF Component ("Sax(Warping)", "Combined(Ssy)", ...). Defaults to "Combined(Ssy)".

        '''
        
        components_json = {
            "PART": part,
            "COMP": component,
            "COMP_SUB": comp_sub
        }
        if component == "7thDOF":
            components_json["COMP_7TH_DOF"] = comp_7th_dof

        json_body = {
            "CURRENT_MODE": "BeamStresses",
            "LOAD_CASE_COMB": {
                "TYPE": lcase_type,
                "NAME": lcase_name,
                "STEP_INDEX": 1
            },
            "COMPONENTS": components_json,
            "TYPE_OF_DISPLAY": {
                "CONTOUR": ResultGraphic.Contour._json(),
                "VALUES": ResultGraphic.Values._json(),
                "DEFORM": ResultGraphic.Deform._json(),
                "LEGEND": ResultGraphic.Legend._json()
            },
            "OUTPUT_SECT_LOCATION": {
                "OPT_MAX_ALL": output_loc
            }
        }
        return json_body

    @staticmethod
    def BeamStressesDiagram(lcase_type:str, lcase_name:str, part:str="Total", 
                            component:str="Combined", comp_sub:str="Maximum", output_loc:str="all",
                            comp_7th_dof:str="Combined(Ssy)", fill:str="Solid", scale:float=1.0) -> dict:
        '''
        Generates JSON for Beam Stresses Diagram Result Graphic.
        
        Args:
            lcase_type (str): Load Case Type ("ST", "CS", ...).
            lcase_name (str): Load Case/Combination Name.
            part (str): Part Name. Defaults to "Total".
            component (str): Component ("Sax", "Ssy", "Ssz", "Sby", "Sbz", "Combined", "7thDOF"). Defaults to "Combined".
            comp_sub (str): Sub-component ("Maximum", "1(-y,+z)", ...). Defaults to "Maximum".
            output_loc (str): Output Section Location ("Max", "MinMax", "all"). Defaults to "all".
            comp_7th_dof (str): 7th DOF Component ("Sax(Warping)", "Combined(Ssy)", ...). Defaults to "Combined(Ssy)".
            fill (str): Fill of Diagram ("No", "Line", "Solid"). Defaults to "Solid".
            scale (float): Scale of Diagram. Defaults to 1.0.

        '''
        
        components_json = {
            "PART": part,
            "COMP": component,
            "COMP_SUB": comp_sub
        }
        if component == "7thDOF":
            components_json["COMP_7TH_DOF"] = comp_7th_dof

        json_body = {
            "CURRENT_MODE": "BeamStressesDiagram",
            "LOAD_CASE_COMB": {
                "TYPE": lcase_type,
                "NAME": lcase_name,
                "STEP_INDEX": 1
            },
            "COMPONENTS": components_json,
            "DISPLAY_OPTIONS": {
                "SCALE": scale,
                "FILL": fill
            },
            "TYPE_OF_DISPLAY": {
                "CONTOUR": ResultGraphic.Contour._json(),
                "VALUES": ResultGraphic.Values._json(),
                "DEFORM": ResultGraphic.Deform._json(),
                "LEGEND": ResultGraphic.Legend._json()
            },
            "OUTPUT_SECT_LOCATION": {
                "OPT_MAX_MINMAX_ALL": output_loc
            }
        }
        return json_body


class Image:
    @staticmethod
    def Capture(location,img_w = 1280 , img_h = 720,view='pre',CS_StageName:str=''):
        ''' 
        Capture the image in the viewport
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
    def CaptureResults(ResultGraphic:dict,location:str,img_w:int = 1280 , img_h:int = 720,CS_StageName:str=''):
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
                    "EXPORT_PATH":location,
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