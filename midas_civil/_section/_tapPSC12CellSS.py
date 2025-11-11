from ._offsetSS import Offset
from ._offsetSS import _common

import numpy as np
from math import hypot
class _SS_TAP_PSC_12CELL(_common):
    def __init__(self,Name='',Shape='1CEL',Joint=[0,0,0,0,0,0,0,0],
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
        self.SHAPE = Shape
        self.TYPE = 'TAPERED'

        # print("***********")
        # print(Name,Shape,Joint)

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
        return _SS_TAP_PSC_12CELL(name,shape,joint,
                            *vA_I,*vB_I,*vC_I,*vD_I,
                            *vA_J,*vB_J,*vC_J,*vD_J,
                            offset,uShear,u7DOF,id)
    
    def _centerLine(shape,end,*args):
        if shape.SHAPE in ['1CEL','2CEL'] :
            if end:
                HO1,HO2,HO21,HO22,HO3,HO31 = shape.HO1_J,shape.HO2_J,shape.HO21_J,shape.HO22_J,shape.HO3_J,shape.HO31_J
                BO1,BO11,BO12,BO2,BO21,BO3 = shape.BO1_J,shape.BO11_J,shape.BO12_J,shape.BO2_J,shape.BO21_J,shape.BO3_J

                HI1,HI2,HI21,HI22,HI3,HI31,HI4,HI41,HI42,HI5 = shape.HI1_J,shape.HI2_J,shape.HI21_J,shape.HI22_J,shape.HI3_J,shape.HI31_J,shape.HI4_J,shape.HI41_J,shape.HI42_J,shape.HI5_J
                BI1,BI11,BI12,BI21,BI3,BI31,BI32,BI4 = shape.BI1_J,shape.BI11_J,shape.BI12_J,shape.BI21_J,shape.BI3_J,shape.BI31_J,shape.BI32_J,shape.BI4_J
                
            
            else:
                HO1,HO2,HO21,HO22,HO3,HO31 = shape.HO1_I,shape.HO2_I,shape.HO21_I,shape.HO22_I,shape.HO3_I,shape.HO31_I
                BO1,BO11,BO12,BO2,BO21,BO3 = shape.BO1_I,shape.BO11_I,shape.BO12_I,shape.BO2_I,shape.BO21_I,shape.BO3_I

                HI1,HI2,HI21,HI22,HI3,HI31,HI4,HI41,HI42,HI5 = shape.HI1_I,shape.HI2_I,shape.HI21_I,shape.HI22_I,shape.HI3_I,shape.HI31_I,shape.HI4_I,shape.HI41_I,shape.HI42_I,shape.HI5_I
                BI1,BI11,BI12,BI21,BI3,BI31,BI32,BI4 = shape.BI1_I,shape.BI11_I,shape.BI12_I,shape.BI21_I,shape.BI3_I,shape.BI31_I,shape.BI32_I,shape.BI4_I

                
                
            JO1,JO2,JO3,JI1,JI2,JI3,JI4,JI5 = shape.JO1,shape.JO2,shape.JO3,shape.JI1,shape.JI2,shape.JI3,shape.JI4,shape.JI5

            sect_cg_LT = [-(BO1+BO2+BO3),0]
            sect_cg_RB = [(BO1+BO2+BO3),-(HO1+HO2+HO3)]
            sect_cg_CC = [0,-(HO1+HO2+HO3)/2]




            def perpendicular_point(pt1,pt2,point, l=0):
                """Function to get orthogonal point on line (x1,y1)-(x2,y2) from point (x3,y3). Enter l=0 for point 3 in between 1 & 2.  Enter l=1 for other scenario."""
                x1,y1 = pt1
                x2,y2 = pt2
                x3,y3 = point

                if x2 != x1:
                    m = (y2 - y1) / (x2 - x1)
                    c = y1 - m * x1
                    x_perp = (x3 + m * (y3 - c)) / (1 + m**2)
                    y_perp = m * x_perp + c
                else:
                    x_perp, y_perp = x1, y3
                
                thk = ((x3 - x_perp)**2 + (y3 - y_perp)**2)**0.5
                return (x_perp, y_perp),thk
            
            def distance_point(pt1,pt2):
                x1,y1 = pt1
                x2,y2 = pt2

                return hypot((x1-x2),(y1-y2))


            HTI = HI1+HI2+HI3+HI4+HI5
            HTO = HO1+HO2+HO3
            slope = (HTI-HTO)/(BO1+BO2+BO3)


            pt1 = (0,0)
            pt2 = (0,-HI1)
            pt5 = (-BI1,-HI1-HI2)
            pt7 = (-BI3,-HI1-HI2-HI3)
            pt10 = (0,-HI1-HI2-HI3-HI4)
            pt11 = (0,-HTI)

            pt12 = (-BO3,-HTI)
            pt14 = (-BO3-BO2,(-HTI+HTO)-HO1-HO2)
            pt17 = (-BO3-BO2-BO1,(-HTI+HTO)-HO1)
            pt18 = (-BO3-BO2-BO1,(-HTI+HTO))

            pt3 = (-BI11,-HI1-HI21)
            pt4 = (-BI12,-HI1-HI22)

            pt6 = (-BI21,-HI1-HI2-HI31)

            pt8 = (-BI32,-HI1-HI2-HI3-HI4+HI42)
            pt9 = (-BI31,-HI1-HI2-HI3-HI4+HI41)

            pt13 = (-BO3-BO21,-HO1-HO2-HO3+HO31)

            pt15 = (-BO3-BO2-BO1+BO12,(-HTI+HTO)-HO1-HO22)
            pt16 = (-BO3-BO2-BO1+BO11,(-HTI+HTO)-HO1-HO21)


            pt016 = (-BO3-BO2-BO1+BO11,slope*(-BO3-BO2-BO1+BO11))
            pt015 = (-BO3-BO2-BO1+BO12,slope*(-BO3-BO2-BO1+BO12))
            pt014 = (-BO3-BO2,slope*(-BO3-BO2))
            pt05 = (-BI1,slope*(-BI1))
            pt04 = (-BI12,slope*(-BI12))
            pt03 = (-BI11,slope*(-BI11))
            # ---------------------- OUTER POINTS  ---------------------------

            temppt = [pt016,pt015,pt014,pt05,pt04,pt03]
            points = []

            #-------
            points.append(pt1)
            points.append(pt2)
            if JI1 : points.append(pt3)
            if JI2 : points.append(pt4)
            points.append(pt5)
            if JI3 : points.append(pt6)
            points.append(pt7)
            if JI4 : points.append(pt8)
            if JI5 : points.append(pt9)
            points.append(pt10)
            points.append(pt11)
            points.append(pt12)
            if JO3 : points.append(pt13)
            points.append(pt14)
            if JO2 : points.append(pt15)
            if JO1 : points.append(pt16)
            points.append(pt17)
            points.append(pt18)
            points.append(pt1)

            x_values, y_values = zip(*points)

            # -------------------   CENTER LINE POINTS ------------------

            cp1 = (0,-HI1/2)


            # cp2 = (-BI11,(-HI1-HI21)/2) #JI1
            cp2 = np.add(pt3,pt03)/2

            # cp3 = (-BI12,(-HI1-HI22)/2) #JI2
            cp3 = np.add(pt4,pt04)/2
            # cp4 = (-BI1,(-HI1-HI2)/2)
            cp4 = np.add(pt5,pt05)/2

            # cp5 = (-BO3-BO2-BO1,-HO1/2)
            cp5 = np.add(pt17,pt18)/2
            # cp6 = (-BO3-BO2-BO1+BO11,(-HO1-HO21)/2) #JO1
            cp6 = np.add(pt16,pt016)/2
            # cp7 = (-BO3-BO2-BO1+BO12,(-HO1-HO22)/2) #JO2
            cp7 = np.add(pt15,pt015)/2
            # cp8 = (-BO3-BO2,(-HO1-HO2)/2)
            cp8 = np.add(pt14,pt014)/2

            cp9 = np.add(cp8,cp4)/2

            cp10 = np.add(pt5,pt14)/2

            cp17 = np.add(pt10,pt11)/2
            cp16 = (-BI31,(-HI1-HI2-HI3-HI4+HI41-HTI)/2) #JI5
            cp15 = (-BI32,(-HI1-HI2-HI3-HI4+HI42-HTI)/2) #JI4
            cp14 = (-BI3,(-HI1-HI2-HI3-HTI)/2)
            cp13 = np.add(pt7,pt12)/2


            tpt,TJI3 = perpendicular_point(pt13,pt14,pt6)
            cp11 = np.add(tpt,pt6)/2  #JI3


            tpt,TJO3 = perpendicular_point(pt7,pt6,pt13)
            cp12 = np.add(tpt,pt13)/2 #JO3

            # if cp12[1] < cp13[1] : 
            #     print("JO3 invalid")


            #----------------------------- THICKNESS COMPUTATION --------------

            THI1 = HI1
            TJI1 = distance_point(pt3,pt03)
            TJI2 = distance_point(pt4,pt04)
            THI2 = distance_point(pt5,pt05)
            THO2 = distance_point(pt14,pt014)
            THO1 = distance_point(pt17,pt18)
            THI3 = (HI4+HI5)
            THI5 = HI5
            TJO1 = distance_point(pt16,pt016)
            TJO2 = distance_point(pt15,pt015)
            TJI4 = (HI5+HI42)
            TJI5 = (HI5+HI41)


            TX_INT_FLANGE = (HO1+HO2+HI1+HI2)/3
            tpt,THIO2 = perpendicular_point(pt13,pt14,pt5)
            TY_INT_FLANGE = THIO2

            TX_BOT_JUNC = hypot(*np.subtract(pt7,pt12))

            tpt,TY_BOT_JUNC = perpendicular_point(pt13,pt14,pt7)
            # TY_BOT_JUNC = (TY_BOT_JUNC+hypot(*np.subtract(pt7,pt12)))/2



            top_flange_point =[]
            top_flange_line = []
            top_flange_thk = []
            q=1
            top_flange_point.append(cp1)
            if JI1 : 
                top_flange_point.append(cp2)
                top_flange_line.append([q,q+1])
                top_flange_thk.append([THI1,TJI1])
                q+=1
            if JI2 : 
                top_flange_point.append(cp3)
                top_flange_line.append([q,q+1])
                q+=1
                if JI1:
                    top_flange_thk.append([TJI1,TJI2])
                else :
                    top_flange_thk.append([THI1,TJI2])
            top_flange_point.append(cp4)
            top_flange_line.append([q,q+1])
            q+=1

            if JI2:
                top_flange_thk.append([TJI2,THI2])
            elif JI1:
                top_flange_thk.append([TJI1,THI2])
            else :
                top_flange_thk.append([THI1,THI2])


            top_flange_line.append([q,q+1]) # TO CONNECT WITH WEB
            q+=1
            top_flange_thk.append([THI2,TX_INT_FLANGE]) 


            # print(top_flange_thk)

            web_point =[]
            web_line =[]
            web_thk = []

            web_point.append(cp9)
            web_point.append(cp10)
            web_line.append([q,q+1])
            q+=1
            web_thk.append([TY_INT_FLANGE,THIO2])
            if JI3 : 
                web_point.append(cp11)
                web_line.append([q,q+1])
                q+=1
                web_thk.append([THIO2,TJI3])
            if JO3 and cp12[1] < cp13[1]: 
                web_point.append(cp12)
                web_line.append([q,q+1])
                if JI3 : 
                    web_thk.append([TJI3,TJO3])
                else:
                    web_thk.append([THIO2,TJO3])
                q+=1

            web_point.append(cp13)
            web_line.append([q,q+1])
            if JO3:
                web_thk.append([TJO3,TY_BOT_JUNC])
            elif JI3:
                web_thk.append([TJI3,TY_BOT_JUNC])
            else:
                web_thk.append([THIO2,TY_BOT_JUNC])
            q+=1


            bottom_flange_point =[]
            bottom_flange_line =[]
            bottom_flange_thk = []

            bottom_flange_line.append([q,q+1]) # TO CONNECT WITH WEB
            bottom_flange_thk.append([TX_BOT_JUNC,THI3])
            q+=1
            bottom_flange_point.append(cp14)
            if JI4 : 
                bottom_flange_point.append(cp15)
                bottom_flange_line.append([q,q+1])
                q+=1
                bottom_flange_thk.append([THI3,TJI4])
            if JI5 : 
                bottom_flange_point.append(cp16)
                bottom_flange_line.append([q,q+1])
                q+=1
                if JI4:
                    bottom_flange_thk.append([TJI4,TJI5])
                else:
                    bottom_flange_thk.append([THI3,TJI5])
            bottom_flange_point.append(cp17)
            bottom_flange_line.append([q,q+1])
            n_cp17 = q+1
            if JI5:
                bottom_flange_thk.append([TJI5,THI5])
            elif JI4:
                bottom_flange_thk.append([TJI4,THI5])
            else:
                bottom_flange_thk.append([THI3,THI5])
            q+=1 


            top_cantelever_point =[]
            top_cantelever_line =[]
            top_cantelever_thk =[]

            top_cantelever_line.append([len(top_flange_point)+1,q+1]) # TO CONNECT WITH WEB
            top_cantelever_thk.append([TX_INT_FLANGE,THO2])
            q+=1
            top_cantelever_point.append(cp8)
            if JO2 : 
                top_cantelever_point.append(cp7)
                top_cantelever_line.append([q,q+1])
                q+=1
                top_cantelever_thk.append([THO2,TJO2])
            if JO1 : 
                top_cantelever_point.append(cp6)
                top_cantelever_line.append([q,q+1])
                q+=1
                if JO2:
                    top_cantelever_thk.append([TJO2,TJO1])
                else:
                    top_cantelever_thk.append([THO2,TJO1])
            top_cantelever_point.append(cp5)
            top_cantelever_line.append([q,q+1])
            if JO1:
                top_cantelever_thk.append([TJO1,THO1])
            elif JO2:
                top_cantelever_thk.append([TJO2,THO1])
            else:
                top_cantelever_thk.append([THO2,THO1])


            final_points = top_flange_point+web_point+bottom_flange_point+top_cantelever_point
            final_line = top_flange_line+web_line+bottom_flange_line+top_cantelever_line
            final_thk = top_flange_thk+web_thk+bottom_flange_thk+top_cantelever_thk

            n_points = len(final_points)


            sect_shape = final_points
            for i in range(n_points):
                sect_shape.append((-final_points[i][0],final_points[i][1]))


            sect_lin_con = final_line
            sect_thk = final_thk
            

            for q in range(len(final_line)):
                sect_thk.append([final_thk[q][1],final_thk[q][0]])
                sect_lin_con.append([final_line[q][1]+n_points,final_line[q][0]+n_points])


            if shape.SHAPE == '2CEL':
                sect_lin_con.append([1,n_cp17])
                sect_thk.append([2*BI4,2*BI4])

            sect_thk_off = [0 for _ in sect_thk]
            
        

        sect_cg = (sect_cg_LT,sect_cg_CC,sect_cg_RB)

        return sect_shape, sect_thk ,sect_thk_off, sect_cg , sect_lin_con
    







