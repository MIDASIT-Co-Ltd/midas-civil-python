from ._offsetSS import Offset
from ._offsetSS import _common
from math import hypot



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
        if shape.SHAPE in ['1CEL','2CEL'] :
            HO1,HO2,HO21,HO22,HO3,HO31 = shape.HO1,shape.HO2,shape.HO21,shape.HO22,shape.HO3,shape.HO31
            BO1,BO11,BO12,BO2,BO21,BO3 = shape.BO1,shape.BO11,shape.BO12,shape.BO2,shape.BO21,shape.BO3

            HI1,HI2,HI21,HI22,HI3,HI31,HI4,HI41,HI42,HI5 = shape.HI1,shape.HI2,shape.HI21,shape.HI22,shape.HI3,shape.HI31,shape.HI4,shape.HI41,shape.HI42,shape.HI5
            BI1,BI11,BI12,BI21,BI3,BI31,BI32,BI4 = shape.BI1,shape.BI11,shape.BI12,shape.BI21,shape.BI3,shape.BI31,shape.BI32,shape.BI4

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