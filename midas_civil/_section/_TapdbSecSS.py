from ._offsetSS import Offset
from ._offsetSS import _common

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