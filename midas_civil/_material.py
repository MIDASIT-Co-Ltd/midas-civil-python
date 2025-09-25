from ._mapi import *




class Material:
    mats = []
    ids = []
    def __init__(self,data,id=0):
        if Material.ids == []: 
            count = 1
        else:
            count = max(Material.ids)+1
        if id == 0 or id in Material.ids: self.ID = count
        if id!= 0 and id not in Material.ids: self.ID = id

        self.DATA = data

        Material.mats.append(self)
        Material.ids.append(self.ID)
    
    @classmethod
    def json(cls):
        json = {"Assign":{}}
        for k in cls.mats:
            json["Assign"][k.ID]=k.DATA
        return json
    
    @staticmethod
    def create_only():
        return MidasAPI("PUT","/db/MATL",Material.json())
        
    @staticmethod
    def get():
        return MidasAPI("GET","/db/MATL")
    
    
    @staticmethod
    def delete():
        MidasAPI("DELETE","/db/MATL")
        Material.mats=[]
        Material.ids=[]

    @staticmethod
    def sync():
        a = Material.get()
        if a != {'message': ''}:
            if list(a['MATL'].keys()) != []:
                Material.mats = []
                Material.ids=[]
                for j in a['MATL'].keys():
                    Material(a['MATL'][j], int(j))

        # ----------------------------------  ALL FUNCTIONS  ---------------------------------------------------
    
    @staticmethod
    def create():
        if Material.mats!=[] : Material.create_only()
        if CreepShrinkage.mats!=[] : CreepShrinkage.create()
        if CompStrength.mats!=[] : CompStrength.create()
        if TDMatLink.json()!={'Assign':{}} : TDMatLink.create()
        
    
    @staticmethod
    def deleteAll():
        Material.delete()
        CreepShrinkage.delete()
        CompStrength.delete()
        


# ---------------------------------  CONCRETE MATERIAL --------------------------------------------------------------

    class CONC:


        # ----------------------------------  DB MATERIAL ---------------------------------------------------

        def __init__(self,name='',standard='',db='',id:int=0,):  
            js =  {
                "TYPE": "CONC",
                "NAME": name,
                "DAMP_RAT": 0.05,
                "PARAM": [
                    {
                        "P_TYPE": 1,
                        "STANDARD": standard,
                        "CODE": "",
                        "DB": db,
                    }
                ]
            }
            temp = Material(js,id)
            self.ID = temp.ID
            self.DATA = js


        # ----------------------------------  USER MATERIAL ---------------------------------------------------

        class User:
            def __init__(self,name='',E=0,pois=0,den=0,mass=0,therm=0,id:int=0,):
                js =  {
                    "TYPE": "CONC",
                    "NAME": name,
                    "DAMP_RAT": 0.05,
                    "PARAM": [
                        {
                            "P_TYPE": 2,
                            "ELAST": E,
                            "POISN": pois,
                            "THERMAL": therm,
                            "DEN": den,
                            "MASS": mass
                        }
                    ]
                }
                temp = Material(js,id)
                self.ID = temp.ID
                self.DATA = js

    

# ---------------------------------  STEEL MATERIAL --------------------------------------------------------------

    class STEEL:

        # ----------------------------------  DB MATERIAL ---------------------------------------------------

        def __init__(self,name='',standard='',db='',id:int=0,):
            js =  {
                "TYPE": "STEEL",
                "NAME": name,
                "DAMP_RAT": 0.05,
                "PARAM": [
                    {
                        "P_TYPE": 1,
                        "STANDARD": standard,
                        "CODE": "",
                        "DB": db,
                    }
                ]
            }
            temp = Material(js,id)
            self.ID = temp.ID
            self.DATA = js


        # ----------------------------------  USER MATERIAL ---------------------------------------------------

        class User:
            def __init__(self,name='',E=0,pois=0,den=0,mass=0,therm=0,id:int=0,):
                js =  {
                    "TYPE": "STEEL",
                    "NAME": name,
                    "DAMP_RAT": 0.05,
                    "PARAM": [
                        {
                            "P_TYPE": 2,
                            "ELAST": E,
                            "POISN": pois,
                            "THERMAL": therm,
                            "DEN": den,
                            "MASS": mass
                        }
                    ]
                }
                temp = Material(js,id)
                self.ID = temp.ID
                self.DATA = js




# ---------------------------------  USER MATERIAL --------------------------------------------------------------

    class USER:

        def __init__(self,name='',E=0,pois=0,den=0,mass=0,therm=0,id:int=0,):
            js =  {
                "TYPE": "USER",
                "NAME": name,
                "DAMP_RAT": 0.05,
                "PARAM": [
                    {
                        "P_TYPE": 2,
                        "ELAST": E,
                        "POISN": pois,
                        "THERMAL": therm,
                        "DEN": den,
                        "MASS": mass
                    }
                ]
            }
            temp = Material(js,id)
            self.ID = temp.ID
            self.DATA = js


# ------------------------------------------ TIME DEPENDENT - CREEP and SHRINKAGE ----------------------------------------------------

