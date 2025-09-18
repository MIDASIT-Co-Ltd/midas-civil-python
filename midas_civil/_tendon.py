
from ._mapi import *
from ._utils import *
from ._load import *
from ._group import *


def _JStoObj_Relax(js):
    rm = js['RM']
    rv = js['RV']
    us = js['US']
    ys = js['YS']
    bRelax = js['bRELAX']
    cff = js['FF']

    if rm == 9: # CEBFIP 2010 Code
        wtype = js['W_TYPE']
        if wtype:
            return Tendon.Relaxation.CEBFIP_2010(rv,js['TDMFK'],us,ys,cff,0,js['W_ANGLE'])
        else:
            return Tendon.Relaxation.CEBFIP_2010(rv,js['TDMFK'],us,ys,cff,js['WF'],0)
        
    elif rm == 8: # CEBFIP 1990 Code
        wtype = js['W_TYPE']
        if wtype:
            return Tendon.Relaxation.CEBFIP_1990(rv,us,ys,cff,0,js['W_ANGLE'])
        else:
            return Tendon.Relaxation.CEBFIP_1990(rv,us,ys,cff,js['WF'],0)
        
    elif rm == 1: # CEBFIP 2010 Code
        wtype = js['W_TYPE']
        if wtype:
            return Tendon.Relaxation.CEBFIP_1978(rv,us,ys,cff,0,js['W_ANGLE'])
        else:
            return Tendon.Relaxation.CEBFIP_1978(rv,us,ys,cff,js['WF'],0)
        
    elif rm == 5: # European
        wtype = js['W_TYPE']
        if wtype:
            return Tendon.Relaxation.European(rv,us,ys,cff,0,js['W_ANGLE'])
        else:
            return Tendon.Relaxation.European(rv,us,ys,cff,js['WF'],0)
    
    elif rm == 4:
        return Tendon.Relaxation.IRC_18(rv,us,ys,cff,js['WF'])
    
    elif rm == 7:
        return Tendon.Relaxation.IRC_112(rv,us,ys,cff,js['WF'])
    
    elif rm == 0:
        if bRelax:
            return Tendon.Relaxation.Magura(rv,us,ys,cff,js['WF'])
        else: return Tendon.Relaxation.Null(us,ys,cff,js['WF'])

    else : # If nothing is matched No relaxation is applied
        return Tendon.Relaxation.Null(us,ys,cff,js['WF'])

def _JStoObj_Prop(id, js):
    name = js['NAME']

    if js['TYPE'] == 'INTERNAL' :
        if js['LT'] == 'POST': type = 2
        else : type = 1
    else: type = 3


    matID = js['MATL']
    tdn_area = js['AREA']
    duct_dia = js['D_AREA']
    relax = _JStoObj_Relax(js)
    ext_mo = js['ALPHA']
    an_s_b = js['ASB']
    an_s_e = js['ASE']
    bond_type = js['bBONDED']
    
    Tendon.Property(name,type,matID,tdn_area,duct_dia,relax,ext_mo,an_s_b,an_s_e,bond_type,id)

