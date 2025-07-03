from ._mapi import *



def _SectionADD(self):
    # Commom HERE ---------------------------------------------
    id = int(self.ID)
    if Section.ids == []: 
        count = 1
    else:
        count = max(Section.ids)+1

    if id==0 :
        self.ID = count
        Section.sect.append(self)
        Section.ids.append(int(self.ID))
    elif id in Section.ids:
        self.ID=int(id)
        print(f'⚠️  Section with ID {id} already exist! It will be replaced.')
        index=Section.ids.index(id)
        Section.sect[index]=self
    else:
        self.ID=id        
        Section.sect.append(self)
        Section.ids.append(int(self.ID))
    # Common END -------------------------------------------------------


def _updateSect(self):
    js2s = {'Assign':{self.ID : _Obj2JS(self)}}
    MidasAPI('PUT','/db/sect',js2s)
    return js2s


def _Obj2JS(sect):

    js={}

    if sect.TYPE == 'DBUSER':
        if sect.DATATYPE == 2:
            #--- DB SECTION  ---------------------------------------
            js =  {
                "SECTTYPE": "DBUSER",
                "SECT_NAME": sect.NAME,
                "SECT_BEFORE": {
                    "SHAPE": sect.SHAPE,
                    "DATATYPE": sect.DATATYPE,
                    "SECT_I": {
                        "vSIZE": sect.PARAMS
                    }
                }
            }
        #--- PSC 1-2 Cell ---------------------------------------
    elif sect.TYPE == 'PSC':
        if sect.SHAPE in ['1CEL','2CEL']:
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

        elif sect.SHAPE in ['PSCI']:
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

    elif sect.TYPE == 'COMPOSITE':
        if sect.SHAPE in ['CI']:
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
        elif sect.SHAPE in ['I']:
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




    #---  COMMON FOR ALL SECTIONS ---------------------------------------  
    js['SECT_BEFORE'].update(sect.OFFSET.JS)
    js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
    js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
    return js



def _JS2Obj(id,js):
    name = js['SECT_NAME']
    type = js['SECTTYPE']
    shape = js['SECT_BEFORE']['SHAPE']
    offset = off_JS2Obj(js['SECT_BEFORE'])
    uShear = js['SECT_BEFORE']['USE_SHEAR_DEFORM']
    u7DOF = js['SECT_BEFORE']['USE_WARPING_EFFECT']

    if type == 'DBUSER':
        if js['SECT_BEFORE']['DATATYPE'] ==2:
        #--- USER DEFINED SECTIONS (STANDARD) -------------------
            Section.DBUSER(name,shape,js['SECT_BEFORE']['SECT_I']['vSIZE'],offset,uShear,u7DOF,id)
    
    elif type == 'PSC':
        if shape in ['1CEL','2CEL']:
        #--- PSC 1,2 CELL -------------------
            vA = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_A']
            vB = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_B']
            vC = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_C']
            vD = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_D']
            joint = js['SECT_BEFORE']['JOINT']
            Section.PSC.CEL12(name,shape,joint,
                              vA[0],vA[1],vA[2],vA[3],vA[4],vA[5],
                              vB[0],vB[1],vB[2],vB[3],vB[4],vB[5],
                              vC[0],vC[1],vC[2],vC[3],vC[4],vC[5],vC[6],vC[7],vC[8],vC[9],
                              vD[0],vD[1],vD[2],vD[3],vD[4],vD[5],vD[6],vD[7],
                              offset,uShear,u7DOF,id)
        elif shape in ['PSCI']:
        #--- PSC I -------------------
            symm = js['SECT_BEFORE']['USE_SYMMETRIC']
            vA = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_A']
            vB = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_B']
            vC = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_C']
            vD = js['SECT_BEFORE']['SECT_I']['vSIZE_PSC_D']
            joint = js['SECT_BEFORE']['JOINT']
            Section.PSC.I(name,symm,joint,
                              vA[0],
                              vA[1],vA[2],vA[3],vA[4],vA[5],vA[6],vA[7],vA[8],vA[9],
                              vB[0],vB[1],vB[2],vB[3],vB[4],vB[5],vB[6],
                              vC[0],vC[1],vC[2],vC[3],vC[4],vC[5],vC[6],vC[7],vC[8],
                              vD[0],vD[1],vD[2],vD[3],vD[4],vD[5],vD[6],
                              offset,uShear,u7DOF,id)
    elif type == 'COMPOSITE':
        if shape in ['CI']:
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


            Section.Composite.PSCI(name,False,joint,
                              slab[0],slab[1],slab[2],
                              vA[0],
                              vA[1],vA[2],vA[3],vA[4],vA[5],vA[6],vA[7],vA[8],vA[9],
                              vB[0],vB[1],vB[2],vB[3],vB[4],vB[5],vB[6],
                              vC[0],vC[1],vC[2],vC[3],vC[4],vC[5],vC[6],vC[7],vC[8],
                              vD[0],vD[1],vD[2],vD[3],vD[4],vD[5],vD[6],
                              secti['MATL_ELAST'],secti['MATL_DENS'],secti['MATL_POIS_S'],secti['MATL_POIS_C'],secti['MATL_THERMAL'],
                              secti['USE_MULTI_ELAST'],e1,e2,
                              offset,uShear,u7DOF,id)
        if shape in ['I']:
            vS = js['SECT_BEFORE']['SECT_I']['vSIZE']
            slab = js['SECT_AFTER']['SLAB']
            secti = js['SECT_BEFORE']

            try: e1 = js['SECT_BEFORE']['LONGTERM_ESEC'] 
            except: e1 = 0
            try: e2 = js['SECT_BEFORE']['SHRINK_ESEC'] 
            except: e2 = 0


            Section.Composite.SteelI_Type1(name,
                              slab[0],slab[1],slab[2],
                              vS[0],vS[1],vS[2],vS[3],vS[4],vS[5],
                              secti['MATL_ELAST'],secti['MATL_DENS'],secti['MATL_POIS_S'],secti['MATL_POIS_C'],secti['MATL_THERMAL'],
                              secti['USE_MULTI_ELAST'],e1,e2,
                              offset,uShear,u7DOF,id)




