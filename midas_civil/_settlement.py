from ._mapi import *

class Settlement:
    
    @classmethod
    def create(cls):
        """Creates Settlement Load in MIDAS Civil NX"""
        if cls.Group.data != []: cls.Group.create()
        if cls.Case.data != []: cls.Case.create()
    
    @classmethod
    def delete(cls):
        """Deletes Settlement load from MIDAS Civil NX and Python"""
        cls.Group.delete()
        cls.Case.delete()
    
    @classmethod
    def sync(cls):
        """Sync Settlement load from MIDAS Civil NX to Python"""
        cls.Group.sync()
        cls.Case.sync()
    
    class Group:
        """ 
        Parameters:
            name: Settlement group name (string)
            displacement: Settlement displacement value (number)
            node_list: List of node IDs to include in the group (array of integers)
            id: Group ID (optional, auto-generated if not provided)
        
        Examples:
            ```python
            Settlement.Group("SG1", 0.025, [100, 101])
            Settlement.Group("SG2", 0.015, [102, 103])
            ```
        """
        data = []

        def __init__(self, name, displacement, node_list, id=""):
            self.NAME = name
            self.SETTLE = displacement
            self.ITEMS = node_list
            if id == "": id = len(Settlement.Group.data) + 1
            self.ID = id
            
            Settlement.Group.data.append(self)

        @classmethod
        def json(cls):
            json = {"Assign": {}}
            for i in cls.data:
                json["Assign"][str(i.ID)] = {
                    "NAME": i.NAME,
                    "SETTLE": i.SETTLE,
                    "ITEMS": i.ITEMS
                }
            return json
        
        @staticmethod
        def create():
            MidasAPI("PUT", "/db/smpt", Settlement.Group.json())
        
        @staticmethod
        def get():
            return MidasAPI("GET", "/db/smpt")
        
        @classmethod
        def delete(cls):
            cls.data = []
            return MidasAPI("DELETE", "/db/smpt")
        
        @classmethod
        def sync(cls):
            cls.data = []
            a = cls.get()
            if a != {'message': ''}:
                for i in a['SMPT'].keys():
                    Settlement.Group(
                        a['SMPT'][i]['NAME'], 
                        a['SMPT'][i]['SETTLE'], 
                        a['SMPT'][i]['ITEMS'],
                        int(i)
                    )

    
    class Case:
        """
        
        Parameters:
            name: Settlement load case name (string)
            settlement_groups: List of settlement group names to include (array of strings, default [])
            factor: Settlement scale factor (number, default 1.0)
            min_groups: Minimum number of settlement groups (integer, default 1)
            max_groups: Maximum number of settlement groups (integer, default 1)
            desc: Description of the settlement case (string, default "")
            id: Case ID (optional, auto-generated if not provided)
        
        Examples:
            ```python
            Settlement.Case("SMLC1", ["SG1"], 1.2, 1, 1, "Foundation Settlement Case")
            Settlement.Case("SMLC2", ["SG1", "SG2"], 1.0, 1, 2, "Combined Settlement")
            ```
        """
        data = []

        def __init__(self, name, settlement_groups=[],factor=1.0, min_groups=1, max_groups=1, desc="", id=""):
            self.NAME = name
            self.DESC = desc
            self.FACTOR = factor
            self.MIN = min_groups
            self.MAX = max_groups
            self.ST_GROUPS = settlement_groups
            if id == "": id = len(Settlement.Case.data) + 1
            self.ID = id
            
            Settlement.Case.data.append(self)

        @classmethod
        def json(cls):
            json = {"Assign": {}}
            for i in cls.data:
                json["Assign"][str(i.ID)] = {
                    "NAME": i.NAME,
                    "DESC": i.DESC,
                    "FACTOR": i.FACTOR,
                    "MIN": i.MIN,
                    "MAX": i.MAX,
                    "ST_GROUPS": i.ST_GROUPS
                }
            return json
        
        @staticmethod
        def create():
            MidasAPI("PUT", "/db/smlc", Settlement.Case.json())
        
        @staticmethod
        def get():
            return MidasAPI("GET", "/db/smlc")
        
        @classmethod
        def delete(cls):
            cls.data = []
            return MidasAPI("DELETE", "/db/smlc")
        
        @classmethod
        def sync(cls):
            cls.data = []
            a = cls.get()
            if a != {'message': ''}:
                for i in a['SMLC'].keys():
                    Settlement.Case(
                        a['SMLC'][i]['NAME'],
                        a['SMLC'][i]['DESC'], 
                        a['SMLC'][i]['FACTOR'],
                        a['SMLC'][i]['MIN'],
                        a['SMLC'][i]['MAX'],
                        a['SMLC'][i]['ST_GROUPS'],
                        int(i)
                    )
