from ._offsetSS import Offset
from ._offsetSS import _common
import math

class _SS_TAPERED_DBUSER(_common):

    """ Create Standard USER DEFINED sections"""

    def __init__(self,Name='',Shape='',params_I:list=[],params_J:list=[],Offset=Offset(),useShear=True,use7Dof=False,id:int=0):  
        """ Shape = 'SB' 'SR' for rectangle \n For cylinder"""
        self.ID = id
        self.NAME = Name
        self.TYPE = 'TAPERED'
        self.SHAPE = Shape
        self.PARAMS_I = params_I
        self.PARAMS_J = params_J
        self.OFFSET = Offset
        self.USESHEAR = useShear
        self.USE7DOF = use7Dof
        self.DATATYPE = 2
    
    def __str__(self):
         return f'  >  ID = {self.ID}   |  USER DEFINED STANDARD SECTION \nJSON = {self.toJSON()}\n'


    def toJSON(sect):
        js =  {
                "SECTTYPE": sect.TYPE,
                "SECT_NAME": sect.NAME,
                "SECT_BEFORE": {
                    "SHAPE": sect.SHAPE,
                    "TYPE": sect.DATATYPE,
                    "SECT_I": {
                        "vSIZE": sect.PARAMS_I
                    },
                    "SECT_J": {
                        "vSIZE": sect.PARAMS_J
                    }
                }
            }
        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js
    
    @staticmethod
    def _objectify(id,name,type,shape,offset,uShear,u7DOF,js):
        return _SS_TAPERED_DBUSER(name,shape,js['SECT_BEFORE']['SECT_I']['vSIZE'],js['SECT_BEFORE']['SECT_J']['vSIZE'],offset,uShear,u7DOF,id)
    
    def _centerLine(shape,end,*args):
        if end: 
            shape.PARAMS = shape.PARAMS_J
            # print(' J end taken')
        else: 
            # print(' I end taken')
            shape.PARAMS = shape.PARAMS_I

        if shape.SHAPE == 'SB' :
            H,B = shape.PARAMS[:2]

            sect_lin_con = [[1,2],[3,1]]

            sect_cg_LT = [-B/2,H/2]
            sect_cg_CC = [0,0]
            sect_cg_RB = [B/2,-H/2]

            if H > B :
                sect_shape = [[0,0],[0,H/2],[0,-H/2],[0,H/4],[0,-H/4]]
                sect_thk = [B,B,B,B]
                sect_thk_off = [0,0,0,0]
            else : 
                sect_shape = [[0,0],[B/2,0],[-B/2,0],[B/4,0],[-B/4,0]]
                sect_thk = [H,H,H,H]
                sect_thk_off = [0,0,0,0]

        elif shape.SHAPE == 'L' :
            H,B,tw,tf = shape.PARAMS[:4]

            sect_cg_LT = [0,0]
            sect_cg_CC = [(H*tw*tw+B*B*tf)/(2*(B*tw+H*tf)),-(H*H*tw+B*tf*tf)/(2*(B*tw+H*tf))]
            sect_cg_RB = [B,-H]

            # sect_shape = [[0.5*tw,-H],[0.5*tw,-0.5*tf],[B,-0.5*tf]]
            sect_shape = [[0,-H],[0,0],[B,0]]
            sect_lin_con = [[3,2],[2,1]]
            sect_thk = [tw,tf]
            # sect_thk_off = [0,0]
            sect_thk_off = [tw/2,tf/2]
        
        elif shape.SHAPE == 'C' :
            H,B1,tw,tf1,B2,tf2 = shape.PARAMS[:6]
            if B2 == 0 : B2 = B1
            if tf2 == 0 : tf2 = tf1

            sect_cg_LT = [0,0]
            sect_cg_CC = [(B1+B2)*0.2,-H*0.5]
            sect_cg_RB = [max(B1,B2),-H]

            # sect_shape = [[0.5*tw,-0.5*tf1],[B1,-0.5*tf1],[0.5*tw,-H+0.5*tf2],[B2,-H+0.5*tf2]]
            sect_shape = [[0,0],[B1,0],[0,-H],[B2,-H]]
            sect_lin_con = [[2,1],[1,3],[3,4]]
            sect_thk = [tf1,tw,tf2]
            # sect_thk_off = [0,0,0]
            sect_thk_off = [tf1/2,tw/2,tf2/2]

        elif shape.SHAPE == 'H' :
            H,B1,tw,tf1,B2,tf2,r1,r2 = shape.PARAMS[:8]
            if B2 == 0 : B2 = B1
            if tf2 == 0 : tf2 = tf1

            sect_cg_LT = [-0.5*max(B1,B2),0.5*H]
            sect_cg_CC = [0,0]
            sect_cg_RB = [0.5*max(B1,B2),-0.5*H]

            sect_shape = [[-0.5*B1,0.5*(H-tf1)],[0,0.5*(H-tf1)],[0.5*B1,0.5*(H-tf1)],[-0.5*B2,-0.5*(H-tf2)],[0,-0.5*(H-tf2)],[0.5*B2,-0.5*(H-tf2)]]
            sect_lin_con = [[2,1],[3,2],[2,5],[4,5],[5,6]]
            sect_thk = [tf1,tf1,tw,tf2,tf2]
            sect_thk_off = [0,0,0,0,0]
        
        elif shape.SHAPE == 'T' :
            H,B,tw,tf = shape.PARAMS[:4]

            sect_cg_LT = [-B*0.5,0]
            sect_cg_CC = [0,-H*0.3]
            sect_cg_RB = [B*0.5,-H]

            sect_shape = [[-0.5*B,-0.5*tf],[0,-0.5*tf],[0.5*B,-0.5*tf],[0,-H]]
            sect_lin_con = [[2,1],[3,2],[2,4]]
            sect_thk = [tf,tf,tw]
            sect_thk_off = [0,0,0]

        elif shape.SHAPE == 'B' :
            H,B,tw,tf1,C,tf2 = shape.PARAMS[:6]
            if tf2 == 0 : tf2 = tf1

            sect_cg_LT = [-0.5*B,0.5*H]
            sect_cg_CC = [0,0]
            sect_cg_RB = [0.5*B,-0.5*H]

            # sect_shape = [[0.5*(B-tw),0.5*(H-tf1)],[-0.5*(B-tw),0.5*(H-tf1)],[-0.5*(B-tw),-0.5*(H-tf2)],[0.5*(B-tw),-0.5*(H-tf2)]]
            sect_shape = [[0.5*B,0.5*H],[-0.5*B,0.5*H],[-0.5*B,-0.5*H],[0.5*B,-0.5*H]]

            sect_lin_con = [[1,2],[2,3],[3,4],[4,1]]
            sect_thk = [tf1,tw,tf2,tw]
            # sect_thk_off = [0,0,0,0]
            sect_thk_off = [0.5*tf1,0.5*tw,0.5*tf2,0.5*tw]
        
        elif shape.SHAPE == 'P' :
            D,tw = shape.PARAMS[:2]

            # R = 0.5*(D-tw)
            R = 0.5*D

            sect_cg_LT = [-R,R]
            sect_cg_CC = [0,0]
            sect_cg_RB = [R,-R]

            sect_shape = []
            sect_lin_con = []
            sect_thk = []
            sect_thk_off = []

            n = 16
            for i in range(n):
                sect_shape.append([R*math.sin(i*2*math.pi/n),R*math.cos(i*2*math.pi/n)])
                sect_lin_con.append([i+1,i+2])
                sect_thk.append(tw)
                sect_thk_off.append(-0.5*tw)
            sect_lin_con[-1] = [i+1,1]



        sect_cg = (sect_cg_LT,sect_cg_CC,sect_cg_RB)

        return sect_shape, sect_thk ,sect_thk_off, sect_cg , sect_lin_con