
from ._mapi import *
from ._utils import *


#5 Class to create nodes
class Tendon:

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



            if Tendon.Profile.ids == []: 
                td_count = 1
            else:
                td_count = max(Tendon.Profile.ids)+1
            
            if id == 0 : self.ID = td_count
            if id != 0 : self.ID = id

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
            x_loc = []
            y_loc = []
            z_loc = []
            bFix = []
            Rd = []
            Rl = []

            for point in prof_xyz:
                x_loc.append(point[0])
                y_loc.append(point[1])
                z_loc.append(point[2])
                bFix.append(False) # Default not defining here
                if curve_type == 'SPLINE':
                    Rd.append([0,0])   # Default not defining here
                else:
                    Rl.append(0)

            #----- 3D Profile -------------

            self.X = x_loc
            self.Y = y_loc
            self.Z = z_loc
            self.bFIX = bFix

            self.R = Rd
            self.RADIUS = Rl


            #----- 2D Profile -------------





            Tendon.Profile.profiles.append(self)
            Tendon.Profile.ids.append(self.ID)



        @classmethod
        def json(cls):

            json = {"Assign":{}}

            for self in cls.profiles:

                array_temp = []
                for j in range(len(self.X)):
                    array_temp.append({
                        'PT' : [self.X[j],self.Y[j],self.Z[j]],
                        'bFIX' : self.bFIX[j],
                        'R' : self.R[j]
                    })
                
                json["Assign"][self.ID]={
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
                                        "SHAPE": self.SHAPE,
                                        "INS_PT": self.INS_PT,
                                        "INS_ELEM": self.INS_ELEM,
                                        "AXIS_IJ": self.AXIS_IJ,
                                        "XAR_ANGLE": self.XAR_ANGLE,
                                        "bPJ": self.bPJ,
                                        "OFF_YZ": self.OFF_YZ,

                                        "PROF":array_temp
                                        }
            return json
        

        @classmethod
        def create(cls):
            MidasAPI("PUT","/db/TDNA",cls.json())


        @classmethod
        def get(cls):
            return MidasAPI('GET','/db/TDNA')
        
        @classmethod
        def sync(cls):
            tendon_json = cls.get()
            for id in tendon_json['TDNA']:
                Tendon.Profile(tendon_json['TDNA'][id],id)

    # ---------------------    END   CLASSS   -----------------------------------------------------