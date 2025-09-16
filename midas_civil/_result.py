from ._mapi import *
from ._model import *


#28 Class to generate load combinations
class LoadCombination:
    data = []
    valid = ["General", "Steel", "Concrete", "SRC", "Composite Steel Girder", "Seismic", "All"]
    com_map = {
            "General": "/db/LCOM-GEN",
            "Steel": "/db/LCOM-STEEL",
            "Concrete": "/db/LCOM-CONC",
            "SRC": "/db/LCOM-SRC",
            "Composite Steel Girder": "/db/LCOM-STLCOMP",
            "Seismic": "/db/LCOM-SEISMIC"
        }
    def __init__(self, name, case, classification = "General", active = "ACTIVE", typ = "Add", id = 0, desc = ""):
        """Name, List of tuple of load cases & factors, classification, active, type. \n
        Sample: LoadCombination('LCB1', [('Dead Load(CS)',1.5), ('Temperature(ST)',0.9)], 'General', 'Active', 'Add')"""
        if not isinstance(case, list):
            print("case should be a list that contains tuple of load cases & factors.\nEg: [('Load1(ST)', 1.5), ('Load2(ST)',0.9)]")
            return
        for i in case:
            if not isinstance(i, tuple):
                print(f"{i} is not a tuple.  case should be a list that contains tuple of load cases & factors.\nEg: [('Load1(ST)', 1.5), ('Load2(ST)',0.9)]")
                return
            if not isinstance(i[0], str):
                print(f"{i[0]} is not a string.  case should be a list that contains tuple of load cases & factors.\nEg: [('Load1(ST)', 1.5), ('Load2(ST)',0.9)]")
                return
            if i[0][-1] != ")":
                print(f"Load case type is not mentioned for {i[0]}.  case should be a list that contains tuple of load cases & factors.\nEg: [('Load1(ST)', 1.5), ('Load2(ST)',0.9)]")
                return
            if not isinstance(i[1],(int, float)):
                print(f"{i[1]} is not a number.  case should be a list that contains tuple of load cases & factors.\nEg: [('Load1(ST)', 1.5), ('Load2(ST)',0.9)]")
                return

        if classification not in LoadCombination.valid[:-1]:
            print(f'"{classification}" is not a valid input.  It is changed to "General".')
            classification = "General"
            
        if classification in ["General", "Seismic"]:
            if active not in ["ACTIVE", "INACTIVE"]: active = "ACTIVE"
        if classification in  ["Steel", "Concrete", "SRC", "Composite Steel Girder"]:
            if active not in ["STRENGTH", "SERVICE", "INACTIVE"]: active = "STRENGTH"
        
        typ_map = {"Add": 0, "Envelope": 1, "ABS": 2, "SRSS": 3, 0:0, 1:1, 2:2, 3:3}
        if typ not in list(typ_map.keys()): typ = "Add"
        if classification not in ["General", "Seismic"] and typ_map.get(typ) == 2: typ = "Add"
        
        if id == 0 and len(LoadCombination.data) == 0: 
            id = 1
        elif id == 0 and len(LoadCombination.data) != 0:
            id = max([i.ID for i in LoadCombination.data]) + 1
        elif id != 0 and id in [i.ID for i in LoadCombination.data]:
            if classification in [i.CLS for i in LoadCombination.data if i.ID == id]:
                print(f"ID {id} is already defined.  Existing combination would be replaced.")
                
        
        combo = []
        valid_anl = ["ST", "CS", "MV", "SM", "RS", "TH", "CB", "CBC", "CBS", "CBR", "CBSC", "CBSM"] #Need to figure out for all combination types
        for i in case:
            a = i[0].rsplit('(', 1)[1].rstrip(')')
            if a in valid_anl:
                combo.append({
                    "ANAL": a,
                    "LCNAME":i[0].rsplit('(', 1)[0],
                    "FACTOR": i[1]
                })
        self.NAME = name
        self.CASE = combo
        self.CLS = classification
        self.ACT = active
        self.TYPE = typ_map.get(typ)
        self.ID = id
        self.DESC = desc
        LoadCombination.data.append(self)
    
    @classmethod
    def json(cls, classification = "All"):
        if len(LoadCombination.data) == 0:
            print("No Load Combinations defined!  Define the load combination using the 'LoadCombination' class before making json file.")
            return
        if classification not in LoadCombination.valid:
            print(f'"{classification}" is not a valid input.  It is changed to "General".')
            classification = "General"
        json = {k:{'Assign':{}} for k in LoadCombination.valid[:-1]}
        for i in LoadCombination.data:
            if i.CLS == classification or classification == "All":
                json[i.CLS]['Assign'][i.ID] = {
                    "NAME": i.NAME,
                    "ACTIVE": i.ACT,
                    "iTYPE": i.TYPE,
                    "DESC": i.DESC,
                    "vCOMB":i.CASE
                }
        json = {k:v for k,v in json.items() if v != {'Assign':{}}}
        return json
    
    @classmethod
    def get(cls, classification = "All"):
        if classification not in LoadCombination.valid:
            print(f'"{classification}" is not a valid input.  It is changed to "General".')
            classification = "General"
        combos = {k:{} for k in LoadCombination.valid[:-1]}
        for i in LoadCombination.valid[:-1]:
            if classification == i or classification == "All":
                combos[i] = MidasAPI("GET",LoadCombination.com_map.get(i))
        json = {k:v for k,v in combos.items() if v != {'message':''}}
        return json
    
    @classmethod
    def create(cls, classification = "All"):
        if len(LoadCombination.data) == 0:
            # print("No Load Combinations defined!  Define the load combination using the 'LoadCombination' class before creating these in the model.")
            return
        if classification not in LoadCombination.valid:
            print(f'"{classification}" is not a valid input.  It is changed to "General".')
            classification = "General"
        json = LoadCombination.json(classification)
        for i in LoadCombination.valid[:-1]:
            if classification == i or classification == "All":
                if i in list(json.keys()):
                    a = list(json[i]['Assign'].keys())
                    b=""
                    for j in range(len(a)):
                        b += str(a[j]) + ","
                    if b != "": b = "/" + b[:-1]
                    MidasAPI("DELETE", LoadCombination.com_map.get(i) + b)     #Delete existing combination if any
                    MidasAPI("PUT", LoadCombination.com_map.get(i), json[i])   #Create new combination
    
    @classmethod
    def sync(cls, classification = "All"):
        json = LoadCombination.get(classification)
        if json != {}:
            keys = list(json.keys())
            for i in keys:
                for k,v in json[i][LoadCombination.com_map.get(i)[4:]].items():
                    c = []
                    for j in range(len(v['vCOMB'])):
                        c.append((v['vCOMB'][j]['LCNAME'] + "("+ v['vCOMB'][j]['ANAL'] + ")", v['vCOMB'][j]['FACTOR']))
                    LoadCombination(v['NAME'], c, i, v['ACTIVE'], v['iTYPE'], int(k), v['DESC'])
    
    @classmethod
    def delete(cls, classification = "All", ids = []):
        json = LoadCombination.json(classification)
        a = ""
        for i in range(len(ids)):
            a += str(ids[i]) + ","
        a = "/" + a[:-1]
        if json == {}: 
            print("No load combinations are defined to delete.")
        for i in list(json.keys()):
            MidasAPI("DELETE",LoadCombination.com_map.get(i) + a)
#---------------------------------------------------------------------------------------------------------------