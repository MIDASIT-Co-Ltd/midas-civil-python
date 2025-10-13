from ._offsetSS import Offset
from ._offsetSS import _common
import math



class _SS_PSC_12CELL(_common):
    def __init__(self,Name='',Shape='1CEL',Joint=[0,0,0,0,0,0,0,0],
                    HO1=0,HO2=0,HO21=0,HO22=0,HO3=0,HO31=0,
                    BO1=0,BO11=0,BO12=0,BO2=0,BO21=0,BO3=0,
                    HI1=0,HI2=0,HI21=0,HI22=0,HI3=0,HI31=0,HI4=0,HI41=0,HI42=0,HI5=0,
                    BI1=0,BI11=0,BI12=0,BI21=0,BI3=0,BI31=0,BI32=0,BI4=0,
                    Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
                
        self.ID = id
        self.NAME = Name
        self.SHAPE = Shape
        self.TYPE = 'PSC'

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

        self.HO1 = HO1
        self.HO2 = HO2
        self.HO21 = HO21
        self.HO22= HO22
        self.HO3 = HO3
        self.HO31 = HO31

        self.BO1 = BO1
        self.BO11 = BO11
        self.BO12 = BO12
        self.BO2 = BO2
        self.BO21 = BO21
        self.BO3 = BO3

        self.HI1 = HI1
        self.HI2 = HI2
        self.HI21 = HI21
        self.HI22 = HI22
        self.HI3 = HI3
        self.HI31 = HI31
        self.HI4 = HI4
        self.HI41 = HI41
        self.HI42 = HI42
        self.HI5 = HI5

        self.BI1 = BI1
        self.BI11 = BI11
        self.BI12 = BI12
        self.BI21 = BI21
        self.BI3 = BI3
        self.BI31 = BI31
        self.BI32 = BI32
        self.BI4 = BI4

    
    def __str__(self):
         return f'  >  ID = {self.ID}   |  PSC 1-2 CELL SECTION \nJSON = {self.toJSON()}\n'


    def toJSON(sect):
        js =  {
                "SECTTYPE": "PSC",
                "SECT_NAME": sect.NAME,
                "SECT_BEFORE": {
                    "SHAPE": sect.SHAPE,
                    "SECT_I": {
                        "vSIZE_PSC_A": [sect.HO1,sect.HO2,sect.HO21,sect.HO22,sect.HO3,sect.HO31],
                        "vSIZE_PSC_B": [sect.BO1,sect.BO11,sect.BO12,sect.BO2,sect.BO21,sect.BO3,],
                        "vSIZE_PSC_C": [sect.HI1,sect.HI2,sect.HI21,sect.HI22,sect.HI3,sect.HI31,sect.HI4,sect.HI41,sect.HI42,sect.HI5],
                        "vSIZE_PSC_D": [sect.BI1,sect.BI11,sect.BI12,sect.BI21,sect.BI3,sect.BI31,sect.BI32,sect.BI4]
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
        vA = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_A']
        vB = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_B']
        vC = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_C']
        vD = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_D']
        joint = js['SECT_BEFORE']['JOINT']
        return _SS_PSC_12CELL(name,shape,joint,
                            vA[0],vA[1],vA[2],vA[3],vA[4],vA[5],
                            vB[0],vB[1],vB[2],vB[3],vB[4],vB[5],
                            vC[0],vC[1],vC[2],vC[3],vC[4],vC[5],vC[6],vC[7],vC[8],vC[9],
                            vD[0],vD[1],vD[2],vD[3],vD[4],vD[5],vD[6],vD[7],
                            offset,uShear,u7DOF,id)
    
    def _centerLine(shape,*args):
        if shape.SHAPE == '1CEL':
            BO1 = shape.BO1
            BO2 = shape.BO2
            BO3 = shape.BO3
            HO1 = shape.HO1
            HO2 = shape.HO2
            HO3 = shape.HO3
            HI1 = shape.HI1
            HI5 = shape.HI5
            BI3 = shape.BI3

            sect_lin_con = [[1,2],[2,3],[3,4],[2,5],[3,6],[5,6]]

            sect_cg_LT = [0,0]
            sect_cg_RB = [2*(BO1+BO2+BO3),-(HO1+HO2+HO3)]
            sect_cg_CC = [(BO1+BO2+BO3),-(HO1+HO2+HO3)/2]

            sect_shape = [[0,0],[BO1,0],[BO1+2*(BO2+BO3),0],[2*(BO1+BO2+BO3),0],[BO1+BO2,-HO1-HO3-HO2],[BO1+BO2+2*BO3,-HO1-HO3-HO2]]
            sect_thk = [HO1,HI1,HO1,BO3-BI3,BO3-BI3,HI5]
            sect_thk_off = [-HO1/2,-HI1/2,-HO1/2,(BO3-BI3)/2,-(BO3-BI3)/2,HI5/2]       



        sect_cg = (sect_cg_LT,sect_cg_CC,sect_cg_RB)

        return sect_shape, sect_thk ,sect_thk_off, sect_cg , sect_lin_con

    








class _SS_PSC_I(_common):
    def __init__(self,Name='',Symm = True,Joint=[0,0,0,0,0,0,0,0,0],
                            H1=0,
                            HL1=0,HL2=0,HL21=0,HL22=0,HL3=0,HL4=0,HL41=0,HL42=0,HL5=0,
                            BL1=0,BL2=0,BL21=0,BL22=0,BL4=0,BL41=0,BL42=0,

                            HR1=0,HR2=0,HR21=0,HR22=0,HR3=0,HR4=0,HR41=0,HR42=0,HR5=0,
                            BR1=0,BR2=0,BR21=0,BR22=0,BR4=0,BR41=0,BR42=0,

                            Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
                
        self.ID = id
        self.NAME = Name
        self.SHAPE = 'PSCI'
        self.TYPE = 'PSC'

        self.SYMM = bool(Symm)

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
         return f'  >  ID = {self.ID}   |  PSC I SECTION \nJSON = {self.toJSON()}\n'


    def toJSON(sect):
        js =  {
                "SECTTYPE": "PSC",
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
                    "USE_SYMMETRIC" : sect.SYMM,
                    "JOINT": [sect.J1,sect.JL1,sect.JL2,sect.JL3,sect.JL4,sect.JR1,sect.JR2,sect.JR3,sect.JR4]
                }
            }
        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js
    

    @staticmethod
    def _objectify(id,name,type,shape,offset,uShear,u7DOF,js):
        symm = js['SECT_BEFORE']['USE_SYMMETRIC']
        vA = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_A']
        vB = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_B']
        vC = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_C']
        vD = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_D']
        joint = js['SECT_BEFORE']['JOINT']
        return _SS_PSC_I(name,symm,joint,
                            vA[0],
                            vA[1],vA[2],vA[3],vA[4],vA[5],vA[6],vA[7],vA[8],vA[9],
                            vB[0],vB[1],vB[2],vB[3],vB[4],vB[5],vB[6],
                            vC[0],vC[1],vC[2],vC[3],vC[4],vC[5],vC[6],vC[7],vC[8],
                            vD[0],vD[1],vD[2],vD[3],vD[4],vD[5],vD[6],
                            offset,uShear,u7DOF,id)
    











import numpy as np
def _poly_dir(poly,rot='CCW'):
    outer_cg = np.mean(poly,axis=0)
    outer_t = np.subtract(poly,outer_cg)
    dir = 0
    for i in range(len(poly)-1):
        dir+=outer_t[i][0]*outer_t[i+1][1]-outer_t[i][1]*outer_t[i+1][0]
    if dir < 0:
        poly.reverse()
    
    if rot == 'CW':
        poly.reverse()

    return poly






class _SS_PSC_Value(_common):
    def __init__(self,Name:str,
                    OuterPolygon:list,InnerPolygon:list=[],
                    Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
        
        '''
            Outer Polygon -> List of points ; Last input is different from first
                [(0,0),(1,0),(1,1),(0,1)]
            Inner Polygon -> List of points ; Last input is different from first
                Only one inner polygon
        '''
        
        self.ID = id
        self.NAME = Name
        self.SHAPE = 'VALUE'
        self.TYPE = 'PSC'

        self.OFFSET = Offset
        self.USESHEAR = bool(useShear)
        self.USE7DOF = bool(use7Dof)

        self.OUTER_POLYGON = _poly_dir(OuterPolygon)
        self.INNER_POLYGON = []
        self.N_INNER_POLYGON = 0

        temp_arr = [] 

        # Finding no. of internal polygons
        if InnerPolygon != []:
            if not isinstance(InnerPolygon[0][0],(int,float)):
                self.N_INNER_POLYGON = len(InnerPolygon)
                temp_arr = InnerPolygon 
                
            else:
                temp_arr.append(InnerPolygon) #Convert to list
                self.N_INNER_POLYGON = 1

        for i in range(len(temp_arr)):
            self.INNER_POLYGON.append(_poly_dir(temp_arr[i],'CW'))


    def __str__(self):
         return f'  >  ID = {self.ID}   |  PSC VALUE SECTION \nJSON = {self.toJSON()}\n'


    def toJSON(sect):
        js =  {
                    "SECTTYPE": "PSC",
                    "SECT_NAME": sect.NAME,
                    "CALC_OPT": True,
                    "SECT_BEFORE": {
                        "SHAPE": "VALU",
                        "SECT_I": {
                            "SECT_NAME": "",
                            "vSIZE": [0.1, 0.1, 0.1, 0.1],
                            "OUTER_POLYGON": [
                                {
                                    "VERTEX": [
                                        {"X": 5, "Y": 5},
                                        {"X": -5, "Y": 5}
                                    ]
                                }
                            ]
                        },
                        "SHEAR_CHK": True,
                        "SHEAR_CHK_POS": [[0.1, 0, 0.1], [0, 0, 0]],
                        "USE_AUTO_QY": [[True, True, True], [False, False, False]],
                        "WEB_THICK": [0, 0],
                        "USE_WEB_THICK_SHEAR": [[True, True, True], [False, False, False]]
                    }
                }
        
        v_list = []
        for i in sect.OUTER_POLYGON:
            v_list.append({"X":i[0],"Y":i[1]})
        js["SECT_BEFORE"]["SECT_I"]["OUTER_POLYGON"][0]["VERTEX"] =v_list

        

        if sect.N_INNER_POLYGON > 0 :

            js["SECT_BEFORE"]["SECT_I"]["INNER_POLYGON"]= []

            mult_ver = []
            for n in range(sect.N_INNER_POLYGON):
                vi_list = []

                js["SECT_BEFORE"]["SECT_I"]["INNER_POLYGON"]= [
                    {
                        "VERTEX": []
                    }
                ]
                for i in sect.INNER_POLYGON[n]:
                    vi_list.append({"X":i[0],"Y":i[1]})

                ver_json = {"VERTEX": vi_list}
                mult_ver.append(ver_json)

            js["SECT_BEFORE"]["SECT_I"]["INNER_POLYGON"] = mult_ver

        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js
    

    @staticmethod
    def _objectify(id,name,type,shape,offset,uShear,u7DOF,js):

        outer_pt = []
        for pt in js["SECT_BEFORE"]["SECT_I"]["OUTER_POLYGON"][0]["VERTEX"]:
            outer_pt.append((pt['X'],pt['Y']))

        inner_pt = []
        if 'INNER_POLYGON' in js["SECT_BEFORE"]["SECT_I"]:
            innerJSON = js["SECT_BEFORE"]["SECT_I"]['INNER_POLYGON']
            for n_holes in innerJSON:
                h_pt = []
                for pt in n_holes['VERTEX']:
                    h_pt.append([pt['X'],pt['Y']])
                inner_pt.append(h_pt)

        return _SS_PSC_Value(name,outer_pt,inner_pt,offset,uShear,u7DOF,id)