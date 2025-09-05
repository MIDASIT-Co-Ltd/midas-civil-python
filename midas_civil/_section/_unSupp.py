from ._offsetSS import _common


class _SS_UNSUPP(_common):

    """ Store Unsupported section"""

    def __init__(self,id,name,type,shape,offset,uShear,u7DOF,js):  
        """ Shape = 'SB' 'SR' for rectangle \n For cylinder"""
        self.ID = id
        self.NAME = name
        self.TYPE = type
        self.SHAPE = shape
        self.OFFSET = offset
        self.USESHEAR = uShear
        self.USE7DOF = u7DOF
        self.DATATYPE = 2
        self.JS = js
    
    def __str__(self):
         return f'  >  ID = {self.ID}   |  Unsupported Section \nJSON = {self.JS}\n'


    def toJSON(sect):
        js = sect.JS
        js['SECT_NAME'] = sect.NAME
        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js
    
class _SS_STD_DB(_common):

    """ Store Unsupported section"""

    def __init__(self,id,name,type,shape,offset,uShear,u7DOF,js):  
        """ Shape = 'SB' 'SR' for rectangle \n For cylinder"""
        self.ID = id
        self.NAME = name
        self.TYPE = type
        self.SHAPE = shape
        self.OFFSET = offset
        self.USESHEAR = uShear
        self.USE7DOF = u7DOF
        self.DATATYPE = 2
        self.JS = js
    
    def __str__(self):
         return f'  >  ID = {self.ID}   |  STANDARD CODAL SECTION \nJSON = {self.JS}\n'


    def toJSON(sect):
        js = sect.JS
        js['SECT_NAME'] = sect.NAME
        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js