class Offset:
    def __init__(self,OffsetPoint='CC',CenterLocation=0,HOffset=0,HOffOpt=0,VOffset=0,VOffOpt=0,UsrOffOpt=0):

        # self.OFFSET_PT =OffsetPoint
        # self.OFFSET_CENTER =CenterLocation
        # self.HORZ_OFFSET_OPT = HOffOpt
        # self.USERDEF_OFFSET_YI = HOffset
        # self.USERDEF_OFFSET_YJ = HOffset
        # self.VERT_OFFSET_OPT = VOffOpt
        # self.USERDEF_OFFSET_ZI = VOffset
        # self.USERDEF_OFFSET_ZJ = VOffset
        # self.USER_OFFSET_REF = UsrOffOpt

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
        return Offset()
    
    @staticmethod
    def CT():
        return Offset('CT')


def off_JS2Obj(js):
    
        # self.USERDEF_OFFSET_YJ = HOffset

        # self.USERDEF_OFFSET_ZJ = VOffset

    try: OffsetPoint = js['OFFSET_PT']
    except: OffsetPoint='CC'

    try: CenterLocation = js['OFFSET_CENTER']
    except: CenterLocation=0

    try: HOffset = js['USERDEF_OFFSET_YI']
    except: HOffset=0

    try: HOffOpt = js['HORZ_OFFSET_OPT']
    except: HOffOpt=0

    try: VOffOpt = js['VERT_OFFSET_OPT']
    except: VOffOpt=0

    try: VOffset = js['USERDEF_OFFSET_ZI']
    except: VOffset=0

    try: UsrOffOpt = js['USER_OFFSET_REF']
    except: UsrOffOpt=0


    return Offset(OffsetPoint,CenterLocation,HOffset,HOffOpt,VOffset,VOffOpt,UsrOffOpt)




class _common:
    def __str__(self):
        return str(f'ID = {self.ID}  \nJSON : {_Obj2JS(self)}\n')

    def update(self):
        return _updateSect(self)


class Section:
    """Create Sections \n Use Section.USER , Section.PSC to create sections"""
    sect = []
    ids = []


    @classmethod
    def json(cls):
        json = {"Assign":{}}
        for sect in cls.sect:
            js = _Obj2JS(sect)
            json["Assign"][sect.ID] = js
        return json
    
    @staticmethod
    def create():
        MidasAPI("PUT","/db/SECT",Section.json())
        
    @staticmethod
    def get():
        return MidasAPI("GET","/db/SECT")
    
    
    @staticmethod
    def delete():
        MidasAPI("DELETE","/db/SECT")
        Section.sect=[]
        Section.ids=[]


    @staticmethod
    def sync():
        a = Section.get()
        if a != {'message': ''}:
            if list(a['SECT'].keys()) != []:
                Section.sect = []
                Section.ids=[]
                for sect_id in a['SECT'].keys():
                    _JS2Obj(sect_id,a['SECT'][sect_id])


    # ---------------------------------  USER DEFINED SECTIONS --------------------------------------------------------------

    class DBUSER(_common):

        """ Create Standard USER DEFINED sections"""

        def __init__(self,Name='',Shape='',parameters:list=[],Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):  
            """ Shape = 'SB' 'SR' for rectangle \n For cylinder"""
            self.ID = id
            self.NAME = Name
            self.TYPE = 'DBUSER'
            self.SHAPE = Shape
            self.PARAMS = parameters
            self.OFFSET = Offset
            self.USESHEAR = useShear
            self.USE7DOF = use7Dof
            self.DATATYPE = 2

            _SectionADD(self)
    
    class PSC:

        class CEL12(_common):

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

                _SectionADD(self)
        
        class I(_common):

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

                _SectionADD(self)

    class Composite:
        class PSCI(_common):

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

                _SectionADD(self)

        class SteelI_Type1(_common):

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

                _SectionADD(self)
        
            


            


