from ._pscSS import _SS_PSC_12CELL,_SS_PSC_I,_SS_PSC_Value
from ._dbSecSS import _SS_DBUSER
from ._offsetSS import Offset
from ._unSupp import _SS_UNSUPP,_SS_STD_DB
from ._compositeSS import _SS_COMP_PSC_I,_SS_COMP_STEEL_I_TYPE1
from ._TapdbSecSS import _SS_TAPERED_DBUSER

from ._tapPSC12CellSS import _SS_TAP_PSC_12CELL

from midas_civil import MidasAPI


class _helperSECTION:
    ID, NAME, SHAPE, TYPE, OFFSET, USESHEAR, USE7DOF = 0,0,0,0,0,0,0
    def update():
        pass
    def toJSON():
        pass


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



def off_JS2Obj(js):

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



# -------------------  FUNCTION TO CREATE OBJECT used in ELEMENT SYNC  --------------------------
def _JS2OBJ(id,js):
    name = js['SECT_NAME']
    type = js['SECTTYPE']
    shape = js['SECT_BEFORE']['SHAPE']
    offset = off_JS2Obj(js['SECT_BEFORE'])
    uShear = js['SECT_BEFORE']['USE_SHEAR_DEFORM']
    u7DOF = js['SECT_BEFORE']['USE_WARPING_EFFECT']
    if type == 'DBUSER':
        if js['SECT_BEFORE']['DATATYPE'] ==2: obj = _SS_DBUSER._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        else: obj = _SS_STD_DB(id,name,type,shape,offset,uShear,u7DOF,js)

    elif type == 'PSC' :
        if shape in ['1CEL','2CEL']: obj = _SS_PSC_12CELL._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        elif shape in ['PSCI']: obj = _SS_PSC_I._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        elif shape in ['VALU']: obj = _SS_PSC_Value._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        else: obj = _SS_UNSUPP(id,name,type,shape,offset,uShear,u7DOF,js)

    elif type == 'COMPOSITE':
        if shape in ['CI']: obj = _SS_COMP_PSC_I._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        elif shape in ['I']: obj = _SS_COMP_STEEL_I_TYPE1._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        else: obj = _SS_UNSUPP(id,name,type,shape,offset,uShear,u7DOF,js)

    elif type == 'TAPERED' :
        try:
            typeDB = js['SECT_BEFORE']['TYPE']
        except: typeDB = 0
        if typeDB == 2: 
            obj = _SS_TAPERED_DBUSER._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        elif shape in ['1CEL','2CEL']: obj = _SS_TAP_PSC_12CELL._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        else: obj = _SS_UNSUPP(id,name,type,shape,offset,uShear,u7DOF,js)

    else :
        obj = _SS_UNSUPP(id,name,type,shape,offset,uShear,u7DOF,js)


    _SectionADD(obj)





class Section:
    """ NEW Create Sections \n Use Section.USER , Section.PSC to create sections"""
    sect:list[_helperSECTION] = []
    ids:list[int] = []


    @classmethod
    def json(cls):
        json = {"Assign":{}}
        for sect in cls.sect:
            js = sect.toJSON()
            json["Assign"][str(sect.ID)] = js
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
            Section.sect = []
            Section.ids=[]
            for sect_id in a['SECT'].keys():
                _JS2OBJ(sect_id,a['SECT'][sect_id])


