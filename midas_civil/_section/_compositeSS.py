from ._offsetSS import Offset
from ._offsetSS import _common

class _SS_COMP_PSC_I(_common):

    """ Create Standard USER DEFINED sections"""

    def __init__(self,Name='',Symm = True,Joint=[0,0,0,0,0,0,0,0,0],
                    Bc=0,tc=0,Hh=0,
                    H1=0,
                    HL1=0,HL2=0,HL21=0,HL22=0,HL3=0,HL4=0,HL41=0,HL42=0,HL5=0,
                    BL1=0,BL2=0,BL21=0,BL22=0,BL4=0,BL41=0,BL42=0,

                    HR1=0,HR2=0,HR21=0,HR22=0,HR3=0,HR4=0,HR41=0,HR42=0,HR5=0,
                    BR1=0,BR2=0,BR21=0,BR22=0,BR4=0,BR41=0,BR42=0,

                    EgdEsb =0, DgdDsb=0,Pgd=0,Psb=0,TgdTsb=0,

                    MultiModulus = False,CreepEratio=0,ShrinkEratio=0,

                    Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
        
        self.ID = id
        self.NAME = Name
        self.SHAPE = 'CI'
        self.TYPE = 'COMPOSITE'

        self.SYMM = bool(Symm)

        self.BC =Bc
        self.TC =tc
        self.HH =Hh

        self.MATL_ELAST = EgdEsb
        self.MATL_DENS = DgdDsb
        self.MATL_POIS_S = Pgd
        self.MATL_POIS_C = Psb
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

            self.HR1	  =	HL1
            self.HR2	  =	HL2
            self.HR21	  =	HL21
            self.HR22	  =	HL22
            self.HR3	  =	HL3
            self.HR4	  =	HL4
            self.HR41	  =	HL41
            self.HR42	  =	HL42
            self.HR5	  =	HL5

            self.BR1	  =	BL1
            self.BR2	  =	BL2
            self.BR21	  =	BL21
            self.BR22	  =	BL22
            self.BR4	  =	BL4
            self.BR41	  =	BL41
            self.BR42	  =	BL42
        else:
            self.JR1=bool(Joint[5])
            self.JR2=bool(Joint[6])
            self.JR3=bool(Joint[7])
            self.JR4=bool(Joint[8])

            self.HR1	  =	HR1
            self.HR2	  =	HR2
            self.HR21	  =	HR21
            self.HR22	  =	HR22
            self.HR3	  =	HR3
            self.HR4	  =	HR4
            self.HR41	  =	HR41
            self.HR42	  =	HR42
            self.HR5	  =	HR5

            self.BR1	  =	BR1
            self.BR2	  =	BR2
            self.BR21	  =	BR21
            self.BR22	  =	BR22
            self.BR4	  =	BR4
            self.BR41	  =	BR41
            self.BR42	  =	BR42

        self.OFFSET = Offset
        self.USESHEAR = bool(useShear)
        self.USE7DOF = bool(use7Dof)

        self.H1	  =	H1
        self.HL1	  =	HL1
        self.HL2	  =	HL2
        self.HL21	  =	HL21
        self.HL22	  =	HL22
        self.HL3	  =	HL3
        self.HL4	  =	HL4
        self.HL41	  =	HL41
        self.HL42	  =	HL42
        self.HL5	  =	HL5

        self.BL1	  =	BL1
        self.BL2	  =	BL2
        self.BL21	  =	BL21
        self.BL22	  =	BL22
        self.BL4	  =	BL4
        self.BL41	  =	BL41
        self.BL42	  =	BL42
    
    def __str__(self):
         return f'  >  ID = {self.ID}   |  PSC COMPOSITE I SECTION \nJSON = {self.toJSON()}\n'


    def toJSON(sect):
        js =  {
                "SECTTYPE": sect.TYPE,
                "SECT_NAME": sect.NAME,
                "SECT_BEFORE": {
                    "SHAPE": sect.SHAPE,
                    "SECT_I": {
                        "vSIZE_PSC_A": [sect.H1,sect.HL1,sect.HL2,sect.HL21,sect.HL22,sect.HL3,sect.HL4,sect.HL41,sect.HL42,sect.HL5],
                        "vSIZE_PSC_B": [sect.BL1,sect.BL2,sect.BL21,sect.BL22,sect.BL4,sect.BL41,sect.BL42],
                        "vSIZE_PSC_C": [sect.HR1,sect.HR2,sect.HR21,sect.HR22,sect.HR3,sect.HR4,sect.HR41,sect.HR42,sect.HR5],
                        "vSIZE_PSC_D": [sect.BR1,sect.BR2,sect.BR21,sect.BR22,sect.BR4,sect.BR41,sect.BR42]
                    },
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
                    "MATL_ELAST": sect.MATL_ELAST,
                    "MATL_DENS": sect.MATL_DENS,
                    "MATL_POIS_S": sect.MATL_POIS_S,
                    "MATL_POIS_C": sect.MATL_POIS_C,
                    "MATL_THERMAL": sect.MATL_THERMAL,
                    "USE_MULTI_ELAST": sect.USE_MULTI_ELAST,
                    "LONGTERM_ESEC": sect.LONGTERM_ESEC,
                    "SHRINK_ESEC": sect.SHRINK_ESEC,
                },
                "SECT_AFTER": {
                    "SLAB": [sect.BC,sect.TC,sect.HH]
                }
            }
        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js
    
    @staticmethod
    def _objectify(id,name,type,shape,offset,uShear,u7DOF,js):
        vA = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_A']
        vB = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_B']
        vC = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_C']
        vD = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_D']
        joint = js['SECT_BEFORE']['JOINT']
        slab = js['SECT_AFTER']['SLAB']
        secti = js['SECT_BEFORE']

        try: e1 = js['SECT_BEFORE']['LONGTERM_ESEC'] 
        except: e1 = 0
        try: e2 = js['SECT_BEFORE']['SHRINK_ESEC'] 
        except: e2 = 0


        return _SS_COMP_PSC_I(name,False,joint,
                            slab[0],slab[1],slab[2],
                            vA[0],
                            vA[1],vA[2],vA[3],vA[4],vA[5],vA[6],vA[7],vA[8],vA[9],
                            vB[0],vB[1],vB[2],vB[3],vB[4],vB[5],vB[6],
                            vC[0],vC[1],vC[2],vC[3],vC[4],vC[5],vC[6],vC[7],vC[8],
                            vD[0],vD[1],vD[2],vD[3],vD[4],vD[5],vD[6],
                            secti['MATL_ELAST'],secti['MATL_DENS'],secti['MATL_POIS_S'],secti['MATL_POIS_C'],secti['MATL_THERMAL'],
                            secti['USE_MULTI_ELAST'],e1,e2,
                            offset,uShear,u7DOF,id)
    

class _SS_COMP_STEEL_I_TYPE1(_common):

    """ Create Standard USER DEFINED sections"""

    def __init__(self,Name='',
        Bc=0,tc=0,Hh=0,
        Hw=0,B1=0,tf1=0,tw=0,B2=0,tf2=0,

        EsEc =0, DsDc=0,Ps=0,Pc=0,TsTc=0,
        MultiModulus = False,CreepEratio=0,ShrinkEratio=0,
        Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
                
        self.ID = id
        self.NAME = Name
        self.SHAPE = 'I'
        self.TYPE = 'COMPOSITE'

        self.BC =Bc
        self.TC =tc
        self.HH =Hh

        self.HW	 =	Hw
        self.B1	 =	B1
        self.TF1 =	tf1
        self.TW	 =	tw
        self.B2	 =	B2    
        self.TF2  =	tf2    

        self.MATL_ELAST = EsEc
        self.MATL_DENS = DsDc
        self.MATL_POIS_S = Ps
        self.MATL_POIS_C = Pc
        self.MATL_THERMAL = TsTc
        self.USE_MULTI_ELAST = MultiModulus
        self.LONGTERM_ESEC = CreepEratio
        self.SHRINK_ESEC = ShrinkEratio

        self.OFFSET = Offset
        self.USESHEAR = bool(useShear)
        self.USE7DOF = bool(use7Dof)  
    
    def __str__(self):
         return f'  >  ID = {self.ID}   |  STEEL COMPOSITE I SECTION \nJSON = {self.toJSON()}\n'


    def toJSON(sect):
        js =  {
                "SECTTYPE": sect.TYPE,
                "SECT_NAME": sect.NAME,
                "SECT_BEFORE": {
                    "SHAPE": sect.SHAPE,
                    "SECT_I": {
                        "vSIZE": [sect.HW,sect.TW,sect.B1,sect.TF1,sect.B2,sect.TF2],
                    },
 
                    "MATL_ELAST": sect.MATL_ELAST,
                    "MATL_DENS": sect.MATL_DENS,
                    "MATL_POIS_S": sect.MATL_POIS_S,
                    "MATL_POIS_C": sect.MATL_POIS_C,
                    "MATL_THERMAL": sect.MATL_THERMAL,
                    "USE_MULTI_ELAST": sect.USE_MULTI_ELAST,
                    "LONGTERM_ESEC": sect.LONGTERM_ESEC,
                    "SHRINK_ESEC": sect.SHRINK_ESEC,
                },
                "SECT_AFTER": {
                    "SLAB": [sect.BC,sect.TC,sect.HH]
                }
            }
        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js
    
    @staticmethod
    def _objectify(id,name,type,shape,offset,uShear,u7DOF,js):
        vS = js['SECT_BEFORE']['SECT_I']['vSIZE']
        slab = js['SECT_AFTER']['SLAB']
        secti = js['SECT_BEFORE']

        try: e1 = js['SECT_BEFORE']['LONGTERM_ESEC'] 
        except: e1 = 0
        try: e2 = js['SECT_BEFORE']['SHRINK_ESEC'] 
        except: e2 = 0


        return _SS_COMP_STEEL_I_TYPE1(name,
                            slab[0],slab[1],slab[2],
                            vS[0],vS[2],vS[3],vS[1],vS[4],vS[5],
                            secti['MATL_ELAST'],secti['MATL_DENS'],secti['MATL_POIS_S'],secti['MATL_POIS_C'],secti['MATL_THERMAL'],
                            secti['USE_MULTI_ELAST'],e1,e2,
                            offset,uShear,u7DOF,id)