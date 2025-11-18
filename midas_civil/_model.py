from ._mapi import *

from ._node import *
from ._element import *
from ._group import *
from ._load import *
from ._boundary import *

from ._section import *
from ._material import *
from ._thickness import *

from ._tendon import *
from ._result import *
from ._movingload import *

from ._temperature import *

from collections import defaultdict
class Model:

    #4 Function to check analysis status & perform analysis if not analyzed
    @staticmethod
    def analyse():
        """Checkes whether a model is analyzed or not and then performs analysis if required."""
        json_body = {
        "Argument": {
            "HEIGHT" : 1,
            "WIDTH" : 1,
            "SET_MODE": "post"
        }
        }
        resp = MidasAPI('POST','/view/CAPTURE',json_body)

        if 'message' in resp or 'error' in resp:
                MidasAPI("POST","/doc/ANAL",{"Assign":{}})
                return True
        print(" ⚠️   Model ananlysed. Switching to post-processing mode.")

    #9 Function to remove duplicate nodes and elements from Node & Element classes\
    @staticmethod
    def merge_nodes(tolerance = 0):
        """This functions removes duplicate nodes defined in the Node Class and modifies Element class accordingly.  \nSample: remove_duplicate()"""
        a=[]
        b=[]
        node_json = Node.json()
        elem_json = Element.json()
        node_di = node_json["Assign"]
        elem_di = elem_json["Assign"]
        for i in list(node_di.keys()):
            for j in list(node_di.keys()):
                if list(node_di.keys()).index(j) > list(node_di.keys()).index(i):
                    if (node_di[i]["X"] >= node_di[j]["X"] - tolerance and node_di[i]["X"] <= node_di[j]["X"] + tolerance):
                        if (node_di[i]["Y"] >= node_di[j]["Y"] - tolerance and node_di[i]["Y"] <= node_di[j]["Y"] + tolerance):
                            if (node_di[i]["Z"] >= node_di[j]["Z"] - tolerance and node_di[i]["Z"] <= node_di[j]["Z"] + tolerance):
                                a.append(i)
                                b.append(j)
        for i in range(len(a)):
            for j in range(len(b)):
                if a[i] == b[j]: 
                    a[i] = a[j]
                    for k in elem_di.keys():
                        for i in range(len(a)):
                            if elem_di[k]['NODE'][0] == b[i]: elem_di[k]['NODE'][0] = a[i]
                            if elem_di[k]['NODE'][1] == b[i]: elem_di[k]['NODE'][1] = a[i]
                            try: 
                                if elem_di[k]['NODE'][3] == b[i]: elem_di[k]['NODE'][3] = a[i]
                            except: pass
                            try: 
                                if elem_di[k]['NODE'][4] == b[i]: elem_di[k]['NODE'][4] = a[i]
                            except: pass

        if len(b)>0:
            for i in range(len(b)):
                if b[i] in node_di: del node_di[b[i]]
            Node.nodes = []
            Node.ids = []
            for i in node_di.keys():
                Node(node_di[i]['X'], node_di[i]['Y'], node_di[i]['Z'], i)
            Element.elements = []
            Element.ids = []
            for i in elem_di.keys():
                Element(elem_di[i], i)

    @staticmethod
    def units(force = "KN",length = "M", heat = "BTU", temp = "C"):
        """force --> KN, N, KFG, TONF, LFB, KIPS ||  
        \ndist --> M, CM, MM, FT, IN ||  
        \nheat --> CAL, KCAL, J, KJ, BTU ||  
        \ntemp --> C, F
        \nDefault --> KN, M, BTU, C"""
        if temp not in ["C","F"]:
            temp="C"
        if force not in ["KN", "N", "KGF", "TONF", "LBF", "KIPS"]:
            force = "KN"
        if length not in ["M", "CM", "MM", "FT", "IN"]:
            dist = "M"
        if heat not in ["CAL", "KCAL", "J", "KJ", "BTU"]:
            heat = "BTU"
        unit={"Assign":{
            1:{
                "FORCE":force,
                "DIST":length,
                "HEAT":heat,
                "TEMPER":temp
            }
        }}
        MidasAPI("PUT","/db/UNIT",unit)

    @staticmethod
    def select(crit_1 = "X", crit_2 = 0, crit_3 = 0, st = 'a', en = 'a', tolerance = 0):
        """Get list of nodes/elements as required.\n
        crit_1 (=> Along: "X", "Y", "Z". OR, IN: "XY", "YZ", "ZX". OR "USM"),\n
        crit_2 (=> With Ordinate value: Y value, X value, X Value, Z value, X value, Y value. OR Material ID),\n
        crit_3 (=> At Ordinate 2 value: Z value, Z value, Y value, 0, 0, 0. OR Section ID),\n
        starting ordinate, end ordinate, tolerance, node dictionary, element dictionary.\n
        Sample:  get_select("Y", 0, 2) for selecting all nodes and elements parallel Y axis with X ordinate as 0 and Z ordinate as 2."""
        output = {'NODE':[], 'ELEM':[]}
        ok = 0
        no = Node.json()
        el = Element.json()
        if crit_1 == "USM":
            materials = Material.json()
            sections = Section.json()
            elements = el
            k = list(elements.keys())[0]
            mat_nos = list((materials["Assign"].keys()))
            sect_nos = list((sections["Assign"].keys()))
            elem = {}
            for m in mat_nos:
                elem[int(m)] = {}
                for s in sect_nos:
                        elem[int(m)][int(s)] = []
            for e in elements[k].keys(): elem[((elements[k][e]['MATL']))][((elements[k][e]['SECT']))].append(int(e))
            output['ELEM'] = elem[crit_2][crit_3]
            ok = 1
        elif no != "" and el != "":
            n_key = list(no.keys())[0]
            e_key = list(el.keys())[0]
            if n_key == "Assign": no["Assign"] = {str(key):value for key,value in no["Assign"].items()}
            if e_key == "Assign": el["Assign"] = {str(key):value for key,value in el["Assign"].items()}
            if crit_1 == "X": 
                cr2 = "Y"
                cr3 = "Z"
                ok = 1
            if crit_1 == "Y": 
                cr2 = "X"
                cr3 = "Z"
                ok = 1
            if crit_1 == "Z": 
                cr2 = "X"
                cr3 = "Y"
                ok = 1
            if crit_1 == "XY" or crit_1 == "YX":
                cr2 = "Z"
                ok = 1
            if crit_1 == "YZ" or crit_1 == "ZY":
                cr2 = "X"
                ok = 1
            if crit_1 == "ZX" or crit_1 == "XZ":
                cr2 = "Y"
                ok = 1
            if len(crit_1) == 1 and ok == 1:
                if st == 'a': st = min([v[crit_1] for v in no[n_key].values()])
                if en == 'a': en = max([v[crit_1] for v in no[n_key].values()])
                for n in no[n_key].keys():
                    curr = no[n_key][n]
                    if curr[cr2] >= crit_2 - tolerance and curr[cr2] <= crit_2 + tolerance:
                        if curr[cr3] >= crit_3 - tolerance and curr[cr3] <= crit_3 + tolerance:
                            if curr[crit_1] >= st and curr[crit_1] <= en: output['NODE'].append(int(n))
                for e in el[e_key].keys():
                    curr_0 = no[n_key][str(el[e_key][e]['NODE'][0])]
                    curr_1 = no[n_key][str(el[e_key][e]['NODE'][1])]
                    if curr_0[cr2] == curr_1[cr2] and curr_0[cr3] == curr_1[cr3]:
                        if curr_0[cr2] >= crit_2 - tolerance and curr_0[cr2] <= crit_2 + tolerance:
                            if curr_0[cr3] >= crit_3 - tolerance and curr_0[cr3] <= crit_3 + tolerance:
                                if curr_1[cr2] >= crit_2 - tolerance and curr_1[cr2] <= crit_2 + tolerance:
                                    if curr_1[cr3] >= crit_3 - tolerance and curr_1[cr3] <= crit_3 + tolerance:
                                        if curr_0[crit_1] >= st and curr_0[crit_1] <= en and curr_1[crit_1] >= st and curr_1[crit_1] <= en:
                                            output['ELEM'].append(int(e))
            if len(crit_1) == 2 and ok == 1:
                if st == 'a': st = min(min([v[crit_1[0]] for v in no[n_key].values()]), min([v[crit_1[1]] for v in no[n_key].values()]))
                if en == 'a': en = max(max([v[crit_1[0]] for v in no[n_key].values()]), max([v[crit_1[1]] for v in no[n_key].values()]))
                for n in no[n_key].keys():
                    curr = no[n_key][n]
                    if curr[cr2] >= crit_2 - tolerance and curr[cr2] <= crit_2 + tolerance:
                        if curr[crit_1[0]] >= st and curr[crit_1[1]] >= st and curr[crit_1[0]] <= en and curr[crit_1[1]] <= en: output['NODE'].append(int(n))
                for e in el[e_key].keys():
                    curr_0 = no[n_key][str(el[e_key][e]['NODE'][0])]
                    curr_1 = no[n_key][str(el[e_key][e]['NODE'][1])]
                    if curr_0[cr2] == curr_1[cr2]:
                        if curr_0[cr2] >= crit_2 - tolerance and curr_0[cr2] <= crit_2 + tolerance:
                            if curr_1[cr2] >= crit_2 - tolerance and curr_1[cr2] <= crit_2 + tolerance:
                                if curr_0[crit_1[0]] >= st and curr_0[crit_1[0]] <= en and curr_1[crit_1[0]] >= st and curr_1[crit_1[0]] <= en:
                                    if curr_0[crit_1[1]] >= st and curr_0[crit_1[1]] <= en and curr_1[crit_1[1]] >= st and curr_1[crit_1[1]] <= en:
                                        output['ELEM'].append(int(e))
        if ok != 1: output = "Incorrect input.  Please check the syntax!"
        return output



    # @staticmethod
    # def _create2(request = "update", set = 1, force = "KN", length = "M", heat = "BTU", temp = "C"):
    #     """request["update" to update a model, "call" to get details of existing model], \nforce[Optional], length[Optional], heat[Optional], temp[Optional].  
    #     \nSample: model() to update/create model. model("call") to get details of existing model and update classes.\n
    #     set = 1 => Functions that don't need to call data from connected model file.\n
    #     set = 2 => Functions that may need to call data from connected model file."""
    #     Model.units(force, length, heat, temp)
    #     if MAPI_KEY.data == []:  print(f"Enter the MAPI key using the MAPI_KEY command.")
    #     if MAPI_KEY.data != []:
    #         if set == 1:
    #             if request == "update" or request == "create" or request == "PUT":
    #                 if Node.json() != {"Assign":{}}: Node.create()
    #                 if Element.json() != {"Assign":{}}: Element.create()
    #                 if Section.json() != {"Assign":{}}: Section.create()
    #                 if Group.json_BG() != {"Assign":{}}: Group.create_BG()
    #                 if Group.json_LG() != {"Assign":{}}: Group.create_LG()
    #                 if Group.json_TG() != {"Assign":{}}: Group.create_TG()
    #                 if Material.json() != {"Assign":{}}: Material.create()
    #             if request == "call" or request == "GET":
    #                 Node.sync()
    #                 Element.sync()
    #                 Section.sync()
    #                 Group.sync()
    #                 Material.sync()
    #         if set == 2:
    #             if request == "update" or request == "create" or request == "PUT":
    #                 if Node.json() != {"Assign":{}}: Node.create()
    #                 if Element.json() != {"Assign":{}}: Element.create()
    #                 if Section.json() != {"Assign":{}}: Section.create()
    #                 if Group.json_BG() != {"Assign":{}}: Group.create_BG()
    #                 if Group.json_LG() != {"Assign":{}}: Group.create_LG()
    #                 if Group.json_TG() != {"Assign":{}}: Group.create_TG()
    #                 if Material.json() != {"Assign":{}}: Material.create()
    #                 if Group.json_SG() != {"Assign":{}}: Group.create_SG()
    #             if request == "call" or request == "GET": 
    #                 Node.update_class()
    #                 Element.update_class()
    #                 Section.update_class()
    #                 Group.update_class()
    #                 Material.update_class()


    @staticmethod
    def maxID(dbNAME:str = 'NODE') -> int :
        ''' 
        Returns maximum ID of a DB in CIVIL NX
        dbNAME - 'NODE' , 'ELEM' , 'THIK' , 'SECT' 
        If no data exist, 0 is returned
        '''
        dbJS = MidasAPI('GET',f'/db/{dbNAME}')
        if dbJS == {'message': ''}:
            return 0
        return max(map(int, list(dbJS[dbNAME].keys())))

    @staticmethod
    def create():
        """Create Material, Section, Node, Elements, Groups and Boundary."""
        if Material.mats!=[]: Material.create()
        if Section.sect!=[]: Section.create()
        if Thickness.thick!=[]: Thickness.create()
        if Node.nodes!=[]: Node.create()
        if Element.elements!=[] : Element.create()
        if NodeLocalAxis.skew!=[] : NodeLocalAxis.create()
        Group.create()
        Boundary.create()
        Load.create()
        Temperature.create()
        Tendon.create()
        if Section.TaperedGroup.data !=[] : Section.TaperedGroup.create()
        MovingLoad.create()
        LoadCombination.create()
        





    @staticmethod
    def clear():
        Node.delete()
        Element.delete()
        Load_Case.delete()
        Group.delete()
        Material.deleteAll()
        Section.delete()
        Boundary.delete()

    @staticmethod
    def type(strc_type=0,mass_type=1,gravity:float=0,mass_dir=1):
        """Structure Type option 
        --------------------------------
        
        Structure Type:
            0 = 3D
            1 = X-Z Plane
            2 = Y-Z Plane
            3 = X-Y Plane
            4 = Constraint RZ

        Mass Type:
            1 = Lumped Mass
            2 = Consistent Mass
        
        Gravity Acceleration (g) = 9.81 m/s^2
        
        Mass Direction(Structure Mass type):
            1 = Convert to X, Y, Z
            2 = Convert to X, Y
            3 = Convert to Z
        """

        js = {"Assign": {
              "1":{}}}
        

        js["Assign"]["1"]["STYP"] = strc_type

        js["Assign"]["1"]["MASS"] = mass_type

        if mass_dir==0:
            js["Assign"]["1"]["bSELFWEIGHT"] = False
        else:
            js["Assign"]["1"]["bSELFWEIGHT"] = True
            js["Assign"]["1"]["SMASS"] = mass_dir

        if gravity!=0:
            js["Assign"]["1"]["GRAV"] = gravity


        MidasAPI("PUT","/db/STYP",js)

    @staticmethod
    def save(location=""):
        """Saves the model\nFor the first save, provide location - \nModel.save("D:\\model2.mcb")"""
        if location=="":
            MidasAPI("POST","/doc/SAVE",{"Argument":{}})
        else:
            MidasAPI("POST","/doc/SAVEAS",{"Argument":str(location)})#Dumy location

    @staticmethod
    def saveAs(location=""):
        """Saves the model at location provided"""
        MidasAPI("POST","/doc/SAVEAS",{"Argument":str(location)})
    
    @staticmethod
    def open(location=""):
        """Open Civil NX model file \n Model.open("D:\\model.mcb")"""
        MidasAPI("POST","/doc/OPEN",{"Argument":str(location)})

    @staticmethod
    def new():
        """Creates a new model"""
        MidasAPI("POST","/doc/NEW",{"Argument":{}})

    @staticmethod
    def info(project_name="",revision="",user="",title=""):
        """Enter Project information"""

        js = {"Assign": {
              "1":{}}}
        
        if project_name+revision+user+title=="":
            return MidasAPI("GET","/db/PJCF",{})
        else:
            if project_name!="":
                js["Assign"]["1"]["PROJECT"] = project_name
            if revision!="":
                js["Assign"]["1"]["REVISION"] = revision
            if user!="":
                js["Assign"]["1"]["USER"] = user
            if title!="":
                js["Assign"]["1"]["TITLE"] = title


            MidasAPI("PUT","/db/PJCF",js)
    
    @staticmethod
    def exportJSON(location=""):
        """Export the model data as JSON file
        Model.exportJSON('D:\\model.json')"""
        if location.endswith('.json'):
            MidasAPI("POST","/doc/EXPORT",{"Argument":str(location)})
        else:
            print('⚠️  Location data in exportJSON is missing file extension')

    @staticmethod
    def exportMCT(location=""):
        """Export the model data as MCT file
        Model.exportMCT('D:\\model.mct')"""
        if location.endswith('.mct'):
            MidasAPI("POST","/doc/EXPORTMXT",{"Argument":str(location)})
        else:
            print('⚠️  Location data in exportMCT is missing file extension')

    
    @staticmethod
    def importJSON(location=""):
        """Import JSON data file in MIDAS CIVIL NX
        Model.importJSON('D:\\model.json')"""
        if location.endswith('.json'):
            MidasAPI("POST","/doc/IMPORT",{"Argument":str(location)})
        else:
            print('⚠️  Location data in importJSON is missing file extension')

    @staticmethod
    def importMCT(location=""):
        """Import MCT data file in MIDAS CIVIL NX
        Model.importMCT('D:\\model.mct')"""
        if location.endswith('.mct'):
            MidasAPI("POST","/doc/IMPORTMXT",{"Argument":str(location)})
        else:
            print('⚠️  Location data in importMCT is missing file extension')

    @staticmethod
    def get_element_connectivity():
        element_connectivity = {}
        for element in Element.elements:
            element_id = element.ID
            connected_nodes = element.NODE
            element_connectivity.update({element_id: connected_nodes})
        return element_connectivity

    @staticmethod
    def get_node_connectivity():
        element_connectivity = Model.get_element_connectivity()
        node_connectivity = defaultdict(list)

        for element_id, nodes in element_connectivity.items():
            for node in nodes:
                node_connectivity[node].append(element_id)
        node_connectivity = dict(node_connectivity)
        return node_connectivity

    # @staticmethod
    # def visualise():
    #     try:
    #         from ._visualise import displayWindow
    #         displayWindow()
    #     except:
    #         pass

    # @staticmethod
    # def snap():
    #     try:
    #         from ._visualise import take_snapshot
    #         take_snapshot()
    #     except:
    #         pass