#---------------------------------     S E C T I O N S    ---------------------------------------------

    #---------------------     D B   U S E R    --------------------
    @staticmethod
    def DBUSER(Name='',Shape='',parameters:list=[],Offset=Offset(),useShear=True,use7Dof=False,id:int=0): 
        args = locals()
        sect_Obj = _SS_DBUSER(**args)
        _SectionADD(sect_Obj)
        return sect_Obj
    
    class PSC :

        @staticmethod
        def CEL12(Name='',Shape='1CEL',Joint=[0,0,0,0,0,0,0,0],
                    HO1=0,HO2=0,HO21=0,HO22=0,HO3=0,HO31=0,
                    BO1=0,BO11=0,BO12=0,BO2=0,BO21=0,BO3=0,
                    HI1=0,HI2=0,HI21=0,HI22=0,HI3=0,HI31=0,HI4=0,HI41=0,HI42=0,HI5=0,
                    BI1=0,BI11=0,BI12=0,BI21=0,BI3=0,BI31=0,BI32=0,BI4=0,
                    Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
            args = locals()
            sect_Obj = _SS_PSC_12CELL(**args)
            _SectionADD(sect_Obj)
            return sect_Obj
        
        @staticmethod
        def I(Name='',Symm = True,Joint=[0,0,0,0,0,0,0,0,0],
                            H1=0,
                            HL1=0,HL2=0,HL21=0,HL22=0,HL3=0,HL4=0,HL41=0,HL42=0,HL5=0,
                            BL1=0,BL2=0,BL21=0,BL22=0,BL4=0,BL41=0,BL42=0,
                            HR1=0,HR2=0,HR21=0,HR22=0,HR3=0,HR4=0,HR41=0,HR42=0,HR5=0,
                            BR1=0,BR2=0,BR21=0,BR22=0,BR4=0,BR41=0,BR42=0,
                            Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
             
            args = locals()
            sect_Obj = _SS_PSC_I(**args)
            
            _SectionADD(sect_Obj)
            return sect_Obj
        
        @staticmethod
        def Value(Name:str,
                    OuterPolygon:list,InnerPolygon:list=[],
                    Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
             
            args = locals()
            sect_Obj = _SS_PSC_Value(**args)
            
            _SectionADD(sect_Obj)
            return sect_Obj
        
    
    class Composite :
        @staticmethod
        def PSCI(Name='',Symm = True,Joint=[0,0,0,0,0,0,0,0,0],
                    Bc=0,tc=0,Hh=0,
                    H1=0,
                    HL1=0,HL2=0,HL21=0,HL22=0,HL3=0,HL4=0,HL41=0,HL42=0,HL5=0,
                    BL1=0,BL2=0,BL21=0,BL22=0,BL4=0,BL41=0,BL42=0,
                    HR1=0,HR2=0,HR21=0,HR22=0,HR3=0,HR4=0,HR41=0,HR42=0,HR5=0,
                    BR1=0,BR2=0,BR21=0,BR22=0,BR4=0,BR41=0,BR42=0,
                    EgdEsb =0, DgdDsb=0,Pgd=0,Psb=0,TgdTsb=0,
                    MultiModulus = False,CreepEratio=0,ShrinkEratio=0,
                    Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
             
            args = locals()
            sect_Obj = _SS_COMP_PSC_I(**args)
            
            _SectionADD(sect_Obj)
            return sect_Obj
        
        @staticmethod
        def SteelI_Type1(Name='',Bc=0,tc=0,Hh=0,Hw=0,B1=0,tf1=0,tw=0,B2=0,tf2=0,EsEc =0, DsDc=0,Ps=0,Pc=0,TsTc=0,
                MultiModulus = False,CreepEratio=0,ShrinkEratio=0,
                Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
             
            args = locals()
            sect_Obj = _SS_COMP_STEEL_I_TYPE1(**args)
            
            _SectionADD(sect_Obj)
            return sect_Obj
    
    class Tapered:

        @staticmethod
        def DBUSER(Name='',Shape='',params_I:list=[],params_J:list=[],Offset=Offset(),useShear=True,use7Dof=False,id:int=0):
            args = locals()
            sect_Obj = _SS_TAPERED_DBUSER(**args)
            
            _SectionADD(sect_Obj)
            return sect_Obj
        
        @staticmethod
        def PSC12CEL(Name='',Shape='1CEL',Joint=[0,0,0,0,0,0,0,0],
                    HO1_I=0,HO2_I=0,HO21_I=0,HO22_I=0,HO3_I=0,HO31_I=0,
                    BO1_I=0,BO11_I=0,BO12_I=0,BO2_I=0,BO21_I=0,BO3_I=0,
                    HI1_I=0,HI2_I=0,HI21_I=0,HI22_I=0,HI3_I=0,HI31_I=0,HI4_I=0,HI41_I=0,HI42_I=0,HI5_I=0,
                    BI1_I=0,BI11_I=0,BI12_I=0,BI21_I=0,BI3_I=0,BI31_I=0,BI32_I=0,BI4_I=0,

                    HO1_J=0,HO2_J=0,HO21_J=0,HO22_J=0,HO3_J=0,HO31_J=0,
                    BO1_J=0,BO11_J=0,BO12_J=0,BO2_J=0,BO21_J=0,BO3_J=0,
                    HI1_J=0,HI2_J=0,HI21_J=0,HI22_J=0,HI3_J=0,HI31_J=0,HI4_J=0,HI41_J=0,HI42_J=0,HI5_J=0,
                    BI1_J=0,BI11_J=0,BI12_J=0,BI21_J=0,BI3_J=0,BI31_J=0,BI32_J=0,BI4_J=0,

                    Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
            args = locals()
            sect_Obj = _SS_TAP_PSC_12CELL(**args)
            
            _SectionADD(sect_Obj)
            return sect_Obj

        
        

#---------------------------------     T A P E R E D   G R O U P    ---------------------------------------------
    class TaperedGroup:
        
        data = []
        
        def __init__(self, name, elem_list, z_var="LINEAR", y_var="LINEAR", z_exp=2.0, z_from="i", z_dist=0, 
                     y_exp=2.0, y_from="i", y_dist=0, id=""):
            """
            Args:
                name (str): Tapered Group Name (Required).
                elem_list (list): List of element numbers (Required).
                z_var (str): Section shape variation for Z-axis: "LINEAR" or "POLY" (Required).
                y_var (str): Section shape variation for Y-axis: "LINEAR" or "POLY" (Required).
                z_exp (float, optional): Z-axis exponent. Required if z_var is "POLY".
                z_from (str, optional): Z-axis symmetric plane ("i" or "j"). Defaults to "i" for "POLY".
                z_dist (float, optional): Z-axis symmetric plane distance. Defaults to 0 for "POLY".
                y_exp (float, optional): Y-axis exponent. Required if y_var is "POLY".
                y_from (str, optional): Y-axis symmetric plane ("i" or "j"). Defaults to "i" for "POLY".
                y_dist (float, optional): Y-axis symmetric plane distance. Defaults to 0 for "POLY".
                id (str, optional): ID for the tapered group. Auto-generated if not provided.
            
            Example:
                Section.TapperGroup("Linear", [1, 2, 3], "LINEAR", "LINEAR")
                Section.TapperGroup("ZPoly", [4, 5], "POLY", "LINEAR", z_exp=2.5)
            """
            self.NAME = name
            self.ELEM_LIST = elem_list
            self.Z_VAR = z_var
            self.Y_VAR = y_var
            
            # Z-axis parameters (only for POLY)
            if z_var == "POLY":
                if z_exp is None:
                    raise ValueError("z_exp is required when z_var is 'POLY'")
                self.Z_EXP = z_exp
                self.Z_FROM = z_from if z_from is not None else "i"
                self.Z_DIST = z_dist if z_dist is not None else 0
            else:
                self.Z_EXP = None
                self.Z_FROM = None
                self.Z_DIST = None
            
            # Y-axis parameters (only for POLY)
            if y_var == "POLY":
                if y_exp is None:
                    raise ValueError("y_exp is required when y_var is 'POLY'")
                self.Y_EXP = y_exp
                self.Y_FROM = y_from if y_from is not None else "i"
                self.Y_DIST = y_dist if y_dist is not None else 0
            else:
                self.Y_EXP = None
                self.Y_FROM = None
                self.Y_DIST = None
            
            if id == "":
                id = len(Section.TaperedGroup.data) + 1
            self.ID = id
            
            Section.TaperedGroup.data.append(self)
        
        @classmethod
        def json(cls):
            json_data = {"Assign": {}}
            for i in cls.data:
                # Base data that's always included
                tapper_data = {
                    "NAME": i.NAME,
                    "ELEMLIST": i.ELEM_LIST,
                    "ZVAR": i.Z_VAR,
                    "YVAR": i.Y_VAR
                }
                
                # Add Z-axis polynomial parameters only if Z_VAR is "POLY"
                if i.Z_VAR == "POLY":
                    tapper_data["ZEXP"] = i.Z_EXP
                    tapper_data["ZFROM"] = i.Z_FROM
                    tapper_data["ZDIST"] = i.Z_DIST
                
                # Add Y-axis polynomial parameters only if Y_VAR is "POLY"
                if i.Y_VAR == "POLY":
                    tapper_data["YEXP"] = i.Y_EXP
                    tapper_data["YFROM"] = i.Y_FROM
                    tapper_data["YDIST"] = i.Y_DIST
                
                json_data["Assign"][str(i.ID)] = tapper_data
            
            return json_data
        
        @classmethod
        def create(cls):
            MidasAPI("PUT", "/db/tsgr", cls.json())
        
        @classmethod
        def get(cls):
            return MidasAPI("GET", "/db/tsgr")
        
        @classmethod
        def delete(cls):
            cls.data = []
            return MidasAPI("DELETE", "/db/tsgr")
        
        @classmethod
        def sync(cls):
            cls.data = []
            response = cls.get()
            
            if response and response != {'message': ''}:
                tsgr_data = response.get('TSGR', {})
                # Iterate through the dictionary of tapered groups from the API response
                for tsgr_id, item_data in tsgr_data.items():
                    # Extract base parameters
                    name = item_data.get('NAME')
                    elem_list = item_data.get('ELEMLIST')
                    z_var = item_data.get('ZVAR')
                    y_var = item_data.get('YVAR')
                    
                    # Extract optional parameters based on variation type
                    z_exp = item_data.get('ZEXP') if z_var == "POLY" else None
                    z_from = item_data.get('ZFROM') if z_var == "POLY" else None
                    z_dist = item_data.get('ZDIST') if z_var == "POLY" else None
                    
                    y_exp = item_data.get('YEXP') if y_var == "POLY" else None
                    y_from = item_data.get('YFROM') if y_var == "POLY" else None
                    y_dist = item_data.get('YDIST') if y_var == "POLY" else None
                    
                    Section.TaperedGroup(
                        name=name,
                        elem_list=elem_list,
                        z_var=z_var,
                        y_var=y_var,
                        z_exp=z_exp,
                        z_from=z_from,
                        z_dist=z_dist,
                        y_exp=y_exp,
                        y_from=y_from,
                        y_dist=y_dist,
                        id=tsgr_id
                    )