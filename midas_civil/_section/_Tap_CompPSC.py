from ._offsetSS import Offset
from ._offsetSS import _common



class _SS_TAP_COMP_PSC_I(_common):

    """ Create Standard USER DEFINED sections"""

    def __init__(self,Name='',Symm = True,Joint=[0,0,0,0,0,0,0,0,0],
                    Bc=0,tc=0,Hh=0,

                    # H1=0,
                    # HL1=0,HL2=0,HL21=0,HL22=0,HL3=0,HL4=0,HL41=0,HL42=0,HL5=0,
                    # BL1=0,BL2=0,BL21=0,BL22=0,BL4=0,BL41=0,BL42=0,

                    # HR1=0,HR2=0,HR21=0,HR22=0,HR3=0,HR4=0,HR41=0,HR42=0,HR5=0,
                    # BR1=0,BR2=0,BR21=0,BR22=0,BR4=0,BR41=0,BR42=0,

                    H1_I=0,
                    HL1_I=0, HL2_I=0, HL21_I=0, HL22_I=0, HL3_I=0, HL4_I=0, HL41_I=0, HL42_I=0, HL5_I=0,
                    BL1_I=0, BL2_I=0, BL21_I=0, BL22_I=0, BL4_I=0, BL41_I=0, BL42_I=0,
                    HR1_I=0, HR2_I=0, HR21_I=0, HR22_I=0, HR3_I=0, HR4_I=0, HR41_I=0, HR42_I=0, HR5_I=0,
                    BR1_I=0, BR2_I=0, BR21_I=0, BR22_I=0, BR4_I=0, BR41_I=0, BR42_I=0,

                    H1_J=0,
                    HL1_J=0, HL2_J=0, HL21_J=0, HL22_J=0, HL3_J=0, HL4_J=0, HL41_J=0, HL42_J=0, HL5_J=0,
                    BL1_J=0, BL2_J=0, BL21_J=0, BL22_J=0, BL4_J=0, BL41_J=0, BL42_J=0,
                    HR1_J=0, HR2_J=0, HR21_J=0, HR22_J=0, HR3_J=0, HR4_J=0, HR41_J=0, HR42_J=0, HR5_J=0,
                    BR1_J=0, BR2_J=0, BR21_J=0, BR22_J=0, BR4_J=0, BR41_J=0, BR42_J=0,

                    EgdEsb =0, DgdDsb=0,Pgd=0,Psb=0,TgdTsb=0,

                    MultiModulus = False,CreepEratio=0,ShrinkEratio=0,

                    Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
        
        self.ID = id
        self.NAME = Name
        self.SHAPE = 'CPCI'
        self.TYPE = 'TAPERED'

        self.SYMM = bool(Symm)

        self.BC =Bc
        self.TC =tc
        self.HH =Hh

        self.MATL_ELAST = EgdEsb
        self.MATL_DENS = DgdDsb
        self.MATL_POIS_G = Pgd
        self.MATL_POIS_S = Psb
        self.MATL_THERMAL = TgdTsb
        self.USE_MULTI_ELAST = MultiModulus
        self.LONGTERM_ESEC = CreepEratio
        self.SHRINK_ESEC = ShrinkEratio


        self.J1=bool(Joint[0])
        self.JL1=bool(Joint[1])
        self.JL2=bool(Joint[2])
        self.JL3=bool(Joint[3])
        self.JL4=bool(Joint[4])

        if self.SYMM:
            self.JR1=bool(Joint[1])
            self.JR2=bool(Joint[2])
            self.JR3=bool(Joint[3])
            self.JR4=bool(Joint[4])

            # _I
            self.HR1_I	  =	HL1_I
            self.HR2_I	  =	HL2_I
            self.HR21_I	  =	HL21_I
            self.HR22_I	  =	HL22_I
            self.HR3_I	  =	HL3_I
            self.HR4_I	  =	HL4_I
            self.HR41_I	  =	HL41_I
            self.HR42_I	  =	HL42_I
            self.HR5_I	  =	HL5_I

            self.BR1_I	  =	BL1_I
            self.BR2_I	  =	BL2_I
            self.BR21_I	  =	BL21_I
            self.BR22_I	  =	BL22_I
            self.BR4_I	  =	BL4_I
            self.BR41_I	  =	BL41_I
            self.BR42_I	  =	BL42_I

            # _J
            self.HR1_J	  =	HL1_J
            self.HR2_J	  =	HL2_J
            self.HR21_J	  =	HL21_J
            self.HR22_J	  =	HL22_J
            self.HR3_J	  =	HL3_J
            self.HR4_J	  =	HL4_J
            self.HR41_J	  =	HL41_J
            self.HR42_J	  =	HL42_J
            self.HR5_J	  =	HL5_J

            self.BR1_J	  =	BL1_J
            self.BR2_J	  =	BL2_J
            self.BR21_J	  =	BL21_J
            self.BR22_J	  =	BL22_J
            self.BR4_J	  =	BL4_J
            self.BR41_J	  =	BL41_J
            self.BR42_J	  =	BL42_J
        else:
            self.JR1=bool(Joint[5])
            self.JR2=bool(Joint[6])
            self.JR3=bool(Joint[7])
            self.JR4=bool(Joint[8])

            # _I
            self.HR1_I	  =	HR1_I
            self.HR2_I	  =	HR2_I
            self.HR21_I	  =	HR21_I
            self.HR22_I	  =	HR22_I
            self.HR3_I	  =	HR3_I
            self.HR4_I	  =	HR4_I
            self.HR41_I	  =	HR41_I
            self.HR42_I	  =	HR42_I
            self.HR5_I	  =	HR5_I

            self.BR1_I	  =	BR1_I
            self.BR2_I	  =	BR2_I
            self.BR21_I	  =	BR21_I
            self.BR22_I	  =	BR22_I
            self.BR4_I	  =	BR4_I
            self.BR41_I	  =	BR41_I
            self.BR42_I	  =	BR42_I

            # _J
            self.HR1_J	  =	HR1_J
            self.HR2_J	  =	HR2_J
            self.HR21_J	  =	HR21_J
            self.HR22_J	  =	HR22_J
            self.HR3_J	  =	HR3_J
            self.HR4_J	  =	HR4_J
            self.HR41_J	  =	HR41_J
            self.HR42_J	  =	HR42_J
            self.HR5_J	  =	HR5_J

            self.BR1_J	  =	BR1_J
            self.BR2_J	  =	BR2_J
            self.BR21_J	  =	BR21_J
            self.BR22_J	  =	BR22_J
            self.BR4_J	  =	BR4_J
            self.BR41_J	  =	BR41_J
            self.BR42_J	  =	BR42_J

        # _I
        self.H1_I	      =	H1_I
        self.HL1_I	  =	HL1_I
        self.HL2_I	  =	HL2_I
        self.HL21_I	  =	HL21_I
        self.HL22_I	  =	HL22_I
        self.HL3_I	  =	HL3_I
        self.HL4_I	  =	HL4_I
        self.HL41_I	  =	HL41_I
        self.HL42_I	  =	HL42_I
        self.HL5_I	  =	HL5_I

        self.BL1_I	  =	BL1_I
        self.BL2_I	  =	BL2_I
        self.BL21_I	  =	BL21_I
        self.BL22_I	  =	BL22_I
        self.BL4_I	  =	BL4_I
        self.BL41_I	  =	BL41_I
        self.BL42_I	  =	BL42_I

        # _J
        self.H1_J	      =	H1_J
        self.HL1_J	  =	HL1_J
        self.HL2_J	  =	HL2_J
        self.HL21_J	  =	HL21_J
        self.HL22_J	  =	HL22_J
        self.HL3_J	  =	HL3_J
        self.HL4_J	  =	HL4_J
        self.HL41_J	  =	HL41_J
        self.HL42_J	  =	HL42_J
        self.HL5_J	  =	HL5_J

        self.BL1_J	  =	BL1_J
        self.BL2_J	  =	BL2_J
        self.BL21_J	  =	BL21_J
        self.BL22_J	  =	BL22_J
        self.BL4_J	  =	BL4_J
        self.BL41_J	  =	BL41_J
        self.BL42_J	  =	BL42_J

        self.OFFSET = Offset
        self.USESHEAR = bool(useShear)
        self.USE7DOF = bool(use7Dof)
    
    def __str__(self):
         return f'  >  ID = {self.ID}   |  PSC COMPOSITE I SECTION \nJSON = {self.toJSON()}\n'


    def toJSON(sect):
        js =  {
                "SECTTYPE": sect.TYPE,
                "SECT_NAME": sect.NAME,
                "SECT_BEFORE": {
                    "SHAPE": sect.SHAPE,
                    "TYPE": 12,
                    "SECT_I": {
                        "vSIZE_PSC_A": [sect.H1_I,sect.HL1_I,sect.HL2_I,sect.HL21_I,sect.HL22_I,sect.HL3_I,sect.HL4_I,sect.HL41_I,sect.HL42_I,sect.HL5_I],
                        "vSIZE_PSC_B": [sect.BL1_I,sect.BL2_I,sect.BL21_I,sect.BL22_I,sect.BL4_I,sect.BL41_I,sect.BL42_I],
                        "vSIZE_PSC_C": [sect.HR1_I,sect.HR2_I,sect.HR21_I,sect.HR22_I,sect.HR3_I,sect.HR4_I,sect.HR41_I,sect.HR42_I,sect.HR5_I],
                        "vSIZE_PSC_D": [sect.BR1_I,sect.BR2_I,sect.BR21_I,sect.BR22_I,sect.BR4_I,sect.BR41_I,sect.BR42_I]
                    },
                    "Y_VAR": 1,
                    "Z_VAR": 1,
                    "WARPING_CHK_AUTO_I": True,
                    "WARPING_CHK_AUTO_J": True,
                    "SHEAR_CHK": True,
                    "WARPING_CHK_POS_I": [[0,0,0,0,0,0],[0,0,0,0,0,0]],
                    "WARPING_CHK_POS_J": [[0,0,0,0,0,0],[0,0,0,0,0,0]],
                    "USE_AUTO_SHEAR_CHK_POS": [[True,False,True],[False,False,False]],
                    "USE_WEB_THICK_SHEAR": [[True, True,True],[False,False,False]],
                    "SHEAR_CHK_POS": [[0,0,0],[0,0,0]],
                    "USE_WEB_THICK": [True,False],
                    "WEB_THICK": [0,0],
                    "JOINT": [sect.J1,sect.JL1,sect.JL2,sect.JL3,sect.JL4,sect.JR1,sect.JR2,sect.JR3,sect.JR4],
                    "USE_SYMMETRIC": sect.SYMM,
                    "MATL_ELAST": sect.MATL_ELAST,
                    "MATL_DENS": sect.MATL_DENS,
                    "MATL_POIS_S": sect.MATL_POIS_G,
                    "MATL_POIS_C": sect.MATL_POIS_S,
                    "MATL_THERMAL": sect.MATL_THERMAL,
                    "USE_MULTI_ELAST": sect.USE_MULTI_ELAST,
                    "LONGTERM_ESEC": sect.LONGTERM_ESEC,
                    "SHRINK_ESEC": sect.SHRINK_ESEC,
                },
                "SECT_AFTER": {
                    "SLAB": [sect.BC,sect.TC,sect.HH],
                    "SECT_I":{"BUILT_FLAG":1},
                },
                "COMPOSITE_J": {
                    "vSIZE_PSC_A": [sect.H1_J,sect.HL1_J,sect.HL2_J,sect.HL21_J,sect.HL22_J,sect.HL3_J,sect.HL4_J,sect.HL41_J,sect.HL42_J,sect.HL5_J],
                    "vSIZE_PSC_B": [sect.BL1_J,sect.BL2_J,sect.BL21_J,sect.BL22_J,sect.BL4_J,sect.BL41_J,sect.BL42_J],
                    "vSIZE_PSC_C": [sect.HR1_J,sect.HR2_J,sect.HR21_J,sect.HR22_J,sect.HR3_J,sect.HR4_J,sect.HR41_J,sect.HR42_J,sect.HR5_J],
                    "vSIZE_PSC_D": [sect.BR1_J,sect.BR2_J,sect.BR21_J,sect.BR22_J,sect.BR4_J,sect.BR41_J,sect.BR42_J]
                }
            }
        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js
    
    @staticmethod
    def _objectify(id,name,type,shape,offset,uShear,u7DOF,js):
        vA_I = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_A']
        vB_I = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_B']
        vC_I = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_C']
        vD_I = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_D']

        vA_J = js['COMPOSITE_J']['vSIZE_PSC_A']
        vB_J = js['COMPOSITE_J']['vSIZE_PSC_B']
        vC_J = js['COMPOSITE_J']['vSIZE_PSC_C']
        vD_J = js['COMPOSITE_J']['vSIZE_PSC_D']

        joint = js['SECT_BEFORE']['JOINT']
        slab = js['SECT_AFTER']['SLAB']
        secti = js['SECT_BEFORE']

        try: e1 = js['SECT_BEFORE']['LONGTERM_ESEC'] 
        except: e1 = 0
        try: e2 = js['SECT_BEFORE']['SHRINK_ESEC'] 
        except: e2 = 0



        return _SS_TAP_COMP_PSC_I(name,False,joint,
                            slab[0],slab[1],slab[2],

                            vA_I[0],
                            vA_I[1],vA_I[2],vA_I[3],vA_I[4],vA_I[5],vA_I[6],vA_I[7],vA_I[8],vA_I[9],
                            vB_I[0],vB_I[1],vB_I[2],vB_I[3],vB_I[4],vB_I[5],vB_I[6],
                            vC_I[0],vC_I[1],vC_I[2],vC_I[3],vC_I[4],vC_I[5],vC_I[6],vC_I[7],vC_I[8],
                            vD_I[0],vD_I[1],vD_I[2],vD_I[3],vD_I[4],vD_I[5],vD_I[6],

                            vA_J[0],
                            vA_J[1],vA_J[2],vA_J[3],vA_J[4],vA_J[5],vA_J[6],vA_J[7],vA_J[8],vA_J[9],
                            vB_J[0],vB_J[1],vB_J[2],vB_J[3],vB_J[4],vB_J[5],vB_J[6],
                            vC_J[0],vC_J[1],vC_J[2],vC_J[3],vC_J[4],vC_J[5],vC_J[6],vC_J[7],vC_J[8],
                            vD_J[0],vD_J[1],vD_J[2],vD_J[3],vD_J[4],vD_J[5],vD_J[6],

                            secti['MATL_ELAST'],secti['MATL_DENS'],secti['MATL_POIS_S'],secti['MATL_POIS_C'],secti['MATL_THERMAL'],
                            secti['USE_MULTI_ELAST'],e1,e2,
                            offset,uShear,u7DOF,id)
    