def _JStoObj_Profile(id,js):
    tdn_id = id 
    name = js['NAME']
    tdnProperty = js['TDN_PROP']
    tdn_group = js['TDN_GRUP']
    elem = js['ELEM']  

    inp_type = js['INPUT'] #3D
    curve_type = js['CURVE'] #SPLINE
    ref_axis = js['SHAPE'] #ELEMENT

    # Common
    st_len_begin = js['BELENG']
    st_len_end = js['ELENG']

    b_typical_tendon = js['bTP']
    n_typical_tendon = 0
    if b_typical_tendon:
        n_typical_tendon = js['CNT']

    trans_len_opt = js['LENG_OPT']
    trans_len_begin = js['BLEN']
    trans_len_end = js['ELEN']

    debon_len_begin = js['DeBondBLEN']
    debon_len_end = js['DeBondELEN']


    #Variable initialise to remove errors
    prof_xyz = []  
    prof_xy = []  
    prof_xz = []  
    prof_ins_point_end = 'END-I'  
    prof_ins_point_elem = 0  
    x_axis_dir_element = 'I-J'  
    x_axis_rot_ang = 0  
    projection = True  
    offset_y = 0  
    offset_z = 0  
    prof_ins_point = [0, 0, 0]  
    x_axis_dir_straight = 'X'  
    x_axis_dir_vec = [0, 0]  
    grad_rot_axis = 'X'  
    grad_rot_ang = 0  
    radius_cen = [0, 0]  
    offset = 0  
    dir = 'CW'      

    
    #3D - SPLINE - ROUND is bFIX , R is not considered
    if inp_type == '3D' :
        prof_xyz = []  
        json_profile_arr = js['PROF']

        for i in range(len(json_profile_arr)):
            prof_xyz.append([json_profile_arr[i]['PT'][0],json_profile_arr[i]['PT'][1],json_profile_arr[i]['PT'][2]])

    

    #2D
    elif inp_type == '2D' :
        prof_xy = []  
        prof_xz = []  
        json_profileY_arr = js['PROFY']
        json_profileZ_arr = js['PROFZ']

        for i in range(len(json_profileY_arr)):
            prof_xy.append([json_profileY_arr[i]['PT'][0],json_profileY_arr[i]['PT'][1]])
        
        for i in range(len(json_profileZ_arr)):
            prof_xz.append([json_profileZ_arr[i]['PT'][0],json_profileZ_arr[i]['PT'][1]])


    # ELEMENT
    if ref_axis == 'ELEMENT' :

        prof_ins_point_end = js['INS_PT'] 
        prof_ins_point_elem = js['INS_ELEM']
        x_axis_dir_element = js['AXIS_IJ'] 
        x_axis_rot_ang =js['XAR_ANGLE']  
        projection = js['bPJ']
        offset_y = js['OFF_YZ'][0]
        offset_z = js['OFF_YZ'][1]

    elif ref_axis == 'STRAIGHT' :
        prof_ins_point = js['IP'] 
        x_axis_dir_straight = js['AXIS'] 
        x_axis_dir_vec = js['VEC'] 
        x_axis_rot_ang =js['XAR_ANGLE']  
        projection = js['bPJ']
        grad_rot_axis = js['GR_AXIS']  
        grad_rot_ang = js['GR_ANGLE'] 

    elif ref_axis == 'CURVE' :
        prof_ins_point = js['IP'] 
        radius_cen = js['RC']  
        offset = js['OFFSET']   
        dir = js['DIR'] 
        x_axis_rot_ang =js['XAR_ANGLE']  
        projection = js['bPJ']
        grad_rot_axis = js['GR_AXIS']  
        grad_rot_ang = js['GR_ANGLE']

    
    Tendon.Profile(name,tdnProperty,tdn_group,elem,inp_type,curve_type,st_len_begin,st_len_end,n_typical_tendon,
                   trans_len_opt,trans_len_begin,trans_len_end,debon_len_begin,debon_len_end,ref_axis,
                   prof_xyz,prof_xy,prof_xz,prof_ins_point,prof_ins_point_elem,x_axis_dir_element,x_axis_rot_ang,
                   projection,offset_y,offset_z,prof_ins_point,x_axis_dir_straight,x_axis_dir_vec,grad_rot_axis,grad_rot_ang,radius_cen,offset,dir,tdn_id)



class _POINT_ : # Local class to store points
    def __init__(self,x,y,z):
        self.X = x
        self.Y = y
        self.Z = z


