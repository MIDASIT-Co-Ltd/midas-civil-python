from ._offsetSS import Offset
from ._offsetSS import _common



class _SS_TAP_PSC_1CELL(_common):
    def __init__(self,Name='',Joint=[0,0,0,0,0,0,0,0],
                    HO1_I=0,HO2_I=0,HO21_I=0,HO22_I=0,HO3_I=0,HO31_I=0,
                    BO1_I=0,BO11_I=0,BO12_I=0,BO2_I=0,BO21_I=0,BO3_I=0,
                    HI1_I=0,HI2_I=0,HI21_I=0,HI22_I=0,HI3_I=0,HI31_I=0,HI4_I=0,HI41_I=0,HI42_I=0,HI5_I=0,
                    BI1_I=0,BI11_I=0,BI12_I=0,BI21_I=0,BI3_I=0,BI31_I=0,BI32_I=0,BI4_I=0,

                    HO1_J=0,HO2_J=0,HO21_J=0,HO22_J=0,HO3_J=0,HO31_J=0,
                    BO1_J=0,BO11_J=0,BO12_J=0,BO2_J=0,BO21_J=0,BO3_J=0,
                    HI1_J=0,HI2_J=0,HI21_J=0,HI22_J=0,HI3_J=0,HI31_J=0,HI4_J=0,HI41_J=0,HI42_J=0,HI5_J=0,
                    BI1_J=0,BI11_J=0,BI12_J=0,BI21_J=0,BI3_J=0,BI31_J=0,BI32_J=0,BI4_J=0,

                    Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
                
        self.ID = id
        self.NAME = Name
        self.SHAPE = '1CEL'
        self.TYPE = 'TAPERED'

        self.JO1=bool(Joint[0])
        self.JO2=bool(Joint[1])
        self.JO3=bool(Joint[2])
        self.JI1=bool(Joint[3])
        self.JI2=bool(Joint[4])
        self.JI3=bool(Joint[5])
        self.JI4=bool(Joint[6])
        self.JI5=bool(Joint[7])

        self.OFFSET = Offset
        self.USESHEAR = bool(useShear)
        self.USE7DOF = bool(use7Dof)

        self.HO1_I = HO1_I
        self.HO2_I = HO2_I
        self.HO21_I = HO21_I
        self.HO22_I= HO22_I
        self.HO3_I = HO3_I
        self.HO31_I = HO31_I

        self.BO1_I = BO1_I
        self.BO11_I = BO11_I
        self.BO12_I = BO12_I
        self.BO2_I = BO2_I
        self.BO21_I = BO21_I
        self.BO3_I = BO3_I

        self.HI1_I = HI1_I
        self.HI2_I = HI2_I
        self.HI21_I = HI21_I
        self.HI22_I = HI22_I
        self.HI3_I = HI3_I
        self.HI31_I = HI31_I
        self.HI4_I = HI4_I
        self.HI41_I = HI41_I
        self.HI42_I = HI42_I
        self.HI5_I = HI5_I

        self.BI1_I = BI1_I
        self.BI11_I = BI11_I
        self.BI12_I = BI12_I
        self.BI21_I = BI21_I
        self.BI3_I = BI3_I
        self.BI31_I = BI31_I
        self.BI32_I = BI32_I
        self.BI4_I = BI4_I




        self.HO1_J = HO1_J
        self.HO2_J = HO2_J
        self.HO21_J = HO21_J
        self.HO22_J= HO22_J
        self.HO3_J = HO3_J
        self.HO31_J = HO31_J

        self.BO1_J = BO1_J
        self.BO11_J = BO11_J
        self.BO12_J = BO12_J
        self.BO2_J = BO2_J
        self.BO21_J = BO21_J
        self.BO3_J = BO3_J

        self.HI1_J = HI1_J
        self.HI2_J = HI2_J
        self.HI21_J = HI21_J
        self.HI22_J = HI22_J
        self.HI3_J = HI3_J
        self.HI31_J = HI31_J
        self.HI4_J = HI4_J
        self.HI41_J = HI41_J
        self.HI42_J = HI42_J
        self.HI5_J = HI5_J

        self.BI1_J = BI1_J
        self.BI11_J = BI11_J
        self.BI12_J = BI12_J
        self.BI21_J = BI21_J
        self.BI3_J = BI3_J
        self.BI31_J = BI31_J
        self.BI32_J = BI32_J
        self.BI4_J = BI4_J

    
    def __str__(self):
         return f'  >  ID = {self.ID}   |  PSC 1-2 CELL SECTION \nJSON = {self.toJSON()}\n'


    def toJSON(sect):
        js =  {
                "SECTTYPE": "TAPERED",
                "SECT_NAME": sect.NAME,
                "SECT_BEFORE": {
                    "SHAPE": sect.SHAPE,
                    "TYPE" : 11,
                    "SECT_I": {
                        "vSIZE_PSC_A": [sect.HO1_I,sect.HO2_I,sect.HO21_I,sect.HO22_I,sect.HO3_I,sect.HO31_I],
                        "vSIZE_PSC_B": [sect.BO1_I,sect.BO11_I,sect.BO12_I,sect.BO2_I,sect.BO21_I,sect.BO3_I,],
                        "vSIZE_PSC_C": [sect.HI1_I,sect.HI2_I,sect.HI21_I,sect.HI22_I,sect.HI3_I,sect.HI31_I,sect.HI4_I,sect.HI41_I,sect.HI42_I,sect.HI5_I],
                        "vSIZE_PSC_D": [sect.BI1_I,sect.BI11_I,sect.BI12_I,sect.BI21_I,sect.BI3_I,sect.BI31_I,sect.BI32_I,sect.BI4_I],
                        "S_WIDTH" : sect.HO1_I
                    },
                    "SECT_J": {
                        "vSIZE_PSC_A": [sect.HO1_J,sect.HO2_J,sect.HO21_J,sect.HO22_J,sect.HO3_J,sect.HO31_J],
                        "vSIZE_PSC_B": [sect.BO1_J,sect.BO11_J,sect.BO12_J,sect.BO2_J,sect.BO21_J,sect.BO3_J,],
                        "vSIZE_PSC_C": [sect.HI1_J,sect.HI2_J,sect.HI21_J,sect.HI22_J,sect.HI3_J,sect.HI31_J,sect.HI4_J,sect.HI41_J,sect.HI42_J,sect.HI5_J],
                        "vSIZE_PSC_D": [sect.BI1_J,sect.BI11_J,sect.BI12_J,sect.BI21_J,sect.BI3_J,sect.BI31_J,sect.BI32_J,sect.BI4_J],
                        "S_WIDTH" : sect.HO1_J
                    },
                    "Y_VAR": 1,
                    "Z_VAR": 1,
                    "WARPING_CHK_AUTO_I": True,
                    "WARPING_CHK_AUTO_J": True,
                    "SHEAR_CHK": False,
                    "WARPING_CHK_POS_I": [[0,0,0,0,0,0],[0,0,0,0,0,0]],
                    "WARPING_CHK_POS_J": [[0,0,0,0,0,0],[0,0,0,0,0,0]],
                    "USE_WEB_THICK_SHEAR": [[True, True,True],[True,True,True]],
                    "WEB_THICK_SHEAR": [[0,0,0],[0,0,0]],
                    "USE_WEB_THICK": [True,True],
                    "WEB_THICK": [0,0],
                    "USE_SYMMETRIC": False,
                    "USE_SMALL_HOLE": False,
                    "USE_USER_DEF_MESHSIZE": False,
                    "USE_USER_INTPUT_STIFF": False,
                    "PSC_OPT1": "",
                    "PSC_OPT2": "",
                    "JOINT": [sect.JO1,sect.JO2,sect.JO3,sect.JI1,sect.JI2,sect.JI3,sect.JI4,sect.JI5]
                }
            }
        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js
    

    @staticmethod
    def _objectify(id,name,type,shape,offset,uShear,u7DOF,js):
        #--- PSC 1,2 CELL -------------------
        vA_I = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_A']
        vB_I = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_B']
        vC_I = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_C']
        vD_I = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_D']

        vA_J = js['SECT_BEFORE']['SECT_J']['vSIZE_PSC_A']
        vB_J = js['SECT_BEFORE']['SECT_J']['vSIZE_PSC_B']
        vC_J = js['SECT_BEFORE']['SECT_J']['vSIZE_PSC_C']
        vD_J = js['SECT_BEFORE']['SECT_J']['vSIZE_PSC_D']

        joint = js['SECT_BEFORE']['JOINT']
        return _SS_TAP_PSC_1CELL(name,joint,
                            *vA_I,*vB_I,*vC_I,*vD_I,
                            *vA_J,*vB_J,*vC_J,*vD_J,
                            offset,uShear,u7DOF,id)
    







