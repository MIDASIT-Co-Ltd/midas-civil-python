from ._mapi import *
from ._model import *


#28 Class to generate load combinations
class Load_Combination:
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
        Sample: Load_Combination('LCB1', [('Dead Load(CS)',1.5), ('Temperature(ST)',0.9)], 'General', 'Active', 'Add')"""
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

        if classification not in Load_Combination.valid[:-1]:
            print(f'"{classification}" is not a valid input.  It is changed to "General".')
            classification = "General"
            
        if classification in ["General", "Seismic"]:
            if active not in ["ACTIVE", "INACTIVE"]: active = "ACTIVE"
        if classification in  ["Steel", "Concrete", "SRC", "Composite Steel Girder"]:
            if active not in ["STRENGTH", "SERVICE", "INACTIVE"]: active = "STRENGTH"
        
        typ_map = {"Add": 0, "Envelope": 1, "ABS": 2, "SRSS": 3, 0:0, 1:1, 2:2, 3:3}
        if typ not in list(typ_map.keys()): typ = "Add"
        if classification not in ["General", "Seismic"] and typ_map.get(typ) == 2: typ = "Add"
        
        if id == 0 and len(Load_Combination.data) == 0: 
            id = 1
        elif id == 0 and len(Load_Combination.data) != 0:
            id = max([i.ID for i in Load_Combination.data]) + 1
        elif id != 0 and id in [i.ID for i in Load_Combination.data]:
            if classification in [i.CLS for i in Load_Combination.data if i.ID == id]:
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
        Load_Combination.data.append(self)
    
    @classmethod
    def json(cls, classification = "All"):
        if len(Load_Combination.data) == 0:
            print("No Load Combinations defined!  Define the load combination using the 'Load_Combination' class before making json file.")
            return
        if classification not in Load_Combination.valid:
            print(f'"{classification}" is not a valid input.  It is changed to "General".')
            classification = "General"
        json = {k:{'Assign':{}} for k in Load_Combination.valid[:-1]}
        for i in Load_Combination.data:
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
        if classification not in Load_Combination.valid:
            print(f'"{classification}" is not a valid input.  It is changed to "General".')
            classification = "General"
        combos = {k:{} for k in Load_Combination.valid[:-1]}
        for i in Load_Combination.valid[:-1]:
            if classification == i or classification == "All":
                combos[i] = MidasAPI("GET",Load_Combination.com_map.get(i))
        json = {k:v for k,v in combos.items() if v != {'message':''}}
        return json
    
    @classmethod
    def create(cls, classification = "All"):
        if len(Load_Combination.data) == 0:
            print("No Load Combinations defined!  Define the load combination using the 'Load_Combination' class before creating these in the model.")
            return
        if classification not in Load_Combination.valid:
            print(f'"{classification}" is not a valid input.  It is changed to "General".')
            classification = "General"
        json = Load_Combination.json(classification)
        for i in Load_Combination.valid[:-1]:
            if classification == i or classification == "All":
                if i in list(json.keys()):
                    a = list(json[i]['Assign'].keys())
                    b=""
                    for j in range(len(a)):
                        b += str(a[j]) + ","
                    if b != "": b = "/" + b[:-1]
                    MidasAPI("DELETE", Load_Combination.com_map.get(i) + b)     #Delete existing combination if any
                    MidasAPI("PUT", Load_Combination.com_map.get(i), json[i])   #Create new combination
    
    @classmethod
    def sync(cls, classification = "All"):
        json = Load_Combination.get(classification)
        if json != {}:
            keys = list(json.keys())
            for i in keys:
                for k,v in json[i][Load_Combination.com_map.get(i)[4:]].items():
                    c = []
                    for j in range(len(v['vCOMB'])):
                        c.append((v['vCOMB'][j]['LCNAME'] + "("+ v['vCOMB'][j]['ANAL'] + ")", v['vCOMB'][j]['FACTOR']))
                    Load_Combination(v['NAME'], c, i, v['ACTIVE'], v['iTYPE'], int(k), v['DESC'])
    
    @classmethod
    def delete(cls, classification = "All", ids = []):
        json = Load_Combination.call_json(classification)
        a = ""
        for i in range(len(ids)):
            a += str(ids[i]) + ","
        a = "/" + a[:-1]
        if json == {}: 
            print("No load combinations are defined to delete.  Def")
        for i in list(json.keys()):
            MidasAPI("DELETE",Load_Combination.com_map.get(i) + a)
#---------------------------------------------------------------------------------------------------------------


#29 Beam result table (IMCOMPLETE)
class Beam_Result_Table:
    force_input_data = []
    stress_input_data = []
    
    def __init__(self, table_of = "FORCE", elem = [], case = [], cs = False, stage = [], step = [], location = "i"):
        if table_of in ["FORCE", "STRESS"]:
            self.TAB = table_of
        else:
            print(f"Please enter 'FORCE' or 'STRESS' as string in capital. {table_of} is not a vaild input.")
            return
        Element.update_class()
        if elem != []:
            a = [i.ID for i in Element.elements if i.ID in elem and i.TYPE == "BEAM"]
            b = [i for i in elem if i not in a]
            elem = a
            if b != []: print(f"The element/s {b} are not defined in the model.  These would be skipped.")
        if elem == []: 
            print(f"Since no valid elements were provided, table is generated for all defined beam elements.")
            elem = [i.ID for i in Element.elements if i.TYPE == "BEAM"]
        self.ELEM = elem
        Load_Case.update_class()
        Load_Combination.update_class()
        ca = Load_Case.make_json()
        co = Load_Combination.make_json()
        if case == [] and cs == False:
            print(f"Since no load cases/combinations are provided for output, results are tabulated for all static load cases.")
            for i in ca["Assign"]:
                case.append(ca["Assign"][i]["NAME"]+"(ST)")
        if case != []:
            for i in range(len(case)):
                if case[i][-1] != ")": 
                    case[i]+="(ST)"
        self.CASE = case
        if location not in ["i", "1/4", "2/4", "3/4", "j"]:
            print(f'{location} not in ["i", "1/4", "2/4", "3/4", "j"]. Output is tablulated for "i" location.')
            location = "i"
        self.LOC = location
        if table_of == "FORCE":
            Beam_Result_Table.force_input_data.append(self)
        elif table_of == "STRESS":
            Beam_Result_Table.stress_input_data.append(self)
        
    @classmethod
    def make_json(cls, json_of = "FORCE"):
        Model.analyse()
        if json_of == "FORCE":1
            
#---------------------------------------------------------------------------------------------------------------

#Function to get stress table JSON output, just the DATA list.
def stress_tab(elem, case):
    """Element list.  Sample stress_tab([3,5], "Self-Weight(ST)").  Returns Cb1 to Cb4 for list of entered elements"""
    if elem == None: elem = list(MidasAPI("GET","/db/ELEM")['ELEM'].keys())
    if case == None: 
        a = MidasAPI("GET","/db/STLD")['STLD']
        for i in range(max(list(a.keys()))):
            if a[i]['TYPE'] not in ['CS']: case.append(str(a[i]["NAME"])+"(ST)")
    stress = {"Argument": {
                "TABLE_NAME": "BeamStress",
                "TABLE_TYPE": "BEAMSTRESS",
                "UNIT": {
                    "FORCE": "N",
                    "DIST": "mm"
                },
                "STYLES": {
                    "FORMAT": "Fixed",
                    "PLACE": 12
                },
                "COMPONENTS": [
                    "Elem",
                    "Load",
                    "Part",
                    "Cb1(-y+z)",
                    "Cb2(+y+z)",
                    "Cb3(+y-z)",
                    "Cb4(-y-z)"
                ],
                "NODE_ELEMS": {
                    "KEYS": [
                        int(item) for item in elem
                    ]
                },
                "LOAD_CASE_NAMES": case,
                "PARTS": [
                    "PartI",
                    "Part1/4",
                    "Part2/4",
                    "Part3/4",
                    "PartJ"
                ]
            }}
    raw = (MidasAPI("POST","/post/TABLE",stress)['BeamStress']['DATA'])
    return(raw)
#---------------------------------------------------------------------------------------------------------------
#Function to call max beam stress results
def max_beam_stress(elem, case):
    """Element list.  Sample:  max_beam_stress([10,18,5], "Self-Weight(ST)") to get maximum stress among these 3 elements.
    Enter max_beam_stress([],[]) to get maximum stress in the entire structure for the first static load case."""
    db = 0
    if elem == None: elem = list(MidasAPI("GET","/db/ELEM")['ELEM'].keys())
    if case == None: 
        for i in range(max(list(MidasAPI("GET","/db/STLD")['STLD'].keys()))):
            case.append(str(MidasAPI("GET","/db/STLD")['STLD'][i]["NAME"])+"(ST)")
    if type(elem == list):
        for i in range(len(elem)):
            if type(elem[i])!= int: db+=1
        if db == 0:
            raw = stress_tab(elem, case)
            current_stress = float(0)
            for i in range(len(raw)):
                max_stress = max(current_stress, float(raw[i][4]),float(raw[i][5]),float(raw[i][6]),float(raw[i][7]))
                current_stress = max_stress
            return(current_stress)
        if db!= 0: print("Enter list of element ID (list of integers only!)")
    if type(elem)!= list: print("Enter list of element ID (list of integers only!) or leave it empty for max stress in structure.")
#---------------------------------------------------------------------------------------------------------------
#Function to call min beam stress results
def min_beam_stress(elem, case):
    """Element list, Load case name or combination.  Sample:  min_beam_stress([10,18,5], ["Self-Weight(ST)"]) to get minimum stress among these 3 elements.
    Enter min_beam_stress([],[]) to get minimum stress in the entire structure for the first static load case."""
    db = 0
    if elem == None: elem = list(MidasAPI("GET","/db/ELEM")['ELEM'].keys())
    if case == None: 
        for i in range(max(list(MidasAPI("GET","/db/STLD")['STLD'].keys()))):
            case.append(str(MidasAPI("GET","/db/STLD")['STLD'][i]["NAME"])+"(ST)")
    if type(elem == list):
        for i in range(len(elem)):
            if type(elem[i])!= int: db+=1
        if db == 0:
            raw = stress_tab(elem, case)
            current_stress = float(0)
            for i in range(len(raw)):
                min_stress = min(current_stress, float(raw[i][4]),float(raw[i][5]),float(raw[i][6]),float(raw[i][7]))
                current_stress = min_stress
            return(current_stress)
        if db!= 0: print("Enter list of element ID (list of integers only!)")
    if type(elem)!= list: print("Enter list of element ID (list of integers only!) or leave it empty for min stress in structure.")
#---------------------------------------------------------------------------------------------------------------
#Function to get force table JSON output, just the DATA list.
def force_tab(elem, case):
    """Element list.  Sample force_tab([23,5]).  Returns element forces for list of entered elements"""
    if elem == None: elem = list(MidasAPI("GET","/db/ELEM")['ELEM'].keys())
    if case == None: 
        for i in range(max(list(MidasAPI("GET","/db/STLD")['STLD'].keys()))):
            case.append(str(MidasAPI("GET","/db/STLD")['STLD'][i]["NAME"])+"(ST)")
    force = {
        "Argument": {
            "TABLE_NAME": "BeamForce",
            "TABLE_TYPE": "BEAMFORCE",
            "EXPORT_PATH": "C:\\MIDAS\\Result\\Output.JSON",
            "UNIT": {
                "FORCE": "kN",
                "DIST": "m"
            },
            "STYLES": {
                "FORMAT": "Fixed",
                "PLACE": 12
            },
            "COMPONENTS": [
                "Elem",
                "Load",
                "Part",
                "Axial",
                "Shear-y",
                "Shear-z",
                "Torsion",
                "Moment-y",
                "Moment-z",
                "Bi-Moment",
                "T-Moment",
                "W-Moment"
            ],
            "NODE_ELEMS": {
                "KEYS": [
                    int(item) for item in elem
                ]
            },
            "LOAD_CASE_NAMES": case,
            "PARTS": [
                "PartI",
                "Part1/4",
                "Part2/4",
                "Part3/4",
                "PartJ"
            ]
        }
    }
    raw = (MidasAPI("POST","/post/TABLE",force)['BeamForce']['DATA'])
    return(raw)
#---------------------------------------------------------------------------------------------------------------
#Function to call beam force results
def beam_force(req = 3, elem = [], case = [], loc = 1):
    """Request, Element list, Case list, Location.  Sample:  beam_force(elem=[10,18,5], case ="Self-Weight(ST)") to get forces at I end in these 3 elements.
    req = (1 --> Maximum force)(2 --> Minimum force)(3 --> Forces for all elements at requested location).
    loc = (1 --> i-end)(2 --> Part1/2)(3 --> Part2/4)(4 --> Part3/4)(5 --> j end)  
    Enter beam_force() to get forces at I end in all elements for all load cases."""
    db = 0
    dir = {"Axial":float(0),
        "Shear-y":float(0),
        "Shear-z":float(0),
        "Torsion":float(0),
        "Moment-y":float(0),
        "Moment-z":float(0),
        "Bi-Moment":float(0),
        "T-Moment":float(0),
        "W-Moment":float(0)}
    dir_2 = {
        "Axial":[],
        "Shear-y":[],
        "Shear-z":[],
        "Torsion":[],
        "Moment-y":[],
        "Moment-z":[],
        "Bi-Moment":[],
        "T-Moment":[],
        "W-Moment":[]}
    if elem == []: elem = [int(item) for item in list(MidasAPI("GET","/db/ELEM")['ELEM'].keys())]
    if case == []: 
        a = MidasAPI("GET","/db/STLD")['STLD']
        for i in range(int(max(list(a.keys())))):
            if a[str(i+1)]['TYPE'] not in ['CS']: case.append(str(a[str(i+1)]["NAME"])+"(ST)")
    if type(elem == list):
        for i in range(len(elem)):
            if type(elem[i])!= int: db+=1
        if (db == 0):
            raw = force_tab(elem, case)
            for i in range(len(raw)):
                if req == 1:
                    dir["Axial"] = max(dir["Axial"], float(raw[i][4]))
                    dir["Shear-y"] = max(dir["Shear-y"],float(raw[i][5]))
                    dir["Shear-z"] = max(dir["Shear-z"],float(raw[i][6]))
                    dir["Torsion"] = max(dir["Torsion"],float(raw[i][7]))
                    dir["Moment-y"] = max(dir["Moment-y"],float(raw[i][8]))
                    dir["Moment-z"] = max(dir["Moment-z"],float(raw[i][9]))
                    if len(raw[0])>10:
                        dir["Bi-Moment"] = max(dir["Bi-Moment"],float(raw[i][10]))
                        dir["T-Moment"] = max(dir["T-Moment"],float(raw[i][11]))
                        dir["W-Moment"] = max(dir["W-Moment"],float(raw[i][12]))
                if req == 2:
                    dir["Axial"] = min(dir["Axial"], float(raw[i][4]))
                    dir["Shear-y"] = min(dir["Shear-y"],float(raw[i][5]))
                    dir["Shear-z"] = min(dir["Shear-z"],float(raw[i][6]))
                    dir["Torsion"] = min(dir["Torsion"],float(raw[i][7]))
                    dir["Moment-y"] = min(dir["Moment-y"],float(raw[i][8]))
                    dir["Moment-z"] = min(dir["Moment-z"],float(raw[i][9]))
                    if len(raw[0])>10:
                        dir["Bi-Moment"] = min(dir["Bi-Moment"],float(raw[i][10]))
                        dir["T-Moment"] = min(dir["T-Moment"],float(raw[i][11]))
                        dir["W-Moment"] = min(dir["W-Moment"],float(raw[i][12]))
                if (loc == int(raw[i][0]) and req == 3):
                    dir_2["Axial"].append(float(raw[i][4]))
                    dir_2["Shear-y"].append(float(raw[i][5]))
                    dir_2["Shear-z"].append(float(raw[i][6]))
                    dir_2["Torsion"].append(float(raw[i][7]))
                    dir_2["Moment-y"].append(float(raw[i][8]))
                    dir_2["Moment-z"].append(float(raw[i][9]))
                    if len(raw[0])>10:
                        dir_2["Bi-Moment"].append(float(raw[i][10]))
                        dir_2["T-Moment"].append(float(raw[i][11]))
                        dir_2["W-Moment"].append(float(raw[i][12]))
                    loc += 5
            if req != 3: return(dir)
            if req == 3: return(dir_2)
        if db!= 0: print("Enter list of element ID (list of integers only!)")
    if type(elem)!= list: print("Enter list of element ID (list of integers only!) or leave it empty for max force in structure.")
#---------------------------------------------------------------------------------------------------------------
#Function to get summary of maximum & minimum forces for each unique section & element
def force_summary(mat = 1, sec = 1, elem = [], case = []):
    """Request type (1 for overall summary, 2  for required material & section, 3 for list of elements).  Sample:
    force_summary() for overall max & min forces for each type of unique material & section used in the software.
    force_summary(2, mat = [1,4], sec = [1,2]) for max & min force for (material 1 + section 1), (material 1 + section 2), (material 4 +  section 1) and (material 4 + section 2).
    force_summary(3, elem = [1,2,3,4]) for max & min force summary for unique material & section property combination among elements 1, 2, 3 & 4."""
    analyze()
    if elem == []: 
        li = get_select("USM", mat, sec)
    else:
        li = elem
    res = {}
    for i in li:
        a = beam_force(1,i,case)
        b = beam_force(2,i,case)
        res[i] = {"max":a,"min":b}
    return(res)
#---------------------------------------------------------------------------------------------------------------
#Function to get summary of maximum & minimum stresses for each unique section & element
def stress_summary(req = 1, mat = [], sec = [], elem = [], case = []):
    """Request type (1 for overall summary, 2  for required material & section, 3 for list of elements).  Sample:
    stress_summary() for overall max & min stress for each type of unique material & section used in the software.
    stress_summary(2, mat = [1,4], sec = [1,2]) for max & min stress for (material 1 + section 1), (material 1 + section 2), (material 4 +  section 1) and (material 4 + section 2).
    stress_summary(3, elem = [1,2,3,4]) for max & min stress summary for unique material & section property combination among elements 1, 2, 3 & 4."""
    analyze()
    if elem == []: 
        li = get_select("USM", mat, sec)
    else:
        li = elem
    res = {}
    for i in li:
        a = stress_tab(elem, case)
        max_str= {"top": 0,"bot": 0}                                #Empty dictionary to store max top stress results based on materil ID and section ID
        min_str = {"top": 0,"bot": 0}                               #Empty dictionary to store min top stress results based on materil ID and section ID
        for i in range(len(a)):
            max_str["top"] = max(max_str["top"],float(a[i][4]),float(a[i][5]))
            max_str["bot"] = max(max_str["bot"],float(a[i][6]),float(a[i][7]))
            min_str["top"] = min(min_str["top"],float(a[i][4]),float(a[i][5]))
            min_str["bot"] = min(min_str["bot"],float(a[i][6]),float(a[i][7]))
        res[i] = ({"max":max_str,"min":min_str})
    return(res)
#---------------------------------------------------------------------------------------------------------------
#Function to get section properties of the specific ID
def sect_prop(id=[]):
    """List of section ID.  Sample: Enter Sect_prop[3,4] for properties of section ID 4 & 5.  
    Enter sect_prop() for properties of all defined sections."""
    dir = {}
    units("N",length="MM")
    sect = MidasAPI("GET","/ope/SECTPROP")
    if id == []: a = list(sect['SECTPROP'].keys())
    if (id != [] and type(id)!= int): a = [str(e) for e in id]
    if type(id) == int: a = [str(id)]
    for i in a:
        if i in sect['SECTPROP'].keys():
            dir.update({int(i):{"Area":None , "Iy":None, "Iz":None, "Yl":None, "Yr":None, "Zt":None, "Zb":None,
            "Y1":None, "Z1":None, "Y2":None, "Z2":None, "Y3":None, "Z3":None, "Y4":None, "Z4":None}})
            data = [float(sect['SECTPROP'][i]['DATA'][0][1])]
            for j in list(range(4,10))+list(range(16,24)):
                data.append(float(sect['SECTPROP'][i]['DATA'][j][1]))
            for idx, key in enumerate(dir[int(i)]):
                dir[int(i)][key] = data[idx]
        elif i not in sect['SECTPROP'].keys(): print ("Section id", i, "is not defined in connected model.")
    units()
    return(dir)
#---------------------------------------------------------------------------------------------------------------
