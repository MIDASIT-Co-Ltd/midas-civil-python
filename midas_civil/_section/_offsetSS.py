from .._mapi import MidasAPI,NX
import numpy as np
from typing import Literal

_offsetPt = Literal['LT','CT','RT','LC','CC','RC','LB','CB','RB']
_AS_ST19 = Literal["T1","T2","T3","T4","T5"]

def _transformSecPT(pts,ox,oy,angle):
    points = np.array(pts)
    offset = np.array([ox, oy])
    theta = np.deg2rad(angle)  # Convert degrees to radians

    R = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

    r_points= points @ R.T
    t_points = r_points + offset

    rounded = np.round(t_points, 3)

    return rounded.tolist()

def _createArc(loc,radius,nSides,angS,angE,bFillet=True):
    angles = np.linspace(np.deg2rad(angS), np.deg2rad(angE), nSides+1, endpoint=True)
    points = np.column_stack((
        radius * np.cos(angles),
        radius * np.sin(angles)
    ))
    origin = np.array([loc])

    if radius==0:
        return origin
    if bFillet:
        totalPTs = origin+points-points[0]-points[-1]
    else:
        totalPTs = origin+points
    return totalPTs

def _DistUnitConvert(pts,initialUnit='MM',targetUnit=None):

    if targetUnit is None:
        if NX._isSyncUnit == False:
            # STARTING THE PLUGIN SYNCS UNIT
            resp = MidasAPI("GET","/db/UNIT")['UNIT']['1']
            NX.units = resp
            NX._isSyncUnit = True
        targetUnit = NX.units['DIST']
    

    len_multi = {
        "M" : 1,
        "CM" : 100,
        "MM" : 1000,
        "IN" : 39.3701,
        "FT" : 3.28084
    }
    
    len_multiplier = len_multi[targetUnit]/len_multi[initialUnit]

    return np.multiply(len_multiplier,pts)


class Offset:
    def __init__(self,OffsetPoint:_offsetPt='CC',CenterLocation:int=0,HOffset:float=0,HOffOpt:int=0,VOffset:float=0,VOffOpt:int=0,UsrOffOpt:int=0,HOffset_J:float=None,VOffset_J:float=None):
        '''
        Parameters
        ----------
        OffsetPoint : str
            Reference point for offset alignment. Default is 'CC' (center-center).     
            Can be 'LT','CT','RT','LC','CC','RC','LB','CB','RB' .    
        CenterLocation : int
            Specifies the central reference location. Default is 0.    
            0 : Centroid     |    1 : Centre of Section
        HOffset : float
            Horizontal offset value. Default is 0.
        HOffOpt : int
            Horizontal offset option flag controlling how HOffset is applied. Default is 0.    
            0 : Extreme fiber   |   1 : User
        VOffset : float
            Vertical offset value. Default is 0.
        VOffOpt : int
            Vertical offset option flag controlling how VOffset is applied. Default is 0.    
            0 : Extreme fiber   |   1 : User
        UsrOffOpt : int
            User-defined offset option flag for custom behavior. Default is 0.    
            0 : Centroid     |    1 : Extreme fiber

        HOffset_J : float   
            Horizontal offset value for J end. Applicable in Tapered sections. Default is 0.   
        VOffset_J : float   
            Vertical offset value for J end. Applicable in Tapered sections. Default is 0.   
        
        '''

        # self.OFFSET_PT =OffsetPoint
        # self.OFFSET_CENTER =CenterLocation
        # self.HORZ_OFFSET_OPT = HOffOpt
        # self.USERDEF_OFFSET_YI = HOffset
        # self.USERDEF_OFFSET_YJ = HOffset
        # self.VERT_OFFSET_OPT = VOffOpt
        # self.USERDEF_OFFSET_ZI = VOffset
        # self.USERDEF_OFFSET_ZJ = VOffset
        # self.USER_OFFSET_REF = UsrOffOpt

        # CenterLocation   0 -> Centroid   | 1-> Centre of Section
        # HOffset -> Horizontal offset distance
        # HOffOpt -> 0 -> Extreme fiber | 1 -> User

        if HOffset_J==None: HOffset_J = HOffset
        if VOffset_J==None: VOffset_J = VOffset

        self.JS = {
            "OFFSET_PT": OffsetPoint,
            "OFFSET_CENTER": CenterLocation,

            "USER_OFFSET_REF": UsrOffOpt,
            "HORZ_OFFSET_OPT": HOffOpt,
            "USERDEF_OFFSET_YI": HOffset,

            "USERDEF_OFFSET_YJ": HOffset_J,   #Tapered only

            "VERT_OFFSET_OPT": VOffOpt,
            "USERDEF_OFFSET_ZI": VOffset,

            "USERDEF_OFFSET_ZJ": VOffset_J,   #Tapered only
        }


    def __str__(self):
        return str(self.JS)
    
    @staticmethod
    def CC():
        return Offset('CC')
    
    @staticmethod
    def CT():
        return Offset('CT')
    
    @staticmethod
    def CB():
        return Offset('CB')
    
    @staticmethod
    def LC():
        return Offset('LC')
    
    @staticmethod
    def LT():
        return Offset('LT')
    
    @staticmethod
    def LB():
        return Offset('LB')
    
    @staticmethod
    def RC():
        return Offset('RC')
    
    @staticmethod
    def RT():
        return Offset('RT')
    
    @staticmethod
    def RB():
        return Offset('RB')
    