class CreepShrinkage:
    mats = []
    ids = []
    def __init__(self,data,id=0):
        if CreepShrinkage.ids == []:
            count = 1
        else:
            count = max(CreepShrinkage.ids)+1
        if id == 0 or id in CreepShrinkage.ids: self.ID = count
        if id!= 0 and id not in CreepShrinkage.ids: self.ID = id

        self.DATA = data

        CreepShrinkage.mats.append(self)
        CreepShrinkage.ids.append(self.ID)

    @classmethod
    def json(cls):
        json = {"Assign":{}}
        for k in cls.mats:
            json["Assign"][k.ID]=k.DATA
        return json

    @staticmethod
    def create():
        MidasAPI("PUT","/db/TDMT",CreepShrinkage.json())

    @staticmethod
    def get():
        return MidasAPI("GET","/db/TDMT")


    @staticmethod
    def delete():
        MidasAPI("DELETE","/db/TDMT")
        CreepShrinkage.mats=[]
        CreepShrinkage.ids=[]

    @staticmethod
    def sync():
        a = CreepShrinkage.get()
        if a != {'message': ''}:
            if list(a['TDMT'].keys()) != []:
                CreepShrinkage.mats = []
                CreepShrinkage.ids=[]
                for j in a['TDMT'].keys():
                    CreepShrinkage(a['TDMT'][j], int(j))

    # ---------------------------------  IRC CnS --------------------------------------------------------------

    class IRC:
        def __init__(self,name: str, code_year: int = 2011, fck: float = 0, notional_size: float = 1,
                     relative_humidity: float = 70, age_shrinkage: int = 3, type_cement: str = 'NR', id: int = 0):
            """
            IRC Creep and Shrinkage for Indian Road Congress standards. 

            Parameters:
                name (str): The name for the material property.
                code_year (int, optional): The year of the IRC code. Can be 2000 or 2011. Defaults to 2011.
                fck (float): 28-day characteristic compressive strength. 
                notional_size (float): The notional size of the member 
                relative_humidity (float): The relative humidity in percentage (40-99%). 
                age_shrinkage (int): The age of the concrete at the beginning of shrinkage in days. 
                type_cement (str, optional): The type of cement ('SL'= Slow Setting cement, 'NR'= Normal cement, 'RS'=Rapid hardening cement). Only for IRC:112-2011. Defaults to 'NR'. 
                id (int, optional): A specific ID for the material. Auto-generated if not provided.

            Examples:
                ```python
                # Create a material based on IRC:112-2011
                CreepShrinkage.IRC("IRC_M30_2011", code_year=2011, fck=30000, notional_size=1, type_cement = "RS", age_shrinkage=7)

                # Create a material based on IRC:18-2000
                CreepShrinkage.IRC("IRC_M25_2000", code_year=2000, fck=25000, notional_size=1, relative_humidity=80, age_shrinkage=3)
                ```
            """
            code_name = ""
            if code_year == 2011:
                code_name = "INDIA_IRC_112_2011"
            elif code_year == 2000:
                code_name = "INDIA_IRC_18_2000"
            else:
                code_name = "INDIA_IRC_112_2011"
            
            if type_cement == "SL":
                type_cement = "RS"
            elif type_cement == "RS":
                type_cement = "SL"

            js =  {
                "NAME": name,
                "CODE": code_name,
                "STR": fck,
                "HU": relative_humidity,
                "AGE": age_shrinkage,
                "MSIZE": notional_size
            }
            if code_year == 2011:
                js["CTYPE"] = type_cement

            temp = CreepShrinkage(js,id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  CEB-FIP CnS --------------------------------------------------------------

    class CEB_FIP:
        def __init__(self, name: str, code_year: int = 2010, fck: float = 0, notional_size: float = 1,
                     relative_humidity: float = 70, age_shrinkage: int = 3, type_cement: str = 'RS',
                     type_of_aggregate: int = 0, id: int = 0):
            """
            CEB-FIP Creep and Shrinkage for European concrete standards.

            Parameters:
                name (str): The name for the material property. 
                code_year (int, optional): Year of the CEB-FIP standard (2010, 1990, 1978). Defaults to 2010.
                fck (float): 28-day characteristic compressive strength. 
                notional_size (float): The notional size of the member. 
                relative_humidity (float): The relative humidity in percentage (40-100%). 
                age_shrinkage (int): The age of the concrete at the beginning of shrinkage in days. 
                type_cement (str, optional): The type of cement ('RS', 'NR', 'SL'). Defaults to 'RS'. 
                type_of_aggregate (int, optional): Type of aggregate, only for CEB-FIP 2010. 0: Basalt, 1: Quartzite, 2: Limestone, 3: Sandstone. Defaults to 0. 
                id (int, optional): A specific ID for the material. Auto-generated if not provided.

            Examples:
                ```python
                # Create a CEB-FIP 2010 material
                CreepShrinkage.CEB_FIP("CEB_M40", code_year=2010, fck=40000, notional_size=2, relative_humidity=65, age_shrinkage=5)

                # Create a CEB-FIP 1990 material
                CreepShrinkage.CEB_FIP("CEB_M35", code_year=1990, fck=35000, notional_size=3, relative_humidity=70, age_shrinkage=3)
                ```
            """
            code_name = ""
            if code_year == 2010:
                code_name = "CEB_FIP_2010"
            elif code_year == 1990:
                code_name = "CEB"
            elif code_year == 1978:
                code_name = "CEB_FIP_1978"
            else:
                code_name = "CEB_FIP_2010"

            js = {
                "NAME": name,
                "CODE": code_name,
                "STR": fck,
                "HU": relative_humidity,
                "AGE": age_shrinkage,
                "MSIZE": notional_size,
                "CTYPE": type_cement,
            }
            if code_year == 2010:
                js["TYPEOFAFFR"] = type_of_aggregate

            temp = CreepShrinkage(js, id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  ACI CnS --------------------------------------------------------------

    class ACI:
        def __init__(self, name: str, fck: float = 0, relative_humidity: float = 70, age_shrinkage: int = 3,
                     vol_surface_ratio: float = 1.2, cfact_a: float = 4, cfact_b: float = 0.85,
                     curing_method: str = "MOIST", material_type: str = "CODE", cement_content: float = 24,
                     slump: float = 1.1, fine_agg_percent: float = 12, air_content: float = 13,
                     creep_coeff: float = None, shrink_strain: float = None, id: int = 0):
            """
            ACI Creep and Shrinkage for American Concrete Institute standards. 

            Parameters:
                name (str): The name for the material property.
                fck (float): 28-day compressive strength . 
                relative_humidity (float): The relative humidity (40-99%). 
                age_shrinkage (int): The age of the concrete at the beginning of shrinkage in days. 
                vol_surface_ratio (float): The volume to surface area ratio. 
                cfact_a (float): Concrete compressive strength factor 'a'. 
                cfact_b (float): Concrete compressive strength factor 'b'. 
                curing_method (str, optional): Curing method ('MOIST' or 'STEAM'). Defaults to 'MOIST'. 
                material_type (str, optional): Material factored ultimate value type ('CODE' or 'USER'). Defaults to 'CODE'. 
                cement_content (float, optional): Cement content (used if material_type='CODE'). 
                slump (float, optional): Slump value (used if material_type='CODE'). 
                fine_agg_percent (float, optional): Fine aggregate percentage (used if material_type='CODE'). 
                air_content (float, optional): Air content (used if material_type='CODE'). 
                creep_coeff (float, optional): Creep coefficient (used if material_type='USER'). 
                shrink_strain (float, optional): Shrinkage strain in E-6 (used if material_type='USER'). 
                id (int, optional): A specific ID for the material. Auto-generated if not provided.

            Examples:
                ```python
                # Create an ACI material using code-based properties
                CreepShrinkage.ACI("ACI_C35_Code", fck=35000, relative_humidity=75, age_shrinkage=7, vol_surface_ratio=50)

                # Create an ACI material using user-defined ultimate values
                CreepShrinkage.ACI("ACI_C35_User", fck=35000, relative_humidity=75, age_shrinkage=7, vol_surface_ratio=50, material_type="USER", creep_coeff=2.5, shrink_strain=600)
                ```
            """
            js = {
                "NAME": name,
                "CODE": "ACI",
                "STR": fck,
                "HU": relative_humidity,
                "AGE": age_shrinkage,
                "VOL": vol_surface_ratio,
                "CFACTA": cfact_a,
                "CFACTB": cfact_b,
                "TYPE": material_type,
                "CMETHOD": curing_method
            }

            if material_type == "CODE":
                js.update({
                    "CEMCONTENT": cement_content,
                    "SLUMP": slump,
                    "FAPERCENT": fine_agg_percent,
                    "AIRCONTENT": air_content
                })
            elif material_type == "USER":
                js.update({
                    "CREEPCOEFF": creep_coeff if creep_coeff is not None else 1.4,
                    "SHRINKSTRAIN": shrink_strain if shrink_strain is not None else 500
                })

            temp = CreepShrinkage(js, id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  AASHTO CnS --------------------------------------------------------------

    class AASHTO:
        def __init__(self, name: str, fck: float = 0, relative_humidity: float = 70, age_shrinkage: int = 3,
                     vol_surface_ratio: float = 1.2, b_expose: bool = False, id: int = 0):
            """
            AASHTO Creep and Shrinkage model.

            Parameters:
                name (str): The name for the material property.
                fck (float): 28-day compressive strength.
                relative_humidity (float): The relative humidity (40-99%).
                age_shrinkage (int): The age of the concrete at the beginning of shrinkage in days.
                vol_surface_ratio (float): The volume to surface area ratio.
                b_expose (bool, optional): Expose to drying before 5 days of curing. Defaults to False.
                id (int, optional): A specific ID for the material. Auto-generated if not provided.

            Examples:
                ```python
                CreepShrinkage.AASHTO("AASHTO_M30", fck=30000, relative_humidity=80, age_shrinkage=5, vol_surface_ratio=60)
                ```
            """
            js = {
                "NAME": name,
                "CODE": "AASHTO",
                "STR": fck,
                "HU": relative_humidity,
                "AGE": age_shrinkage,
                "VOL": vol_surface_ratio,
                "bEXPOSE": b_expose
            }
            temp = CreepShrinkage(js, id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  European CnS --------------------------------------------------------------

    class European:
        def __init__(self, name: str, fck: float = 0, relative_humidity: float = 70, age_shrinkage: int = 3,
                     notional_size: float = 1.2, type_cement: str = "Class N", t_code: int = 0, b_silica: bool = False, id: int = 0):
            """
            European Creep and Shrinkage model (EN 1992). 

            Parameters:
                name (str): The name for the material property.
                fck (float): 28-day characteristic compressive strength. 
                relative_humidity (float): The relative humidity in percentage (40-99%). 
                age_shrinkage (int): The age of the concrete at the beginning of shrinkage in days. 
                notional_size (float): The notional size of the member. 
                type_cement (str, optional): Cement class ('Class S', 'Class N', 'Class R'). Defaults to 'Class N'. 
                t_code (int, optional): Type of code. 0: EN 1992-1 (General), 1: EN 1992-2 (Bridge). Defaults to 0. 
                b_silica (bool, optional): Whether silica fume is used. Only applicable when t_code is 1. Defaults to False. 
                id (int, optional): A specific ID for the material. Auto-generated if not provided.

            Examples:
                ```python
                # EN 1992-1 General Structure
                CreepShrinkage.European("Euro_General_C30", fck=30000, relative_humidity=75, age_shrinkage=7, notional_size=2)

                # EN 1992-2 Concrete Bridge with Silica Fume
                CreepShrinkage.European("Euro_Bridge_C40", fck=40000, relative_humidity=70, age_shrinkage=5, notional_size=2, t_code=1, b_silica=True)
                ```
            """
            js = {
                "NAME": name,
                "CODE": "EUROPEAN",
                "STR": fck,
                "HU": relative_humidity,
                "AGE": age_shrinkage,
                "MSIZE": notional_size,
                "CTYPE": type_cement,
                "TCODE": t_code,
            }
            if t_code == 1:
                js["bSILICA"] = b_silica

            temp = CreepShrinkage(js, id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  Russian CnS --------------------------------------------------------------
    class Russian:
        def __init__(self, name: str, fck: float, relative_humidity: float, module_exposed_surface: float,
                     age_concrete: int, water_content: float, max_aggregate_size: float, air_content: float,
                     specific_cement_paste_content: float, curing_method: int = 0,cement_type=1, fast_accumulating_creep: bool = False,
                     concrete_type: int = 0, id: int = 0):
            """
            Russian Creep and Shrinkage model. 

            Parameters:
                name (str): The name for the material property. 
                fck (float): 28-day compressive strength. 
                relative_humidity (float): The relative humidity in percentage. 
                module_exposed_surface (float): The module of an exposed surface. 
                age_concrete (int): The age of the concrete in days. 
                water_content (float): The water content . 
                max_aggregate_size (float): Maximum aggregate size. 
                air_content (float): Air content. 
                specific_cement_paste_content (float): Specific content of the cement paste. 
                curing_method (int, optional): Curing method. 0: Natural, 1: Steam. Defaults to 0.
                cement_type(int ,optional) : Cement Type. 0: Normal (Default), 1: Fast-hardened , 2: Slag ,3: Pozzolan
                fast_accumulating_creep (bool, optional): Whether to consider fast-accumulating creep. Defaults to False. 
                concrete_type (int, optional): Type of concrete. 0: Heavy, 1: Fine-grained. Defaults to 0. 
                id (int, optional): A specific ID for the material. Auto-generated if not provided.

            Examples:
                ```python
                # Standard Russian model with natural curing
                CreepShrinkage.Russian("RU_Heavy_C30", fck=30000, relative_humidity=70, module_exposed_surface=10, age_concrete=14, water_content=180, max_aggregate_size=0.02, air_content=30, specific_cement_paste_content=0.25,cement_type=2)
                ```
            """
            js = {
                "NAME": name,
                "CODE": "RUSSIAN",
                "STR": fck,
                "HU": relative_humidity,
                "M": module_exposed_surface,
                "AGE": age_concrete,
                "CMETH": curing_method,
                "iCTYPE": cement_type,
                "CREEP": fast_accumulating_creep,
                "CONCT": concrete_type,
                "W": water_content,
                "MAXS": max_aggregate_size,
                "A": air_content,
                "PZ": specific_cement_paste_content
            }
            temp = CreepShrinkage(js, id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  AS & NZ CnS -------------------------------------------------
    class AS_NZ:
        def __init__(self, name: str, standard: str, fck: float, concrete_age: int,
                    hypothetical_thickness: float, drying_shrinkage_type: int = 0,
                    user_defined_shrinkage_strain: float = 0, humidity_factor: float = 0.72,
                    exposure_environment: int = 0, id: int = 0):
            """
            Australian & New Zealand Standards Creep and Shrinkage model.

            Parameters:
                name (str): The name for the material property.
                standard (str): The standard code. Valid codes are 'AS_5100_5_2017', 'AS_5100_5_2016', 'AS_RTA_5100_5_2011', 'AS_3600_2009', 'NEWZEALAND'.
                fck (float): 28-day compressive strength
                concrete_age (int): The age of the concrete in days
                hypothetical_thickness (float): The hypothetical thickness of the member
                drying_shrinkage_type (int, optional): Type of drying basic shrinkage strain,The values depend on the chosen standard.
                    - For AS Standards ('AS_5100_5_2017', 'AS_5100_5_2016', etc.):
                    - 0: 800.0 (Sydney, Brisbane)
                    - 1: 900.0 (Melbourne)
                    - 2: 1000.0 (Elsewhere)
                    - 3: User Defined Value
                - For NZ Bridge Standard ('NEWZEALAND'):
                    - 0: 1500 (Hastings, Palmerston North, etc.)
                    - 1: 1460 (Nelson)
                    - 2: 1315 (Kaitaia, Tauranga)
                    - 3: 1080 (New Plymouth, Taranaki)
                    - 4: 1000 (Whangarei, Auckland Hunua, Hamilton)
                    - 5: 990 (Auckland)
                    - 6: 950 (Christchurch, Timaru, etc.)
                    - 7: 775 (Westport, Queenstown, etc.)
                    - 8: 735 (Dunedin)
                    - 9: 570 (Waiapu)
                    - 10: User Defined Value
                user_defined_shrinkage_strain (float, optional): The user-defined drying basic shrinkage strain, This value is ONLY used when `drying_shrinkage_type` is set to a user-defined option (3 for AS, 10 for NZ).
                humidity_factor (float, optional): Relative humidity thickness. This is only for the NZ Bridge standard and has a range of 0.20 to 0.72. Defaults to 0.72.
                exposure_environment (int, optional): Exposure environment classification ("EXPOSURE") for AS standards. Defaults to 0.
                id (int, optional): A specific ID for the material. Auto-generated if not provided.

            Examples:
                ```python
                # AS 5100.5-2017 
                CreepShrinkage.AS_NZ("AS_Melbourne_C40", standard="AS_5100_5_2017", fck=40000, hypothetical_thickness=0.3, concrete_age=7, drying_shrinkage_type=1)

                # NZ Bridge standard 
                CreepShrinkage.AS_NZ("NZ_Bridge_Custom", standard="NEWZEALAND", fck=35000, hypothetical_thickness=0.25, concrete_age=14, drying_shrinkage_type=10, user_defined_shrinkage_strain=955.5)
                ```
            """
            js = {
                "NAME": name,
                "CODE": standard,
                "STR": fck,
                "THIK": hypothetical_thickness,
                "AGE": concrete_age,
                "iEPS_DRY": drying_shrinkage_type,
            }

            # Internal maps for predefined shrinkage values from the manual
            as_strain_map = {0: 800.0, 1: 900.0, 2: 1000.0}
            nz_strain_map = {0: 1500.0, 1: 1460.0, 2: 1315.0, 3: 1080.0, 4: 1000.0, 5: 990.0, 6: 950.0, 7: 775.0, 8: 735.0, 9: 570.0}

            eps_dry_value = None
            is_as_code = standard != "NEWZEALAND"
            is_nz_code = standard == "NEWZEALAND"

            # Check for user-defined cases first
            if is_as_code and drying_shrinkage_type == 3:
                eps_dry_value = user_defined_shrinkage_strain
            elif is_nz_code and drying_shrinkage_type == 10:
                eps_dry_value = user_defined_shrinkage_strain
            # Otherwise, look up the predefined value from the appropriate map
            elif is_as_code:
                eps_dry_value = as_strain_map.get(drying_shrinkage_type)
            elif is_nz_code:
                eps_dry_value = nz_strain_map.get(drying_shrinkage_type)

            js["EPS_DRY"] = eps_dry_value

            # Add parameters specific to the standard
            if is_nz_code:
                js["FS"] = humidity_factor
            else: # Assumes all other codes are AS standards
                js["EXPOSURE"] = exposure_environment

            temp = CreepShrinkage(js, id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  Chinese Standard CnS ----------------------------------------------------

    class Chinese:
        def __init__(self, name: str, standard: str, fck: float, relative_humidity: float,
                     concrete_age: int, notional_size: float, humidity_type: str = "RH",
                     cement_coeff: float = 5, fly_ash_amount: float = 20, id: int = 0):
            """
            Chinese Standards Creep and Shrinkage model.

            Parameters:
                name (str): The name for the material property. 
                standard (str): The Chinese standard code ('CHINESE', 'JTG', 'CHINA_JTG3362_2018'). 
                fck (float): 28-day compressive strength. 
                relative_humidity (float): The relative humidity in percentage. 
                concrete_age (int): The age of the concrete in days. 
                notional_size (float): The notional size of the member. 
                humidity_type (str, optional): Type of relative humidity ('CU' for Curing Underwater, 'RH' for Relative Humidity). Defaults to 'RH'. 
                cement_coeff (float, optional): Cement type coefficient (for JTG codes). Defaults to 5. 
                fly_ash_amount (float, optional): Amount of added fly ash (for JTG3362-2018). Range 0-30. Defaults to 20. 
                id (int, optional): A specific ID for the material. Auto-generated if not provided.

            Examples:
                ```python
                # General Chinese Standard
                CreepShrinkage.Chinese("Chinese_C30", standard="CHINESE", fck=30000, relative_humidity=75, concrete_age=14, notional_size=2)

                # JTG D62-2004 Standard
                CreepShrinkage.Chinese("JTG_D62_C40", standard="JTG", fck=40000, relative_humidity=80, concrete_age=7, notional_size=250, cement_coeff=5)
                ```
            """
            js = {
                "NAME": name,
                "CODE": standard,
                "STR": fck,
                "HU": relative_humidity,
                "AGE": concrete_age,
                "MSIZE": notional_size,
                "HTYPE": humidity_type
            }
            if "JTG" in standard:
                js["BSC"] = cement_coeff
            if standard == "CHINA_JTG3362_2018":
                js["FLYASH"] = fly_ash_amount

            temp = CreepShrinkage(js, id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  Korean Standards CnS ----------------------------------------------------

    class Korean:
        def __init__(self, name: str, standard: str, fck: float, relative_humidity: float,
                     concrete_age: int, notional_size: float, cement_type: str = "NR",
                     density: float = 240, id: int = 0):
            """
            Korean Standards Creep and Shrinkage model.

            Parameters:
                name (str): The name for the material property. 
                standard (str): The Korean standard code ('KDS_2016', 'KSI_USD12', 'KSCE_2010', 'KS'). 
                fck (float): 28-day compressive strength. 
                relative_humidity (float): The relative humidity in percentage. 
                concrete_age (int): The age of the concrete in days. 
                notional_size (float): The notional size of the member. 
                cement_type (str, optional): The type of cement ('SL', 'NR', 'RS'). Defaults to 'NR'. 
                density (float, optional): Weight density  (Only for KDS-2016). Defaults to 240. 
                id (int, optional): A specific ID for the material. Auto-generated if not provided.

            Examples:
                ```python
                # KDS-2016 Standard
                CreepShrinkage.Korean("KDS_C35", standard="KDS_2016", fck=35000, relative_humidity=65, concrete_age=10, notional_size=2, density=2400)

                # Korea Standard (KS)
                CreepShrinkage.Korean("KS_C30", standard="KS", fck=30000, relative_humidity=70, concrete_age=14, notional_size=2)
                ```
            """
            js = {
                "NAME": name,
                "CODE": standard,
                "STR": fck,
                "HU": relative_humidity,
                "AGE": concrete_age,
                "MSIZE": notional_size,
                "CTYPE": cement_type
            }
            if standard == "KDS_2016":
                js["DENSITY"] = density

            temp = CreepShrinkage(js, id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  PCA CnS -----------------------------------------------------------------

    class PCA:
        def __init__(self, name: str, fck: float, relative_humidity: float, ultimate_creep_strain: float,
                     vol_surface_ratio: float, reinforcement_ratio: float, steel_elasticity_modulus: float,
                     ultimate_shrinkage_strain: float, id: int = 0):
            """
            PCA Creep and Shrinkage model.

            Parameters:
                name (str): The name for the material property. 
                fc (float): Compressive strength
                relative_humidity (float): The relative humidity in percentage. (Range : 40-99) 
                ultimate_creep_strain (float): Ultimate creep strain. (Range : 3-5) 
                vol_surface_ratio (float): The volume to surface area ratio. 
                reinforcement_ratio (float): Reinforcement ratio of the cross section. 
                steel_elasticity_modulus (float): Modulus of elasticity of steel. 
                ultimate_shrinkage_strain (float): Ultimate shrinkage strain. (Range : 500-800) 
                id (int, optional): A specific ID for the material. Auto-generated if not provided.

            Examples:
                ```python
                CreepShrinkage.PCA("PCA_Material", fck=50000, relative_humidity=70, ultimate_creep_strain=4, vol_surface_ratio=1.2, reinforcement_ratio=20, steel_elasticity_modulus=2e8, ultimate_shrinkage_strain=780)
                ```
            """
            js = {
                "NAME": name,
                "CODE": "PCA",
                "STR": fck,
                "HU": relative_humidity,
                "UCS": ultimate_creep_strain,
                "VOL": vol_surface_ratio,
                "RR": reinforcement_ratio,
                "MOD": steel_elasticity_modulus,
                "USS": ultimate_shrinkage_strain
            }
            temp = CreepShrinkage(js, id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  Japan CnS ---------------------------------------------------------------

    class Japan:
        def __init__(self, name: str, standard: str, relative_humidity: float, concrete_age: int,
                     vol_surface_ratio: float, cement_content: float, water_content: float, fck: float = 30000,
                     impact_factor: float = 1, age_of_solidification: int = 5, alpha_factor: int = 11,
                     autogenous_shrinkage: bool = True, gamma_factor: int = 1, a_factor: float = 0.1,
                     b_factor: float = 0.7, general_shrinkage: bool = True, id: int = 0):
            """
            Japan Creep and Shrinkage model (JSCE). 

            Parameters:
                name (str): The name for the material property. 
                standard (str): The Japanese standard ('JSCE_12', 'JSCE_07', 'JSCE'). 
                relative_humidity (float): The relative humidity in percentage. 
                concrete_age (int): The age of the concrete in days. 
                vol_surface_ratio (float): The volume to surface area ratio. 
                cement_content (float): Cement content. 
                water_content (float): Water content. 
                fck (float, optional): Compressive strength (not for JSCE). Defaults to 30000. 
                impact_factor (float, optional): Impact factor by cement type (JSCE 2012 only). Defaults to 1. 
                age_of_solidification (int, optional): Age at beginning of solidification (JSCE 2012 only). Defaults to 5. 
                alpha_factor (int, optional): Alpha-factor by cement type (JSCE 2007 only). Defaults to 11. 
                autogenous_shrinkage (bool, optional): Autogenous shrinkage option (JSCE 2007 only). Defaults to True. 
                gamma_factor (int, optional): Gamma-factor (JSCE 2007 only). Defaults to 1. 
                a_factor (float, optional): a-factor (JSCE 2007 only). Defaults to 0.1. 
                b_factor (float, optional): b-factor (JSCE 2007 only). Defaults to 0.7. 
                general_shrinkage (bool, optional): General shrinkage option (JSCE 2007 only). Defaults to True. 
                id (int, optional): A specific ID for the material. Auto-generated if not provided.

            Examples:
                ```python
                # JSCE 2012
                CreepShrinkage.Japan("JSCE12_mat", "JSCE_12", 70, 3, 0.2, 30, 20, fck=30000)
                # JSCE 2007
                CreepShrinkage.Japan("JSCE07_mat", "JSCE_07", 70, 3, 0.2, 30, 20, fck=30000, alpha_factor=15)
                ```
            """
            js = {
                "NAME": name,
                "CODE": standard,
                "HU": relative_humidity,
                "AGE": concrete_age,
                "VOL": vol_surface_ratio,
                "CEMCONTENT": cement_content,
                "WATERCONTENT": water_content
            }
            if standard != "JSCE":
                js["STR"] = fck
            if standard == "JSCE_12":
                js["IPFACT"] = impact_factor
                js["AGESOL"] = age_of_solidification
            if standard == "JSCE_07":
                js["ALPHAFACT"] = alpha_factor
                js["bAUTO"] = autogenous_shrinkage
                if autogenous_shrinkage:
                    js["GAMMAFACT"] = gamma_factor
                    js["AFACT"] = a_factor
                    js["BFACT"] = b_factor
                js["bGEN"] = general_shrinkage

            temp = CreepShrinkage(js, id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  Japanese Standard CnS ---------------------------------------------
    class JapaneseStandard:
        def __init__(self, name: str, fck: float, relative_humidity: float, concrete_age: int, notional_size: float,
                     calculation_method: str = "JSCE", humidity_type: str = "RH", cement_type: str = "NC",
                     environmental_coeff: int = 1, id: int = 0):
            """
            Japanese Standard Creep and Shrinkage model. 

            Parameters:
                name (str): The name for the material property. 
                fck (float): Compressive strength 
                relative_humidity (float): The relative humidity in percentage (40-90%). 
                concrete_age (int): The age of the concrete in days. 
                notional_size (float): The notional size of the member. 
                calculation_method (str, optional): Calculation method for E ('JSCE' or 'AIJ'). Defaults to 'JSCE'. 
                humidity_type (str, optional): Relative humidity type ('RH' or 'CU'). Defaults to 'RH'. 
                cement_type (str, optional): Type of cement ('RH', 'NC'). Defaults to 'NC'. 
                environmental_coeff (int, optional): Environmental coefficient. Defaults to 1. 
                id (int, optional): A specific ID for the material. Auto-generated if not provided.

            Examples:
                ```python
                CreepShrinkage.JapaneseStandard("JapanStd_C30", fck=30000, relative_humidity=70, concrete_age=3, notional_size=1.2)
                ```
            """
            js = {
                "NAME": name,
                "CODE": "JAPAN",
                "STR": fck,
                "HU": relative_humidity,
                "HTYPE": humidity_type,
                "AGE": concrete_age,
                "MSIZE": notional_size,
                "CTYPE": cement_type,
                "CM": calculation_method,
                "LAMBDA": environmental_coeff
            }
            temp = CreepShrinkage(js, id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  User Defined CnS ----------------------------------------------------

    class UserDefined:
        def __init__(self, name: str, shrinkage_func_name: str, creep_func_name: str, creep_age: int, id: int = 0):
            """
            User Defined Creep and Shrinkage model.

            Parameters:
                name (str): The name for the material property. 
                shrinkage_func_name (str): The name of the user-defined shrinkage strain function. 
                creep_func_name (str): The name of the user-defined creep function. 
                creep_age (int): Concrete age for the creep function. 
                id (int, optional): A specific ID for the material. Auto-generated if not provided.
            """
            js = {
                "NAME": name,
                "CODE": "USER_DEFINED",
                "SSFNAME": shrinkage_func_name,
                "vCREEP_AGE": [
                    {
                        "NAME": creep_func_name,
                        "AGE": creep_age
                    }
                ]
            }
            temp = CreepShrinkage(js, id)
            self.ID = temp.ID
            self.DATA = js

#------------------------------------------ TIME DEPENDENT - COMPRESSIVE STRENGTH ----------------------------------------------------



class CompStrength:
    mats = []
    ids = []
    def __init__(self,data,id=0):
        if CompStrength.ids == []: 
            count = 1
        else:
            count = max(CompStrength.ids)+1
        if id == 0 or id in CompStrength.ids: self.ID = count
        if id!= 0 and id not in CompStrength.ids: self.ID = id

        self.DATA = data

        CompStrength.mats.append(self)
        CompStrength.ids.append(self.ID)
    
    @classmethod
    def json(cls):
        json = {"Assign":{}}
        for k in cls.mats:
            json["Assign"][k.ID]=k.DATA
        return json
    
    @staticmethod
    def create():
        MidasAPI("PUT","/db/TDME",CompStrength.json())
        
    @staticmethod
    def get():
        return MidasAPI("GET","/db/TDME")
    
    @staticmethod
    def delete():
        MidasAPI("DELETE","/db/TDME")
        CompStrength.mats=[]
        CompStrength.ids=[]

    @staticmethod
    def sync():
        a = CompStrength.get()
        if a != {'message': ''}:
            if list(a['TDME'].keys()) != []:
                CompStrength.mats = []
                CompStrength.ids=[]
                for j in a['TDME'].keys():
                    CompStrength(a['TDME'][j], int(j))


    # ---------------------------------  IRC Compressive Strength --------------------------------------------------------------

    class IRC:
        def __init__(self, name: str, code_year: int = 2020,
                     fck_delta: float = 0, cement_type: int = 1,
                     aggregate_type: int = 0, id: int = 0):
            """
            IRC Compressive Strength for Indian Road Congress standards.

            Parameters:
                name (str): Name 
                code_year (int, optional): Year of the IRC standard. Can be 2020, 2011, or 2000. Defaults to 2020.
                fck_delta (float): 28-day characteristic compressive strength
                cement_type (int, optional): Type of cement used. 
                    • 1: Slow setting (default)
                    • 2: Normal 
                    • 3: Rapid hardening
                aggregate_type (int, optional): Type of aggregate used (for IRC:112 only).
                    • 0: Basalt, dense limestone (default)
                    • 1: Quartzite 
                    • 2: Limestone 
                    • 3: Sandstone
                id (int, optional): Unique identifier. Auto-generated if not specified.

            Examples:
                ```python
                # IRC 112-2020 with normal cement
                CompStrength.IRC("C30_IRC2020", code_year=2020, fck_delta=30000, cement_type=2)

                # IRC 18-2000 standard
                CompStrength.IRC("C25_IRC2000", code_year=2000, fck_delta=25000)

                # IRC 112-2011 with rapid hardening cement and quartzite aggregate
                CompStrength.IRC("C40_IRC2011", code_year=2011, fck_delta=40000, cement_type=3, aggregate_type=1)
                ```
            """
            # Determine the code name string based on the integer year
            if code_year == 2011:
                code_name = "INDIA(IRC:112-2011)"
            elif code_year == 2000:
                code_name = "INDIA(IRC:18-2000)"
            else: # Default to 2020
                code_name = "INDIA(IRC:112-2020)"

            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": code_name,
                "STRENGTH": fck_delta
            }

            # Add cement and aggregate types for IRC:112 standards
            if code_year in [2020, 2011]:
                js["iCTYPE"] = cement_type
                js["nAGGRE"] = aggregate_type

            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js


    # ---------------------------------  ACI Compressive Strength --------------------------------------------------------------

    class ACI:
        def __init__(self, name: str, fck: float = 0, factor_a: float = 1, 
                     factor_b: float = 2, id: int = 0):
            """
            ACI Compressive Strength for American Concrete Institute standards.
            
            Parameters:
                name: Name
                fck: Compression strength (number) - 28-day compressive strength
                factor_a: Factor a (number) - ACI model parameter A (default 1)
                factor_b: Factor b (number) - ACI model parameter B (default 2)
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                # Standard ACI material
                CompStrength.ACI("C30_ACI", 30000, 1, 2)
                
                # Custom factors
                CompStrength.ACI("C25_ACI_Custom", 25000, 1.2, 1.8)
                ```
            """
            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": "ACI",
                "STRENGTH": fck,
                "A": factor_a,
                "B": factor_b
            }
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js


    # ---------------------------------  CEB-FIP Compressive Strength --------------------------------------------------------------

    class CEB_FIP:
        def __init__(self, name: str, code_year: int = 2010, fck: float = 0, 
                     cement_type: int = 1, aggregate_type: int = 0, id: int = 0):
            """
            CEB-FIP Compressive Strength for European concrete standards.
            
            Parameters:
                name: Name
                code_year: Code year (integer) - Year of the CEB-FIP standard
                    • 1978 - CEB-FIP(1978)
                    • 1990 - CEB-FIP(1990) 
                    • 2010 - CEB-FIP(2010) (default)
                fck: Compression strength (number) - 28-day compressive strength
                cement_type: Cement type (integer) - Type of cement (for 1990 and 2010)
                    • 1 - RS: 0.2 / 42.5 R, 52.5 N, 52.5 R: 0.20 (default)
                    • 2 - N, R: 0.25 / 32.5 R, 42.5 N: 0.25
                    • 3 - SL: 0.38 / 32.5 N: 0.38
                aggregate_type: Aggregate type (integer) - Type of aggregate (for 2010 only)
                    • 0 - Basalt, dense limestone aggregates (1.2): 0 (default)
                    • 1 - Quartzite aggregates: 1
                    • 2 - Limestone aggregates: 2
                    • 3 - Sandstone aggregates: 3
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                # CEB-FIP 2010 with normal cement and basalt aggregate
                CompStrength.CEB_FIP("C30_CEBFIP2010", 2010, 30000, 1, 0)
                
                # CEB-FIP 1990 with slow setting cement
                CompStrength.CEB_FIP("C25_CEBFIP1990", 1990, 25000, 3)
                
                # CEB-FIP 1978 (no cement/aggregate type)
                CompStrength.CEB_FIP("C40_CEBFIP1978", 1978, 40000)
                ```
            """
            # Determine code name based on year
            if code_year == 1978:
                code_name = "CEB-FIP(1978)"
            elif code_year == 1990:
                code_name = "CEB-FIP(1990)"
            else:  # Default to 2010
                code_name = "CEB-FIP(2010)"
            
            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": code_name,
                "STRENGTH": fck
            }
            
            # Add cement type for 1990 and 2010
            if code_year in [1990, 2010]:
                js["iCTYPE"] = cement_type
                
            # Add aggregate type for 2010 only
            if code_year == 2010:
                js["nAGGRE"] = aggregate_type
                
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js


    # ---------------------------------  Ohzagi Compressive Strength --------------------------------------------------------------

    class Ohzagi:
        def __init__(self, name: str, fck: float = 0, cement_type: int = 2, id: int = 0):
            """
            Ohzagi Compressive Strength model.
            
            Parameters:
                name: Name
                fck: Compression strength (number) - 28-day compressive strength
                cement_type: Cement type (integer) - Type of cement used
                    • 1 - RS
                    • 2 - N, R (default)
                    • 3 - SL
                    • 4 - Fly-ash
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                # Standard Ohzagi material with N,R cement
                CompStrength.Ohzagi("C30_Ohzagi", 30000, 2)
                
                # Fly-ash cement type
                CompStrength.Ohzagi("C25_Ohzagi_FA", 25000, 4)
                ```
            """
            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": "Ohzagi",
                "STRENGTH": fck,
                "iCTYPE": cement_type
            }
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js


    # ---------------------------------  European Compressive Strength --------------------------------------------------------------

    class European:
        def __init__(self, name: str, fck: float = 0, cement_type: int = 2, id: int = 0):
            """
            European Compressive Strength model.
            
            Parameters:
                name: Name
                fck: Compression strength (number) - 28-day compressive strength
                cement_type: Cement type (integer) - Cement class type
                    • 1 - Class R: 0.20
                    • 2 - Class N: 0.25 (default)
                    • 3 - Class S: 0.38
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                # European standard with Class N cement
                CompStrength.European("C30_Euro", 30000, 2)
                
                # High early strength with Class R cement
                CompStrength.European("C40_Euro_R", 40000, 1)
                ```
            """
            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": "EUROPEAN",
                "STRENGTH": fck,
                "iCTYPE": cement_type
            }
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js


    # ---------------------------------  Russian Compressive Strength --------------------------------------------------------------

    class Russian:
        def __init__(self, name: str, fck: float = 0, cement_type: int = 1, 
                     curing_method: int = 1, concrete_type: int = 1, 
                     max_aggregate_size: float = 0.02, specific_cement_content: float = 0.25, 
                     id: int = 0):
            """
            Russian Compressive Strength model.
            
            Parameters:
                name: Name
                fck: Compression strength (number) - 28-day compressive strength
                cement_type: Cement type (integer) - Type of cement
                    • 1 - Normal (default)
                    • 2 - Fast-hardened
                    • 3 - Slag
                    • 4 - Pozzolan
                curing_method: Curing method (integer) - Method of curing
                    • 0 - Natural cure: 0
                    • 1 - Steam cure: 1 (default)
                concrete_type: Concrete type (integer) - Type of concrete
                    • 0 - Heavy concrete: 0
                    • 1 - Fine-grained concrete: 1 (default)
                max_aggregate_size: Maximum aggregate size (number) - Maximum size in meters (default 0.02)
                specific_cement_content: Specific content of cement paste (number) - Content ratio (default 0)
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                # Standard Russian concrete
                CompStrength.Russian("C30_RU", 30000, 1, 1, 1, 0.02, 0)
                
                # Fast-hardened cement with natural curing
                CompStrength.Russian("C25_RU_FH", 25000, 2, 0, 0, 0.025, 0)
                ```
            """
            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": "RUSSIAN",
                "STRENGTH": fck,
                "iCTYPE": cement_type,
                "CMETH": curing_method,
                "CTYPE": concrete_type,
                "MAXS": max_aggregate_size,
                "PZ": specific_cement_content
            }
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js


    # ---------------------------------  Australian Standards Compressive Strength --------------------------------------------------------------
#add EXPOSURE
    class AS:
        def __init__(self, name: str, standard: str = "AS5100.5-2017", fck: float = 0, id: int = 0):
            """
            Australian Standards Compressive Strength model.
            
            Parameters:
                name: Name
                standard: Standard code (string) - Australian standard specification
                    • "AS5100.5-2017" - AS 5100.5-2017 (default)
                    • "AS5100.5-2016" - AS 5100.5-2016
                    • "AS/RTA5100.5-2011" - AS/RTA 5100.5-2011
                    • "AS3600-2009" - AS 3600-2009
                fck: Compression strength (number) - 28-day compressive strength
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                # AS 5100.5-2017 standard
                CompStrength.AS("C30_AS2017", "AS 5100.5-2017", 30000)
                
                # AS 3600-2009 standard
                CompStrength.AS("C25_AS3600", "AS 3600-2009", 25000)
                ```
            """
            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": standard,
                "STRENGTH": fck
            }
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js


    # ---------------------------------  Gilbert and Ranzi Compressive Strength --------------------------------------------------------------

    class GilbertRanzi:
        def __init__(self, name: str, fck: float = 0, cement_type: int = 1, 
                     density: float = 230, id: int = 0):
            """
            Gilbert and Ranzi Compressive Strength model.
            
            Parameters:
                name: Name
                fck: Compression strength (number) - 28-day compressive strength
                cement_type: Cement type (integer) - Type of cement
                    • 1 - Ordinary Portland cement: 0.38 (default)
                    • 2 - High early strength cement: 0.25
                density: Weight density (number) - Density in kg/m³ (default 230)
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                # Standard Gilbert-Ranzi model
                CompStrength.GilbertRanzi("C30_GR", 30000, 1, 2400)
                
                # High early strength cement
                CompStrength.GilbertRanzi("C40_GR_HES", 40000, 2, 2450)
                ```
            """
            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": "GILBERT AND RANZI",
                "STRENGTH": fck,
                "iCTYPE": cement_type,
                "DENSITY": density
            }
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js


    # ---------------------------------  Japan Hydration Compressive Strength --------------------------------------------------------------

    class JapanHydration:
        def __init__(self, name: str, fck: float = 0, cement_type: int = 1, 
                     use_concrete_data: bool = True, tensile_strength_factor: float = 3,
                     factor_a: float = 4.5, factor_b: float = 0.95, factor_d: float = 1.11,
                     id: int = 0):
            """
            Japan Hydration Compressive Strength model.
            
            Parameters:
                name: Name
                fck: Compression strength (number) - 28-day compressive strength
                cement_type: Cement type (integer) - Type of cement
                    • 0 - Normal Portland cement
                    • 1 - Moderate Portland cement (default)
                    • 2 - High-early-strength Portland cement
                use_concrete_data: Use concrete data option (boolean) - Enable concrete data option
                    • True - Use concrete data (default)
                    • False - Use custom factors
                tensile_strength_factor: Tensile strength factor (number) - Factor for tensile strength (default 3)
                factor_a: Factor a (number) - Model parameter A (default 4.5, used when use_concrete_data=False)
                factor_b: Factor b (number) - Model parameter B (default 0.95, used when use_concrete_data=False)
                factor_d: Factor d (number) - Model parameter D (default 1.11, used when use_concrete_data=False)
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                # Standard Japan hydration with concrete data
                CompStrength.JapanHydration("C30_JH", 30000, 1, True, 3)
                
                # Custom factors without concrete data
                CompStrength.JapanHydration("C25_JH_Custom", 25000, 0, False, 3, 4.0, 0.9, 1.0)
                ```
            """
            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": "Japan(hydration)",
                "STRENGTH": fck,
                "iCTYPE": cement_type,
                "bUSE": use_concrete_data,
                "TENS_STRN_FACTOR": tensile_strength_factor
            }
            
            # Add custom factors if not using concrete data
            if not use_concrete_data:
                js.update({
                    "A": factor_a,
                    "B": factor_b,
                    "D": factor_d
                })
                
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js


    # ---------------------------------  Japan Elastic Compressive Strength --------------------------------------------------------------

    class JapanElastic:
        def __init__(self, name: str, fck: float = 0, elastic_cement_type: int = 0, id: int = 0):
            """
            Japan Elastic Compressive Strength model.
            
            Parameters:
                name: Name
                fck: Compression strength (number) - 28-day compressive strength
                elastic_cement_type: Elastic cement type (integer) - Type of cement for elastic model
                    • 0 - Normal type: 0 (default)
                    • 1 - Rapid type: 1
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                # Normal type cement
                CompStrength.JapanElastic("C30_JE", 30000, 0)
                
                # Rapid type cement
                CompStrength.JapanElastic("C40_JE_Rapid", 40000, 1)
                ```
            """
            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": "Japan(elastic)",
                "STRENGTH": fck,
                "iECTYPE": elastic_cement_type
            }
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js


    # ---------------------------------  KDS-2016 Compressive Strength --------------------------------------------------------------

    class KDS:
        def __init__(self, name: str, fck: float = 0, cement_type: int = 1, 
                     density: float = 230, id: int = 0):
            """
            KDS-2016 Compressive Strength model.
            
            Parameters:
                name: Name
                fck: Compression strength (number) - 28-day compressive strength 
                cement_type: Cement type (integer) - Type of cement
                    • 1 - N,R moist cured: 0.35 (default)
                    • 2 - N,R steam cured: 0.15
                    • 3 - RS moist cured: 0.25
                    • 4 - RS steam cured: 0.12
                    • 5 - SL: 0.40
                density: Weight density (number) - Density in kg/m³ (default 230)
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                # Standard KDS with N,R moist cured cement
                CompStrength.KDS("C30_KDS", 30000, 1, 2400)
                
                # Steam cured cement
                CompStrength.KDS("C25_KDS_Steam", 25000, 2, 2350)
                ```
            """
            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": "KDS-2016",
                "STRENGTH": fck,
                "iCTYPE": cement_type,
                "DENSITY": density
            }
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js

    # ---------------------------------  KCI-USD12 Compressive Strength --------------------------------------------------------------

    class KCI:
        def __init__(self, name: str, fck: float = 0, cement_type: int = 1, 
                     id: int = 0):
            """
            KDS-2016 Compressive Strength model.
            
            Parameters:
                name: Name
                fck: Compression strength (number) - 28-day compressive strength 
                cement_type: Cement type (integer) - Type of cement
                    • 1 - N,R moist cured: 0.35 (default)
                    • 2 - N,R steam cured: 0.15
                    • 3 - RS moist cured: 0.25
                    • 4 - RS steam cured: 0.12
                    • 5 - SL: 0.40
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                CompStrength.KCI("C30_KCI", 30000, 1)
                
                ```
            """
            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": "KCI-USD12",
                "STRENGTH": fck,
                "iCTYPE": cement_type,
                
            }
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js
    # ---------------------------------  Korean Standard Compressive Strength --------------------------------------------------------------

    class KoreanStandard:
        def __init__(self, name: str, fck: float = 0, factor_a: float = 1, 
                     factor_b: float = 2, id: int = 0):
            """
            Korean Standard Compressive Strength model.
            
            Parameters:
                name: Material name (string) - Name identifier for the material
                fck: Compression strength (number) - 28-day compressive strength
                factor_a: Factor a (number) - Model parameter A (default 1)
                factor_b: Factor b (number) - Model parameter B (default 2)
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                # Standard Korean model
                CompStrength.KoreanStandard("C30_KS", 30000, 1, 2)
                
                # Custom factors
                CompStrength.KoreanStandard("C25_KS_Custom", 25000, 1.1, 1.8)
                ```
            """
            js = {
                "NAME": name,
                "TYPE": "CODE",
                "CODENAME": "KoreanStandard",
                "STRENGTH": fck,
                "A": factor_a,
                "B": factor_b
            }
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js


    # ---------------------------------  User Defined Compressive Strength --------------------------------------------------------------

    class UserDefined:
        def __init__(self, name: str, scale_factor: float = 1, 
                     time_data: list = None, id: int = 0):
            """
            User Defined Compressive Strength model.
            
            Parameters:
                name: Material name (string) - Name identifier for the material
                scale_factor: Scale factor (number) - Scaling factor for the data (default 1)
                time_data: Function data (list of objects) - Time-dependent strength data
                    Each object should contain:
                    • TIME - Time in days (number)
                    • COMP - Compression strength (number)
                    • TENS - Tensile strength  (number)
                    • ELAST - Elastic modulus (number)
                id: Unique identifier (integer) - Auto-generated if not specified
            
            Examples:
                ```python
                # User defined with custom time data
                time_points = [
                    {"TIME": 0, "COMP": 0, "TENS": 0, "ELAST": 0},
                    {"TIME": 7, "COMP": 20000, "TENS": 800, "ELAST": 25000000},
                    {"TIME": 28, "COMP": 30000, "TENS": 1000, "ELAST": 30000000},
                    {"TIME": 90, "COMP": 35000, "TENS": 1200, "ELAST": 32000000}
                ]
                CompStrength.UserDefined("C30_User", 1.0, time_points)
                
                # Simple default case
                CompStrength.UserDefined("C25_User_Simple", 1.2)
                ```
            """
            if time_data is None:
                time_data = [
                    {"TIME": 0, "COMP": 0, "TENS": 0, "ELAST": 0},
                    {"TIME": 1000, "COMP": 30000, "TENS": 1000, "ELAST": 3000000}
                ]
            
            js = {
                "NAME": name,
                "TYPE": "USER",
                "SCALE": scale_factor,
                "aDATA": time_data
            }
            temp = CompStrength(js, id)
            self.ID = temp.ID
            self.DATA = js

#------------------------------------------ TIME DEPENDENT - MATERIAL LINK  ----------------------------------------------------



class TDMatLink:
    mats = {}
    def __init__(self,matID,CnSName='',CompName=''):

        TDMatLink.mats[str(matID)]={
            "TDMT_NAME": CnSName,
            "TDME_NAME": CompName
        }
    
    @classmethod
    def json(cls):
        json = {"Assign": TDMatLink.mats}
        return json
    
    @staticmethod
    def create():
        MidasAPI("PUT","/db/TMAT",TDMatLink.json())
        
    @staticmethod
    def get():
        return MidasAPI("GET","/db/TMAT")
    
    
    @staticmethod
    def delete():
        MidasAPI("DELETE","/db/TMAT")
        TDMatLink.mats={}

    @staticmethod
    def clear():
        TDMatLink.mats={}

    @staticmethod
    def sync():
        a = TDMatLink.get()
        if a != {'message': ''}:
            if list(a['TMAT'].keys()) != []:
                TDMatLink.mats = []
                TDMatLink.ids=[]
                for j in a['TMAT'].keys():
                    TDMatLink(a['TMAT'][j], int(j))

#-------------------------------------------------------------------------------------------------