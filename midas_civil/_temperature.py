from ._mapi import *
from ._node import *
from ._group import *

def convList(item):
    if type(item) != list:
        return [item]
    else:
        return item
    
class Temperature:

    @classmethod
    def create(cls):
        """Creates Temperature elements in MIDAS Civil NX"""
        if cls.System.temps: cls.System.create()
        if cls.Element.temps: cls.Element.create()
        if cls.Gradient.temps: cls.Gradient.create()

    @classmethod
    def delete(cls):
        """Deletes Temperature elements from MIDAS Civil NX and Python"""
        cls.System.delete()
        cls.Element.delete()
        cls.Gradient.delete()
        

    @classmethod
    def sync(cls):
        """Sync Temperature elements from MIDAS Civil NX to Python"""
        cls.System.sync()
        cls.Element.sync()
        cls.Gradient.sync()
        
    # --------------------------------------------------------------------------------------------------
    # System Temperature
    # --------------------------------------------------------------------------------------------------
    class System:
        """
        Create System Temperature Object in Python
        
        Parameters:
            temperature (float): Temperature value
            lcname (str): Load case name
            group (str): Load group name (default "")
            id (int): System ID (optional)
        
        Example:
            Temperature.System(12.5, "Temp(+)", "LoadGroup1", 1)
        """
        temps = []
        
        def __init__(self, temperature, lcname, group="", id=None):
            if group:
                chk = 0
                try:
                    a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                    if group in a:
                        chk = 1
                except:
                    pass
                if chk == 0:
                    Group.Load(group)
            
            self.TEMPER = temperature
            self.LCNAME = lcname
            self.GROUP_NAME = group
            
            if id is None:
                self.ID = len(Temperature.System.temps) + 1
            else:
                self.ID = id
            
            Temperature.System.temps.append(self)

        @classmethod
        def json(cls):
            """Creates JSON from System Temperature objects defined in Python"""
            json_data = {"Assign": {}}
            for temp in cls.temps:
                json_data["Assign"][str(temp.ID)] = {
                    "TEMPER": temp.TEMPER,
                    "LCNAME": temp.LCNAME,
                    "GROUP_NAME": temp.GROUP_NAME
                }
            return json_data

        @staticmethod
        def create():
            """Creates System Temperatures in MIDAS Civil NX"""
            MidasAPI("PUT", "/db/stmp", Temperature.System.json())

        @staticmethod
        def get():
            """Get the JSON of System Temperatures from MIDAS Civil NX"""
            return MidasAPI("GET", "/db/stmp")

        @staticmethod
        def sync():
            """Sync System Temperatures from MIDAS Civil NX to Python"""
            Temperature.System.temps = []
            a = Temperature.System.get()
            
            if a and 'STMP' in a:
                temp_data = a.get('STMP', {})
                for temp_id, temp_info in temp_data.items():
                    Temperature.System(
                        temp_info.get('TEMPER', 0),
                        temp_info.get('LCNAME', ''),
                        temp_info.get('GROUP_NAME', ''),
                        int(temp_id)
                    )

        @staticmethod
        def delete():
            """Delete System Temperatures from MIDAS Civil NX and Python"""
            Temperature.System.temps = []
            return MidasAPI("DELETE", "/db/stmp")

    # --------------------------------------------------------------------------------------------------
    # Element Temperature
    # --------------------------------------------------------------------------------------------------
    class Element:
        """
        Create Element Temperature Object in Python
        
        Parameters:
            element (int): Element ID
            temperature (float): Temperature value
            lcname (str): Load case name
            group (str): Load group name (default "")
            id (int): Temperature ID (optional)
        
        Example:
            Temperature.Element(1, 35, "Temp(+)", "", 1)
        """
        temps = []
        
        def __init__(self, element, temperature, lcname, group="", id=None):
            if group:
                chk = 0
                try:
                    a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                    if group in a:
                        chk = 1
                except:
                    pass
                if chk == 0:
                    Group.Load(group)
            
            self.ELEMENT = element
            self.TEMP = temperature
            self.LCNAME = lcname
            self.GROUP_NAME = group
            
            if id is None:
                existing_ids = []
                for temp in Temperature.Element.temps:
                    if temp.ELEMENT == element:
                        existing_ids.extend([item.get('ID', 0) for item in temp.ITEMS if hasattr(temp, 'ITEMS')])
                self.ID = max(existing_ids, default=0) + 1
            else:
                self.ID = id
            
            existing_temp = None
            for temp in Temperature.Element.temps:
                if temp.ELEMENT == element:
                    existing_temp = temp
                    break
            
            item_data = {
                "ID": self.ID, "LCNAME": self.LCNAME,
                "GROUP_NAME": self.GROUP_NAME, "TEMP": self.TEMP
            }

            if existing_temp:
                if not hasattr(existing_temp, 'ITEMS'):
                    existing_temp.ITEMS = []
                existing_temp.ITEMS.append(item_data)
            else:
                self.ITEMS = [item_data]
                Temperature.Element.temps.append(self)

        @classmethod
        def json(cls):
            """Creates JSON from Element Temperature objects defined in Python"""
            json_data = {"Assign": {}}
            for temp in cls.temps:
                json_data["Assign"][str(temp.ELEMENT)] = {"ITEMS": temp.ITEMS}
            return json_data

        @staticmethod
        def create():
            """Creates Element Temperatures in MIDAS Civil NX"""
            MidasAPI("PUT", "/db/etmp", Temperature.Element.json())

        @staticmethod
        def get():
            """Get the JSON of Element Temperatures from MIDAS Civil NX"""
            return MidasAPI("GET", "/db/etmp")

        @staticmethod
        def sync():
            """Sync Element Temperatures from MIDAS Civil NX to Python"""
            Temperature.Element.temps = []
            a = Temperature.Element.get()
            
            if a and 'ETMP' in a:
                temp_data = a.get('ETMP', {})
                for element_id, element_data in temp_data.items():
                    element_obj = type('obj', (object,), {
                        'ELEMENT': int(element_id),
                        'ITEMS': element_data.get('ITEMS', [])
                    })()
                    Temperature.Element.temps.append(element_obj)

        @staticmethod
        def delete():
            """Delete Element Temperatures from MIDAS Civil NX and Python"""
            Temperature.Element.temps = []
            return MidasAPI("DELETE", "/db/etmp")

    # --------------------------------------------------------------------------------------------------
    # Temperature Gradient
    # --------------------------------------------------------------------------------------------------
    class Gradient:
        """
        Create Temperature Gradient Object in Python for Beam and Plate elements.
        
        Parameters:
            element (int): Element ID to apply the gradient.
            type (str): Element type, either 'Beam' or 'Plate'.
            lcname (str): Load Case Name (must exist in the model).
            tz (float): Temperature difference in the local z-direction (T2z - T1z).
            group (str, optional): Load Group Name. Defaults to "".
            id (int, optional): Gradient ID. Auto-assigned if not provided.
            hz (float, optional): Gradient value for local z-dir. If omitted, section default is used.
            ty (float, optional): Temp. diff. in local y-dir (T2y - T1y). **Required for 'Beam' type.**
            hy (float, optional): Gradient value for local y-dir. If omitted, section default is used.
        
        Example for Beam (providing gradient values):
            Temperature.Gradient(element=2, type='Beam', lcname='Temp(-)', tz=10, ty=-10, hz=1.2, hy=0.5)
        
        Example for Beam (using section defaults):
            Temperature.Gradient(element=2, type='Beam', lcname='Temp(+)', tz=10, ty=-10)
        
        Example for Plate (providing gradient value):
            Temperature.Gradient(element=21, type='Plate', lcname='Temp(-)', tz=10, hz=0.2)
        """
        temps = []

        def __init__(self, element, type, lcname, tz, group="", id=None, hz=None, ty=0, hy=None):
            if group:
                chk = 0
                try:
                    a = [v['NAME'] for v in Group.Load.json()["Assign"].values()]
                    if group in a:
                        chk = 1
                except:
                    pass
                if chk == 0:
                    Group.Load(group)
            
            self.ELEMENT = element
            
            if id is None:
                existing_ids = []
                for temp in Temperature.Gradient.temps:
                    if temp.ELEMENT == element:
                        existing_ids.extend([item.get('ID', 0) for item in temp.ITEMS if hasattr(temp, 'ITEMS')])
                self.ID = max(existing_ids, default=0) + 1
            else:
                self.ID = id

            use_hz = (hz is None)
            use_hy = (hy is None)

            item_data = {
                "ID": self.ID,
                "LCNAME": lcname,
                "GROUP_NAME": group,
                "TZ": tz,
                "USE_HZ": use_hz,
            }

            if not use_hz:
                item_data["HZ"] = hz

            if type.lower() == 'beam':
                item_data["TYPE"] = 1
                item_data["TY"] = ty
                item_data["USE_HY"] = use_hy
                if not use_hy:
                    item_data["HY"] = hy
            elif type.lower() == 'plate':
                item_data["TYPE"] = 2
            else:
                raise ValueError("Element type for Gradient must be 'Beam' or 'Plate'.")

            existing_temp = None
            for temp in Temperature.Gradient.temps:
                if temp.ELEMENT == element:
                    existing_temp = temp
                    break

            if existing_temp:
                if not hasattr(existing_temp, 'ITEMS'):
                    existing_temp.ITEMS = []
                existing_temp.ITEMS.append(item_data)
            else:
                self.ITEMS = [item_data]
                Temperature.Gradient.temps.append(self)
        
        @classmethod
        def json(cls):
            """Creates JSON from Temperature Gradient objects defined in Python"""
            json_data = {"Assign": {}}
            for temp in cls.temps:
                json_data["Assign"][str(temp.ELEMENT)] = {"ITEMS": temp.ITEMS}
            return json_data

        @staticmethod
        def create():
            """Creates Temperature Gradients in MIDAS Civil NX"""
            MidasAPI("PUT", "/db/gtmp", Temperature.Gradient.json())

        @staticmethod
        def get():
            """Get the JSON of Temperature Gradients from MIDAS Civil NX"""
            return MidasAPI("GET", "/db/gtmp")

        @staticmethod
        def sync():
            """Sync Temperature Gradients from MIDAS Civil NX to Python"""
            Temperature.Gradient.temps = []
            a = Temperature.Gradient.get()
            
            if a and 'GTMP' in a:
                temp_data = a.get('GTMP', {})
                for element_id, element_data in temp_data.items():
                    element_obj = type('obj', (object,), {
                        'ELEMENT': int(element_id),
                        'ITEMS': element_data.get('ITEMS', [])
                    })()
                    Temperature.Gradient.temps.append(element_obj)

        @staticmethod
        def delete():
            """Delete Temperature Gradients from MIDAS Civil NX and Python"""
            Temperature.Gradient.temps = []
            return MidasAPI("DELETE", "/db/gtmp")

    # --------------------------------------------------------------------------------------------------