class _common:
    def update(self):
        js2s = {'Assign':{self.ID : self.toJSON()}}
        MidasAPI('PUT','/db/sect',js2s)
        return js2s
    
class Shape:
    def __init__(self,outerPTs,innerPTs=None,mat=(2.1e8,0.3,7.85)):
        self.N_INNER = 0
        self.N_OUTER = 0
        self.INNER = []
        self.OUTER = []

        self.MAT = mat

        if innerPTs is not None:
            if isinstance(innerPTs[0][0],(float,int)):
                # SINGLE HOLE
                self.N_INNER = 1
                self.INNER = [innerPTs]
            else:
                self.N_INNER = len(innerPTs)
                self.INNER = innerPTs

        if isinstance(outerPTs[0][0],(float,int)):
            # SINGLE OUTER
            self.N_OUTER = 1
            self.OUTER = [outerPTs]
        else:
            self.N_INNER = len(outerPTs)
            self.OUTER = outerPTs


    def __createSHAPE__(shape,col=None):
        import matplotlib.pyplot as plt
        def __createPoly__(pts,col=col):
            ptsList = list(pts)
            ptsList.append(pts[0])

            x, y = zip(*ptsList)
            # Scatter plot
            plt.fill(x, y,facecolor=col,edgecolor="#5C86F1",)

        for outerPts in shape.OUTER:
            __createPoly__(outerPts,"#A7C3FF")

        for holePts in shape.INNER:
            __createPoly__(holePts,"#ffffff75")

    def plot(shape):
        import matplotlib.pyplot as plt
        
        shape.__createSHAPE__()
        # If you want to connect the points:
        # plt.plot(x, y, '-o')
        plt.grid(False)
        plt.axis('equal')   # Optional: equal scaling on both axes
        plt.show()



    @staticmethod
    def rect(b:float,d:float,
            origin_X:float=0,origin_Y:float=0,angle:float=0):
        points = [(0.5*b,0.5*d),(-0.5*b,0.5*d),(-0.5*b,-0.5*d),(0.5*b,-0.5*d)]
        return _transformSecPT(points,origin_X,origin_Y,angle)
    
    @staticmethod
    def roundRect(b:float,d:float,radius:float=0,nSides:int=8,
            origin_X:float=0,origin_Y:float=0,angle:float=0):
        
        points = [
                    *_createArc((0.5*b,0.5*d),radius,nSides,0,90),
                    *_createArc((-0.5*b,0.5*d),radius,nSides,90,180),
                    *_createArc((-0.5*b,-0.5*d),radius,nSides,180,270),
                    *_createArc((0.5*b,-0.5*d),radius,nSides,270,360),
                ]
            
        return _transformSecPT(points,origin_X,origin_Y,angle)
    
    @staticmethod
    def circle(r:float,nSides:int=18,
            origin_X:float=0,origin_Y:float=0,angle:float=0):
        angles = np.linspace(0, 2 * np.pi, nSides, endpoint=False)

        points = np.column_stack((
            r * np.cos(angles),
            r * np.sin(angles)
        ))
                    
        return _transformSecPT(points,origin_X,origin_Y,angle)
    
    @staticmethod
    def i_shape(H,B1,tw,tf1,B2=None,tf2=None,r1=0,r2=0,nSides=8,
            origin_X:float=0,origin_Y:float=0,angle:float=0):
        
        if B2 is None: B2 = B1
        if tf2 is None: tf2 = tf1
        r2 = min(r2,0.95*tf1,0.95*tf2)
        points = [
                    (0.5*B1,0.5*H),(-0.5*B1,0.5*H),
                    *_createArc((-0.5*B1,0.5*H-tf1),r2,nSides,180,270),
                    *_createArc((-0.5*tw,0.5*H-tf1),r1,nSides,90,0),
                    *_createArc((-0.5*tw,-0.5*H+tf2),r1,nSides,0,-90),
                    *_createArc((-0.5*B2,-0.5*H+tf2),r2,nSides,90,180),
                    (-0.5*B2,-0.5*H),(0.5*B2,-0.5*H),
                    *_createArc((0.5*B2,-0.5*H+tf2),r2,nSides,0,90),
                    *_createArc((0.5*tw,-0.5*H+tf2),r1,nSides,270,180),
                    *_createArc((0.5*tw,0.5*H-tf1),r1,nSides,180,90),
                    *_createArc((0.5*B1,0.5*H-tf1),r2,nSides,-90,0),
                ]

        return _transformSecPT(points,origin_X,origin_Y,angle)
    
    @staticmethod
    def c_shape(H,B1,tw,tf1,B2=None,tf2=None,r1=0,r2=0,nSides=8,
            origin_X:float=0,origin_Y:float=0,angle:float=0):
        
        
        if B2 is None: B2 = B1
        if tf2 is None: tf2 = tf1
        r2 = min(r2,0.95*tf1,0.95*tf2)

        points = [
                    (B1,0.5*H),(0,0.5*H),
                    (0,-0.5*H),(B2,-0.5*H),
                    *_createArc((B2,-0.5*H+tf2),r2,nSides,0,90),
                    *_createArc((tw,-0.5*H+tf2),r1,nSides,270,180),
                    *_createArc((tw,0.5*H-tf1),r1,nSides,180,90),
                    *_createArc((B1,0.5*H-tf1),r2,nSides,-90,0),
                ]

        return _transformSecPT(points,origin_X,origin_Y,angle)

    @staticmethod
    def angle_shape(H,B,tw,tf,r1=0,r2=0,nSides=8,
            origin_X:float=0,origin_Y:float=0,angle:float=0):
        
        r2 = min(r2,0.95*tf,0.95*tw)

        points = [
                    (B,0),(0,0),(0,-H),
                    *_createArc((tw,-H),r2,nSides,-90,0),
                    *_createArc((tw,-tf),r1,nSides,180,90),
                    *_createArc((B,-tf),r2,nSides,-90,0),
                ]

        return _transformSecPT(points,origin_X,origin_Y,angle)
    
    @staticmethod
    def t_shape(H,B,tw,tf,r1=0,r2=0,nSides=8,
            origin_X:float=0,origin_Y:float=0,angle:float=0):
        

        r2 = min(r2,0.95*tf)
        points = [
                    (0.5*B,0.5*H),(-0.5*B,0.5*H),
                    *_createArc((-0.5*B,0.5*H-tf),r2,nSides,180,270),
                    *_createArc((-0.5*tw,0.5*H-tf),r1,nSides,90,0),
                    (-0.5*tw,-0.5*H),(0.5*tw,-0.5*H),
                    *_createArc((0.5*tw,0.5*H-tf),r1,nSides,180,90),
                    *_createArc((0.5*B,0.5*H-tf),r2,nSides,-90,0),
                ]

        return _transformSecPT(points,origin_X,origin_Y,angle)
    
    @staticmethod
    def AS_SuperT_RMS2019(type:_AS_ST19='T1',ModelUnit:str=None):
        ''' Base coordinates are in mm .
        Returns coordinates of section as per model units.
        
        '''
        

        pt_T1 = [(-1050,414.967),(-1050,324.967),(-613.5,324.967),(-506.421,250.301),
                    (-449.5,-350.033),(449.5,-350.033),(506.421,250.301),(613.5,324.967),
                    (1050,324.967),(1050,414.967),(446.5,414.967),(446.5,389.967),(419.128,389.967),
                    (379,-33.0333),(0,-105.033),(-379,-33.0333),(-419.128,389.967),(-446.5,389.967),
                    (-446.5,414.967)]
        pt_T2 = [(-1050,552.767),(-1050,462.767),(-613.5,462.767),(-506.437,388.101),(-426,-462.233),
                    (426,-462.233),(506.437,388.101),(613.5,462.767),(1050,462.767),(1050,552.767),
                    (446.5,552.767),(446.5,527.767),(419.135,527.767),(355,-150.233),(0,-217.233),
                    (-355,-150.233),(-419.135,527.767),(-446.5,527.767),(-446.5,552.767)]

        pt_T3 = [(-1050,663.558),(-1050,573.558),(-613.5,573.558),(-506.432,498.892),
                    (-407,-551.442),(407,-551.442),(506.432,498.892),(613.5,573.558),
                    (1050,573.558),(1050,663.558),(446.5,663.558),(446.5,638.558),(419.144,638.558),
                    (338,-222.442),(0,-286.442),(-338,-222.442),(-419.144,638.558),(-446.5,638.558),(-446.5,663.558)]      

        pt_T4 = [(-1050,813.180),(-1050,723.180),(-613.5,723.180),(-506.426,648.514),(-378.5,-701.82),
                    (378.5,-701.82),(506.426,648.514),(613.5,723.180),(1050,723.180),(1050,813.180),(446.5,813.180),
                    (446.5,788.180),(419.141,788.180),(309,-378.82),(0,-436.82),(-309,-378.82),(-419.14,788.180),(-446.5,788.180),(-446.5,813.180)]   
        
        pt_T5 = [(-1050,962.804),(-1050,872.804),(-613.5,872.804),(-506.423,798.138),
                    (-350,-852.196),(350,-852.196),(506.423,798.138),(613.5,872.804),(1050,872.804),
                    (1050,962.804),(426.5,962.804),(426.5,937.804),(399.122,937.804),(265,-472.196),(0,-522.196),
                    (-265,-472.196),(-399.122,937.804),(-426.5,937.804),(-426.5,962.804)]
        
        _map = {"T1":pt_T1,"T2":pt_T2,"T3":pt_T3,"T4":pt_T4,"T5":pt_T5,}

        return _DistUnitConvert(_map.get(type,_map['T1']),'MM',ModelUnit)