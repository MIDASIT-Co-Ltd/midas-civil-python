from ._offsetSS import Offset
from ._offsetSS import _common


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



class _SS_COMP_STEEL_TUB_TYPE1(_common):

    """ Create Standard USER DEFINED sections"""

    def __init__(self,Name='',
        Bc=0,tc=0,Hh=0,
        Hw=0,B1=0,Bf1=0,tf1=0,Bf3=0,
        tw=0,B2=0,Bf2=0,tf2=0,tfp=0,

        EsEc =0, DsDc=0,Ps=0,Pc=0,TsTc=0,
        MultiModulus = False,CreepEratio=0,ShrinkEratio=0,
        Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
                
        self.ID = id
        self.NAME = Name
        self.SHAPE = 'Tub'
        self.TYPE = 'COMPOSITE'

        self.BC =Bc
        self.TC =tc
        self.HH =Hh

        self.HW	 =	Hw
        self.B1	 =	B1
        self.BF1 =	Bf1
        self.TF1 =	tf1
        self.BF3 =	Bf3


        self.TW	 =	tw
        self.B2	 =	B2
        self.BF2 =	Bf2
        self.TF2  =	tf2    
        self.TFP  =	tfp   

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
                        "vSIZE": [sect.HW,sect.TW,sect.B1,sect.BF1,sect.TF1,sect.B2,sect.BF2,sect.TF2,sect.BF3,sect.TFP],
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


        return _SS_COMP_STEEL_TUB_TYPE1(name,
                            slab[0],slab[1],slab[2],
                            vS[0],vS[2],vS[3],vS[4],vS[8],vS[1],vS[5],vS[6],vS[7],vS[9],
                            secti['MATL_ELAST'],secti['MATL_DENS'],secti['MATL_POIS_S'],secti['MATL_POIS_C'],secti['MATL_THERMAL'],
                            secti['USE_MULTI_ELAST'],e1,e2,
                            offset,uShear,u7DOF,id)

    def _centerLine(shape,*args):
        BC,TC,HH = shape.BC,shape.TC,shape.HH
        HW,B1,BF1,TF1,BF3 = shape.HW,shape.B1,shape.BF1,shape.TF1,shape.BF3
        TW,B2,BF2,TF2,TFP = shape.TW,shape.B2,shape.BF2,shape.TF2,shape.TFP


        sect_cg_LT = [-0.5*BC,TF2+HW+TF1+TC+HH]
        sect_cg_RB = [0.5*BC,0]
        sect_cg_CC = [0,(TF2+HW+TF1)/2]

        cp1=(0,0.5*TF2)
        cp2=(-0.5*B2,0.5*TF2)
        cp3=(-0.5*B2-BF2,0.5*TF2)
        cp4=(-0.5*B1-BF1+BF3,TF2+HW+0.5*TF1)
        cp5=(-0.5*B1,TF2+HW+0.5*TF1)
        cp6=(-0.5*B1-BF1,TF2+HW+0.5*TF1)

        sect_shape = [cp1,cp2,cp4,cp5]
        sect_lin_con = [[1,2],[3,2],[4,3]]
        sect_thk = [TF2,TW,TF1]
        sect_thk_off = [0,0,0]

        if BF2!=0:
            sect_shape.append(cp3)
            sect_lin_con.append([2,5])
            sect_thk.append(TF2)
            sect_thk_off.append(0)
        if BF3!=0:
            sect_shape.append(cp6)
            sect_thk.append(TF1)
            sect_thk_off.append(0)
            if BF2==0:
                sect_lin_con.append([3,5])
            else:
                sect_lin_con.append([3,6])
    
        
        n_points = len(sect_shape)

        final_lin_con = sect_lin_con
        final_shape = sect_shape
        final_thk_off = sect_thk_off
        final_thk = sect_thk

        for i in range(n_points):
            final_shape.append((-sect_shape[i][0],sect_shape[i][1]))

        for q in range(len(sect_lin_con)):    # SYMMETRY
            final_thk.append(final_thk[q])
            final_thk_off.append(final_thk_off[q])
            final_lin_con.append([sect_lin_con[q][1]+n_points,sect_lin_con[q][0]+n_points])


        sect_cg = (sect_cg_LT,sect_cg_CC,sect_cg_RB)

        return final_shape, final_thk ,final_thk_off, sect_cg , final_lin_con