#5 Class to create nodes
class Tendon:

    @staticmethod
    def create():
        if Tendon.Property.properties!=[]:
            Tendon.Property.create()
        if Tendon.Profile.profiles !=[]:
            Tendon.Profile.create()
        if Tendon.Prestress.loads !=[]:
            Tendon.Prestress.create()

    class Relaxation:

        class CEBFIP_2010:
            
            def __init__(self,rho,rel_class,ult_st,yield_st,curv_fric_fac=0,wob_fric_fac=0,unint_ang_disp=0):
                '''
                    rel_class =  1 Slow | 2 Mean | 3 Rapid
                '''
                self.CODE = 'CEB FIP-2010'
                self.RHO = rho
                self.CLASS = rel_class

                self.ULT_ST = ult_st
                self.YIELD_ST = yield_st
                self.CURV_FF = curv_fric_fac
                self.WOBBLE_FF = wob_fric_fac

                self.UNINT_AD = unint_ang_disp
            
            def json(self):
                bs_json ={
                    "RM" : 9,
                    "RV" : self.RHO,
                    "TDMFK" : self.CLASS,
                    "US" : self.ULT_ST,
                    "YS" : self.YIELD_ST,
                    "FF" : self.CURV_FF,
                    "WF" : self.WOBBLE_FF,
                }

                if self.UNINT_AD != 0:
                    bs_json.update({"W_TYPE" : 1 , "W_ANGLE" : self.UNINT_AD})

                return bs_json
            
            def __str__(self):
                return str(self.__dict__)
            
        class CEBFIP_1978:
            
            def __init__(self,rho,ult_st,yield_st,curv_fric_fac=0,wob_fric_fac=0,unint_ang_disp=0):
                '''
                    rel_class =  1 Slow | 2 Mean | 3 Rapid
                '''
                self.CODE = 'CEB FIP-1978'
                self.RHO = rho

                self.ULT_ST = ult_st
                self.YIELD_ST = yield_st
                self.CURV_FF = curv_fric_fac
                self.WOBBLE_FF = wob_fric_fac

                self.UNINT_AD = unint_ang_disp
            
            def json(self):
                bs_json ={
                    "RM" : 1,
                    "RV" : self.RHO,
                    "US" : self.ULT_ST,
                    "YS" : self.YIELD_ST,
                    "FF" : self.CURV_FF,
                    "WF" : self.WOBBLE_FF,
                }

                if self.UNINT_AD != 0:
                    bs_json.update({"W_TYPE" : 1 , "W_ANGLE" : self.UNINT_AD})

                return bs_json
            
            def __str__(self):
                return str(self.__dict__)
        
        class CEBFIP_1990:
            
            def __init__(self,rho,ult_st,yield_st,curv_fric_fac=0,wob_fric_fac=0,unint_ang_disp=0):
                '''
                    rel_class =  1 Slow | 2 Mean | 3 Rapid
                '''
                self.CODE = 'CEB FIP-1990'
                self.RHO = rho

                self.ULT_ST = ult_st
                self.YIELD_ST = yield_st
                self.CURV_FF = curv_fric_fac
                self.WOBBLE_FF = wob_fric_fac

                self.UNINT_AD = unint_ang_disp
            
            def json(self):
                bs_json ={
                    "RM" : 8,
                    "RV" : self.RHO,
                    "US" : self.ULT_ST,
                    "YS" : self.YIELD_ST,
                    "FF" : self.CURV_FF,
                    "WF" : self.WOBBLE_FF,
                }

                if self.UNINT_AD != 0:
                    bs_json.update({"W_TYPE" : 1 , "W_ANGLE" : self.UNINT_AD})

                return bs_json
            
            def __str__(self):
                return str(self.__dict__)
            
        class European:
            
            def __init__(self,rel_class,ult_st,yield_st,curv_fric_fac=0,wob_fric_fac=0,unint_ang_disp=0):
                '''
                    rel_class =  1 Ordinary | 2 Low | 3 HotRolled
                '''
                self.CODE = 'European'
                self.CLASS = rel_class

                self.ULT_ST = ult_st
                self.YIELD_ST = yield_st
                self.CURV_FF = curv_fric_fac
                self.WOBBLE_FF = wob_fric_fac

                self.UNINT_AD = unint_ang_disp
            
            def json(self):
                bs_json ={
                    "RM" : 5,
                    "RV" : self.CLASS,
                    "US" : self.ULT_ST,
                    "YS" : self.YIELD_ST,
                    "FF" : self.CURV_FF,
                    "WF" : self.WOBBLE_FF,
                }

                if self.UNINT_AD != 0:
                    bs_json.update({"W_TYPE" : 1 , "W_ANGLE" : self.UNINT_AD})

                return bs_json
            
            def __str__(self):
                return str(self.__dict__)

        class IRC_18:
            
            def __init__(self,factor,ult_st,yield_st,curv_fric_fac=0,wob_fric_fac=0):

                self.CODE = 'IRC:18-2000'

                self.FACTOR = factor

                self.ULT_ST = ult_st
                self.YIELD_ST = yield_st
                self.CURV_FF = curv_fric_fac
                self.WOBBLE_FF = wob_fric_fac
            
            def json(self):
                bs_json ={
                    "RM" : 4,
                    "RV" : self.FACTOR,
                    "US" : self.ULT_ST,
                    "YS" : self.YIELD_ST,
                    "FF" : self.CURV_FF,
                    "WF" : self.WOBBLE_FF
                }
                return bs_json
            
            def __str__(self):
                return str(self.__dict__)
            
        class IRC_112:
            
            def __init__(self,factor,ult_st,yield_st,curv_fric_fac=0,wob_fric_fac=0):

                self.CODE = 'IRC:112-2011'


                self.FACTOR = factor

                self.ULT_ST = ult_st
                self.YIELD_ST = yield_st
                self.CURV_FF = curv_fric_fac
                self.WOBBLE_FF = wob_fric_fac
            
            def json(self):
                bs_json ={
                    "RM" : 7,
                    "RV" : self.FACTOR,
                    "US" : self.ULT_ST,
                    "YS" : self.YIELD_ST,
                    "FF" : self.CURV_FF,
                    "WF" : self.WOBBLE_FF
                }
                return bs_json
            
            def __str__(self):
                return str(self.__dict__)
            
        class Null:
            
            def __init__(self,ult_st,yield_st,curv_fric_fac=0,wob_fric_fac=0):

                self.CODE = 'No Relaxation'

                self.ULT_ST = ult_st
                self.YIELD_ST = yield_st
                self.CURV_FF = curv_fric_fac
                self.WOBBLE_FF = wob_fric_fac
            
            def json(self):
                bs_json ={
                    "RM" : 0,
                    "RV" : 0,
                    "US" : self.ULT_ST,
                    "YS" : self.YIELD_ST,
                    "FF" : self.CURV_FF,
                    "WF" : self.WOBBLE_FF,
                    "bRELAX" : False
                }
                return bs_json
            
            def __str__(self):
                return str(self.__dict__)

        class Magura:
            
            def __init__(self,factor,ult_st,yield_st,curv_fric_fac=0,wob_fric_fac=0):

                self.CODE = 'Magura'

                if factor not in [10,45]:
                    factor = 45
                
                self.FACTOR = factor

                self.ULT_ST = ult_st
                self.YIELD_ST = yield_st
                self.CURV_FF = curv_fric_fac
                self.WOBBLE_FF = wob_fric_fac
            
            def json(self):
                bs_json ={
                    "RM" : 0,
                    "RV" : self.FACTOR,
                    "US" : self.ULT_ST,
                    "YS" : self.YIELD_ST,
                    "FF" : self.CURV_FF,
                    "WF" : self.WOBBLE_FF
                }
                return bs_json
            
            def __str__(self):
                return str(self.__dict__)
                                     
    # -----------------   TENDON    PROPERTY  --------------------------
    class Property:
        properties =[]
        ids = []

        def __init__(self,name,type,matID:int,tdn_area,duct_dia,relaxation,ext_mom_mag=0,anch_slip_begin=0,anch_slip_end=0,bond_type:bool=True,id=0):
            
            '''
            type = ['Internal (Pre-tension)' , 'Internal (Post-tenstion)' , 'External'] =>  1,2,3
            '''
            if Tendon.Property.ids == []: 
                tp_count = 1
            else:
                tp_count = max(Tendon.Property.ids)+1
            
            if id == 0 : self.ID = tp_count
            if id != 0 : self.ID = id

            self.NAME = name

            if type == 2:
                self.TYPE = 'INTERNAL'
                self.TENS = 'POST'
            elif type == 3:
                self.TYPE = 'EXTERNAL'
                self.TENS = 'PRE'
            else :
                self.TYPE = 'INTERNAL'
                self.TENS = 'PRE'

            self.MAT = matID
            self.TDN_AREA = tdn_area
            self.DUCT_DIA = duct_dia

            self.RELAX = relaxation

            self.EXT_MOM_MAG = ext_mom_mag
            self.ANC_SLIP_B = anch_slip_begin
            self.ANC_SLIP_E = anch_slip_end
            self.BOND_TYPE = bond_type

            Tendon.Property.properties.append(self)
            Tendon.Property.ids.append(self.ID)

        @classmethod
        def json(cls):
            json = {"Assign":{}}

            for self in cls.properties:
                json['Assign'][self.ID]={
                    "NAME" : self.NAME,
                    "TYPE" : self.TYPE,
                    "LT" : self.TENS,
                    "MATL" : self.MAT,
                    "AREA" : self.TDN_AREA,
                    "D_AREA" : self.DUCT_DIA,
                    "ASB" : self.ANC_SLIP_B,
                    "ASE" : self.ANC_SLIP_E,
                    "bBONDED" : self.BOND_TYPE,
                    "ALPHA" : self.EXT_MOM_MAG
                }
                json['Assign'][self.ID].update(self.RELAX.json())
            
            return json
        
        @classmethod
        def create(cls):
            MidasAPI("PUT","/db/TDNT",cls.json())


        @classmethod
        def get(cls):
            return MidasAPI('GET','/db/TDNT')
        
        @classmethod
        def delete(cls):
            MidasAPI("DELETE","/db/TDNT")
            cls.properties = []
            cls.ids = []


        @classmethod
        def sync(cls):
            a = cls.get()
            if a != {'message': ''}:
                if list(a['TDNT'].keys()) != []:
                    cls.properties = []
                    cls.ids=[]
                    for id in a['TDNT'].keys():
                        _JStoObj_Prop(int(id),a['TDNT'][id])


    # -----------------   TENDON    PROFILE  --------------------------
    class Profile:
        profiles =[]
        ids=[]

        def __init__(self,name,tdn_prop,tdn_group=0,elem=[],inp_type='3D',curve_type = 'SPLINE',st_len_begin = 0 , st_len_end = 0,n_typical_tendon=0,
                     trans_len_opt='USER', trans_len_begin = 0 , trans_len_end = 0, debon_len_begin=0 , debon_len_end=0,
                     ref_axis = 'ELEMENT',
                     prof_xyz = [], prof_xy =[],prof_xz=[],
                     prof_ins_point_end = 'END-I', prof_ins_point_elem = 0, x_axis_dir_element = 'I-J', x_axis_rot_ang = 0 , projection = True, offset_y = 0 , offset_z = 0,
                     prof_ins_point =[0,0,0], x_axis_dir_straight = 'X' , x_axis_dir_vec = [0,0], grad_rot_axis = 'X', grad_rot_ang=0,
                     radius_cen = [0,0], offset = 0, dir = 'CW',
                     id=0):
            '''
                TDN GROUP = Group ID
            '''



            if Tendon.Profile.ids == []: 
                td_count = 1
            else:
                td_count = max(Tendon.Profile.ids)+1
            
            if id == 0 : self.ID = td_count
            else : self.ID = id

            self.NAME = name
            self.PROP = tdn_prop
            self.GROUP = tdn_group
            self.ELEM = elem

            if inp_type not in ['2D' , '3D']: inp_type = '3D'
            self.INPUT = inp_type

            if curve_type not in ['SPLINE' , 'ROUND']: curve_type = 'ROUND'
            self.CURVE = curve_type

            self.BELENG = st_len_begin
            self.ELENG = st_len_end

            
            self.CNT = n_typical_tendon 
            if n_typical_tendon > 0: 
                self.bTP = True
            else: self.bTP = False

            if trans_len_opt not in ['USER' , 'AUTO']: trans_len_opt = 'USER'
            self.LENG_OPT = trans_len_opt
            self.BLEN = trans_len_begin
            self.ELEN =  trans_len_end

            self.DeBondBLEN = debon_len_begin
            self.DeBondELEN = debon_len_end

            if ref_axis not in ['ELEMENT' , 'STRAIGHT' , 'CURVE']: ref_axis = 'ELEMENT'
            self.SHAPE = ref_axis

            #------- ELEMENT TYPE -------------

            if prof_ins_point_end not in ['END-I' , 'END-J']: prof_ins_point_end = 'END-I'
            self.INS_PT = prof_ins_point_end

            if prof_ins_point_elem == 0: prof_ins_point_elem = elem[0]
            self.INS_ELEM = prof_ins_point_elem

            if x_axis_dir_element not in ['I-J' , 'J-I']: x_axis_dir_element = 'I-J'
            self.AXIS_IJ = x_axis_dir_element

            self.XAR_ANGLE = x_axis_rot_ang  # common in straight
            self.bPJ = projection # common in straight

            self.OFF_YZ = [offset_y,offset_z]

            #------- STRAIGHT TYPE -------------

            self.IP = prof_ins_point

            if x_axis_dir_straight not in ['X' , 'Y' , 'VECTOR']: x_axis_dir_straight = 'X'
            self.AXIS = x_axis_dir_straight

            self.VEC = x_axis_dir_vec


            if grad_rot_axis not in ['X' , 'Y']: grad_rot_axis = 'X'
            self.GR_AXIS = grad_rot_axis

            self.GR_ANGLE = grad_rot_ang

            #------- CURVE TYPE -------------

            self.RC = radius_cen
            self.OFFSET =  offset

            if dir not in ['CW' , 'CCW']: dir = 'CW'
            self.DIR = dir



            #---------------   PROFILES CREATION -----------------

            #----- 3D Profile (Round + Spline) -------------
            xyz_loc = []
            bFix = []
            R_spline3d = []
            R_round3d = []

            for point in prof_xyz:
                xyz_loc.append(_POINT_(point[0],point[1],point[2]))
                bFix.append(False) # Default not defining here
                if curve_type == 'SPLINE':
                    R_spline3d.append([0,0])   # Default not defining here
                else:
                    R_round3d.append(0)

            self.P_XYZ = xyz_loc

            self.bFIX = bFix
            self.R = R_spline3d
            self.RADIUS = R_round3d

            

            #----- 2D Profile Spline (only)-------------
            xy_loc = []
            xz_loc = []

            bFix_y = []
            bFix_z = []

            R_spline2d_Rz = []
            R_spline2d_Ry = []

            for point in prof_xy:
                xy_loc.append(_POINT_(point[0],point[1],0))
                bFix_y.append(False) # Default not defining here
                R_spline2d_Rz.append(0)

            for point in prof_xz:
                xz_loc.append(_POINT_(point[0],0,point[1]))
                bFix_z.append(False) # Default not defining here
                R_spline2d_Ry.append(0)


            self.P_XY = xy_loc
            self.P_XZ = xz_loc

            self.bFIX_XY = bFix_y
            self.bFIX_XZ = bFix_z

            self.R_XY = R_spline2d_Rz
            self.R_XZ = R_spline2d_Ry


            Tendon.Profile.profiles.append(self)
            Tendon.Profile.ids.append(self.ID)

        def update_profile(self,points_xyz):
            xyz_loc = []
            bFix = []
            R_spline3d = []
            R_round3d = []

            for point in points_xyz:
                xyz_loc.append(_POINT_(point[0],point[1],point[2]))
                bFix.append(False) # Default not defining here
                R_spline3d.append([0,0])   # Default not defining here

            self.P_XYZ = xyz_loc
            self.INPUT = '3D'
            self.CURVE = 'SPLINE'
            self.SHAPE = 'STRAIGHT'

            self.bFIX = bFix
            self.R = R_spline3d
            self.RADIUS = R_round3d

        @classmethod
        def json(cls):

            json = {"Assign":{}}

            for self in cls.profiles:
                json["Assign"][self.ID] = {
                                    'NAME' : self.NAME,
                                    'TDN_PROP' : self.PROP,
                                    'ELEM' : self.ELEM,
                                    'BELENG' : self.BELENG,
                                    'ELENG' : self.ELENG,
                                    'CURVE' : self.CURVE,
                                    'INPUT' : self.INPUT,
                                    'TDN_GRUP' : self.GROUP,
                                    "LENG_OPT": self.LENG_OPT,
                                    "BLEN": self.BLEN,
                                    "ELEN": self.ELEN,
                                    "bTP": self.bTP,
                                    "CNT": self.CNT,
                                    "DeBondBLEN": self.DeBondBLEN,
                                    "DeBondELEN": self.DeBondELEN,
                                    "SHAPE": self.SHAPE
                                }
                # --------------------------------   2D OR 3D (ROUND/SPLINE)--------------------------
                if self.INPUT == '3D':

                    # -------- 3D  ------------
                    array_temp = []

                    # -------- 3D SPLINE & ROUND ------------
                    if self.CURVE == 'ROUND' :
                        for j in range(len(self.P_XYZ)):
                            array_temp.append({
                                    'PT' : [self.P_XYZ[j].X,self.P_XYZ[j].Y,self.P_XYZ[j].Z],
                                    'bFIX' : self.bFIX[j],
                                    'RADIUS' : self.RADIUS[j]
                            })
                    else:
                        for j in range(len(self.P_XYZ)):
                            array_temp.append({
                                    'PT' : [self.P_XYZ[j].X,self.P_XYZ[j].Y,self.P_XYZ[j].Z],
                                    'bFIX' : self.bFIX[j],
                                    'R' : self.R[j]
                            })
                    
                    
                    
                    
                    # --- 3D Main ----

                    json_prof = {
                                    "PROF":array_temp
                                }

                elif self.INPUT == '2D':

                    # -------- 2D  ------------
                    array_y_temp = []
                    array_z_temp = []

                    # -------- 2D ONLY SPLINE  NOT ROUND ❌ ------------

                    for j in range(len(self.P_XY)):
                            array_y_temp.append({
                                    'PT' : [self.P_XY[j].X,self.P_XY[j].Y],
                                    'bFIX' : self.bFIX_XY[j],
                                    'R' : self.R_XY[j]
                            })

                    for j in range(len(self.P_XZ)):
                            array_z_temp.append({
                                    'PT' : [self.P_XZ[j].X,self.P_XZ[j].Z],
                                    'bFIX' : self.bFIX_XZ[j],
                                    'R' : self.R_XZ[j]
                            })

                    
                    # --- 3D Main ----

                    json_prof = {
                                    "PROFY":array_y_temp,
                                    "PROFZ":array_z_temp
                                }
                    
                # -------------------------------------------     TYPE  (ELEMNENT , STRAIGHT , CURVE)   ------------------------------------

                # ----- 3D Spline Element--------
                if self.SHAPE == 'ELEMENT' :
                    json_shape={
                                            "INS_PT": self.INS_PT,
                                            "INS_ELEM": self.INS_ELEM,
                                            "AXIS_IJ": self.AXIS_IJ,
                                            "XAR_ANGLE": self.XAR_ANGLE,
                                            "bPJ": self.bPJ,
                                            "OFF_YZ": self.OFF_YZ,
                                            }
                    
                # ----- 3D Spline Straight --------
                elif self.SHAPE == 'STRAIGHT' :
                    json_shape={
                                            "IP" : self.IP,
                                            "AXIS" : self.AXIS,
                                            "VEC" : self.VEC,
                                            "XAR_ANGLE": self.XAR_ANGLE,
                                            "bPJ": self.bPJ,
                                            "GR_AXIS": self.GR_AXIS,
                                            "GR_ANGLE": self.GR_ANGLE,
                                            }
                    
                # ----- 3D Spline Curve --------
                elif self.SHAPE == 'CURVE' :
                    json_shape={
                                            "IP" : self.IP,
                                            "RC" : self.RC,
                                            "OFFSET" : self.OFFSET,
                                            "DIR" : self.DIR,
                                            "XAR_ANGLE": self.XAR_ANGLE,
                                            "bPJ": self.bPJ,
                                            "GR_AXIS": self.GR_AXIS,
                                            "GR_ANGLE": self.GR_ANGLE,
                                            }
                
                json["Assign"][self.ID].update(json_shape)
                json["Assign"][self.ID].update(json_prof)
                        
            return json
        

        @classmethod
        def create(cls):
            MidasAPI("PUT","/db/TDNA",cls.json())


        @classmethod
        def get(cls):
            return MidasAPI('GET','/db/TDNA')
        
        @classmethod
        def delete(cls):
            cls.profiles=[]
            cls.ids=[]
            return MidasAPI('DELETE','/db/TDNA')
        
        @classmethod
        def sync(cls):
            a = cls.get()
            if a != {'message': ''}:
                if list(a['TDNA'].keys()) != []:
                    cls.profiles = []
                    cls.ids=[]
                    for id in a['TDNA'].keys():
                        _JStoObj_Profile(int(id),a['TDNA'][id])

    # ---------------------    END   CLASSS   -----------------------------------------------------


    class Prestress:
        """Prestress Loading for Tendons.
        """
        loads = []
        ids = []
        def __init__(self, profile_name, load_case, load_group = "", prestress_type = "STRESS", jack_step = "BEGIN", jack_begin = 0, jack_end=0, grouting_stage = 0, id = 0):


            if id > -1 :
                chk = 0
                for i in Load_Case.cases:
                    if load_case in i.NAME: chk = 1
                if chk == 0: Load_Case("PS", load_case)
                if load_group != "":
                    chk = 0
                    a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                    if load_group in a: chk = 1
                    if chk == 0: Group.Load(load_group)


                if prestress_type not in ['STRESS' , 'FORCE']: prestress_type = 'STRESS'
                if jack_step not in ['BEGIN' , 'END' , 'BOTH']: jack_step = 'BEGIN'

                self.TDN_ID = 0
                if id == 0: id = len(Tendon.Prestress.loads) + 1
                self.ID = id
            else:
                self.TDN_ID = -id//100000
                self.ID = -id%100000
            

            self.TDN_NAME = profile_name

            self.LCNAME = load_case
            self.LDGR = load_group
            self.TYPE =prestress_type
            self.ORDER = jack_step

            self.JACK_BEGIN = jack_begin
            self.JACK_END = jack_end
            self.GROUTING = grouting_stage

            

            Tendon.Prestress.loads.append(self)
            Tendon.Prestress.ids.append(self.ID)
            

        @classmethod
        def json(cls):
            json = {"Assign": {}}
            for self in cls.loads:

                # Finding Tendon ID
                tdn_id = self.TDN_ID
                if not self.TDN_ID :
                    tdn_check=0
                    for prof in Tendon.Profile.profiles:
                        if prof.NAME == self.TDN_NAME:
                            tdn_id = prof.ID
                            tdn_check=1
                            break
                    if not tdn_check: 
                        print(f'⚠️   "{self.TDN_NAME}" Tendon name is not found for Prestress load application. Prestress load skipped.\n📑  Try Tendon.Profile.sync() to retrieve Profile Names first')
                        continue


                if tdn_id not in list(json["Assign"].keys()):
                    json["Assign"][tdn_id] = {"ITEMS": []}

                json["Assign"][tdn_id]["ITEMS"].append({
                                        "ID": self.ID,
                                        "LCNAME": self.LCNAME,
                                        "GROUP_NAME": self.LDGR,
                                        "TENDON_NAME": self.TDN_NAME,
                                        "TYPE": self.TYPE,
                                        "ORDER": self.ORDER,
                                        "BEGIN": self.JACK_BEGIN,
                                        "END": self.JACK_END,
                                        "GROUTING": self.GROUTING
                                    })
            return json
        
        @classmethod
        def create(cls):
            MidasAPI("PUT", "/db/TDPL",cls.json())

        @classmethod
        def get(cls):
            return MidasAPI("GET", "/db/TDPL")
        
        @classmethod
        def delete(cls):
            cls.loads=[]
            return MidasAPI("DELETE", "/db/TDPL")
        
        @classmethod
        def sync(cls):
            cls.loads = []
            a = cls.get()
            if a != {'message': ''}:
                for i in a['TDPL'].keys():
                    for j in range(len(a['TDPL'][i]['ITEMS'])):
                        Tendon.Prestress(a['TDPL'][i]['ITEMS'][j]['TENDON_NAME'],a['TDPL'][i]['ITEMS'][j]['LCNAME']
                                         ,a['TDPL'][i]['ITEMS'][j]['GROUP_NAME']
                                         ,a['TDPL'][i]['ITEMS'][j]['TYPE']
                                         ,a['TDPL'][i]['ITEMS'][j]['ORDER']
                                         ,a['TDPL'][i]['ITEMS'][j]['BEGIN']
                                         ,a['TDPL'][i]['ITEMS'][j]['END']
                                         ,a['TDPL'][i]['ITEMS'][j]['GROUTING']
                                         ,-(100000*int(i)+int(a['TDPL'][i]['ITEMS'][j]['ID'])))