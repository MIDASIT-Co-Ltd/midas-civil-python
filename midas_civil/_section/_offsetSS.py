from midas_civil import MidasAPI
from typing import Literal

_offsetPt = Literal['LT','CT','RT','LC','CC','RC','LB','CB','RB']

class Offset:
    def __init__(self,OffsetPoint:_offsetPt='CC',CenterLocation:int=0,HOffset:float=0,HOffOpt:int=0,VOffset:float=0,VOffOpt:int=0,UsrOffOpt:int=0):
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
            0 : Centroid     |    1 : Centre of Section
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



        self.JS = {
            "OFFSET_PT": OffsetPoint,
            "OFFSET_CENTER": CenterLocation,

            "USER_OFFSET_REF": UsrOffOpt,
            "HORZ_OFFSET_OPT": HOffOpt,
            "USERDEF_OFFSET_YI": HOffset,

            "USERDEF_OFFSET_YJ": HOffset,   #Tapered only

            "VERT_OFFSET_OPT": VOffOpt,
            "USERDEF_OFFSET_ZI": VOffset,

            "USERDEF_OFFSET_ZJ": VOffset,   #Tapered only
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