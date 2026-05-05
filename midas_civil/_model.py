from ._mapi import MidasAPI,NX
from colorama import Fore,Style
import numpy as np
import math
from ._node import Node , NodeLocalAxis
from ._element import Element
from ._group import Group
from ._load import Load
from ._boundary import Boundary

from ._section import Section
from ._material import Material
from ._thickness import Thickness

from ._tendon import Tendon
from ._loadcomb import LoadCombination
from ._movingload import MovingLoad

from ._temperature import Temperature
from ._construction import CS

from ._view import View

from collections import defaultdict
from typing import Literal

_forceUnit = Literal["KN", "N", "KGF", "TONF", "LBF", "KIPS"]
_lengthUnit = Literal["M", "CM", "MM", "FT", "IN"]
_heatUnit = Literal["CAL", "KCAL", "J", "KJ", "BTU"]
_tempUnit = Literal["C","F"]

_dbNames = Literal['NODE','ELEM','MATL','SECT','RIGD','ELNK','THIK']
_dbMapping = {
    "NODE" : "Node",
    "ELEM" : "Element",
    "MATL" : "Material",
    "SECT" : "Section",
    "THIK" : "Thickness",
    "ELNK" : "Elastic Link",
    "RIGD" : "Rigid Link",
    "SKEW" : "Node Local Axis",
    "STLD" : "Static Load Case",

}
_SelectOutput = Literal['NODE_ID','NODE','ELEM_ID','ELEM']
_SelectOutputElem = Literal['ELEM_ID','ELEM']
_getSelectOutput = Literal['ELEM_ID','NODE_ID']

class Model:

    @staticmethod
    def gravity():
        g_SI = 9.806

        len_unit =NX.units['DIST']
        len_multi = {
            "M" : 1,
            "CM" : 100,
            "MM" : 1000,
            "IN" : 39.3701,
            "FT" : 3.28084
        }
        
        len_multiplier = len_multi[len_unit]

        return g_SI*len_multiplier

    bounds = {
        "X_min" : -1,
        "X_max" : 1,
        "Y_min" : -1,
        "Y_max" : 1,
        "Z_min" : -1,
        "Z_max" : 1,
    }

    @staticmethod
    def getBounds():
        '''Get the bounds of the model'''
        min_z = 0
        max_z = 0
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for nd in Node.nodes:
            min_z = min(min_z,nd.Z)
            max_z = max(max_z,nd.Z)
            min_x = min(min_x,nd.X)
            max_x = max(max_x,nd.X)
            min_y = min(min_y,nd.Y)
            max_y = max(max_y,nd.Y)
        Model.bounds = {
            "X_min" : min_x,
            "X_max" : max_x,
            "Y_min" : min_y,
            "Y_max" : max_y,
            "Z_min" : min_z,
            "Z_max" : max_z,
        }

        return Model.bounds

    #4 Function to check analysis status & perform analysis if not analyzed
    @staticmethod
    def analyse():
        """Checks whether a model is analyzed or not and then performs analysis if required."""
        json_body = {
        "Argument": {
            "HEIGHT" : 2,
            "WIDTH" : 2,
            "SET_MODE": "post"
        }
        }
        _current_dispWarning = NX.dispWarning
        NX.dispWarning = False
        resp = MidasAPI('POST','/view/CAPTURE',json_body)
        NX.dispWarning = _current_dispWarning

        if 'message' in resp or 'error' in resp:
                MidasAPI("POST","/doc/ANAL",{"Assign":{}})
        print(" 🔒   Model analysed. Switching to post-processing mode.")

    # @staticmethod
    # def merge_nodes(tolerance = 0):
    #     """This functions removes duplicate nodes defined in the Node Class and modifies Element class accordingly.  \nSample: remove_duplicate()"""
    #     a=[]
    #     b=[]
    #     node_json = Node.json()
    #     elem_json = Element.json()
    #     node_di = node_json["Assign"]
    #     elem_di = elem_json["Assign"]
    #     for i in list(node_di.keys()):
    #         for j in list(node_di.keys()):
    #             if list(node_di.keys()).index(j) > list(node_di.keys()).index(i):
    #                 if (node_di[i]["X"] >= node_di[j]["X"] - tolerance and node_di[i]["X"] <= node_di[j]["X"] + tolerance):
    #                     if (node_di[i]["Y"] >= node_di[j]["Y"] - tolerance and node_di[i]["Y"] <= node_di[j]["Y"] + tolerance):
    #                         if (node_di[i]["Z"] >= node_di[j]["Z"] - tolerance and node_di[i]["Z"] <= node_di[j]["Z"] + tolerance):
    #                             a.append(i)
    #                             b.append(j)
    #     for i in range(len(a)):
    #         for j in range(len(b)):
    #             if a[i] == b[j]: 
    #                 a[i] = a[j]
    #                 for k in elem_di.keys():
    #                     for i in range(len(a)):
    #                         if elem_di[k]['NODE'][0] == b[i]: elem_di[k]['NODE'][0] = a[i]
    #                         if elem_di[k]['NODE'][1] == b[i]: elem_di[k]['NODE'][1] = a[i]
    #                         try: 
    #                             if elem_di[k]['NODE'][3] == b[i]: elem_di[k]['NODE'][3] = a[i]
    #                         except: pass
    #                         try: 
    #                             if elem_di[k]['NODE'][4] == b[i]: elem_di[k]['NODE'][4] = a[i]
    #                         except: pass

    #     if len(b)>0:
    #         for i in range(len(b)):
    #             if b[i] in node_di: del node_di[b[i]]
    #         Node.nodes = []
    #         Node.ids = []
    #         for i in node_di.keys():
    #             Node(node_di[i]['X'], node_di[i]['Y'], node_di[i]['Z'], i)
    #         Element.elements = []
    #         Element.ids = []
    #         for i in elem_di.keys():
    #             Element(elem_di[i], i)

    
    @staticmethod
    def units(force:_forceUnit = "KN",length:_lengthUnit = "M", heat:_heatUnit = "BTU", temp:_tempUnit = "C"):
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
            length = "M"
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
        NX.units = {
                "FORCE":force,
                "DIST":length,
                "HEAT":heat,
                "TEMPER":temp
            }
        MidasAPI("PUT","/db/UNIT",unit)


    @staticmethod
    def maxID(dbNAME:_dbNames = 'NODE' , fast:bool=False) -> int :
        ''' 
        Returns maximum ID of a DB in CIVIL NX
        dbNAME - 'NODE' , 'ELEM' , 'THIK' , 'SECT' 
        fast - 'NODE' , 'ELEM' , 'THIK' , 'SECT' , 'MATL'
        If no data exist, 0 is returned
        '''

        if fast:
            
            resp = MidasAPI('GET','/ope/PROJECTSTATUS')
            NX.modelIDs = resp["PROJECTSTATUS"]["DATA"]
            NX.modelIDs += resp["PROJECTSTATUS"]["DATA_LOAD"]

            for data in NX.modelIDs:
                if data[0].lower() == _dbMapping[dbNAME].lower() :
                    _d2 = 0
                    try: _d2 = int(data[2])
                    except: pass
                    if _d2==0:
                        return int(data[1])
                    return _d2
            return 0
        
        else:
            dbJS = MidasAPI('GET',f'/db/{dbNAME}')
            if dbJS == {'message': ''}:
                return 0
            return max(map(int, list(dbJS[dbNAME].keys())))

    @staticmethod
    def create():
        """Create Material, Section, Node, Elements, Groups and Boundary."""
        from tqdm import tqdm
        pbar = tqdm(total=15,desc="Creating Model...")

        if Material.mats!=[]: Material.create()
        pbar.update(1)
        pbar.set_description_str("Creating Section...")
        if Section.sect!=[]: Section.create()
        pbar.update(1)
        pbar.set_description_str("Creating Thickness...")
        if Thickness.thick!=[]: Thickness.create()
        pbar.update(1)
        pbar.set_description_str("Creating Node...")
        if Node.nodes!=[]: Node.create()
        pbar.update(1)
        pbar.set_description_str("Creating Element...")
        if Element.elements!=[] : Element.create()
        pbar.update(1)
        pbar.set_description_str("Creating Tapered Group...")
        if NX.autoTaperGroup: Section.TaperedGroup.autoGenerate()
        if Section.TaperedGroup.data !=[] : Section.TaperedGroup.create()
        pbar.update(1)
        pbar.set_description_str("Creating Node Local Axis...")
        if NodeLocalAxis.skew!=[] : NodeLocalAxis.create()
        pbar.update(1)
        pbar.set_description_str("Creating Group...")
        Group.create()
        pbar.update(1)
        pbar.set_description_str("Creating Boundary...")
        Boundary.create()
        pbar.update(1)
        pbar.set_description_str("Creating Load...")
        Load.create()
        pbar.update(1)
        pbar.set_description_str("Creating Temperature...")
        Temperature.create()
        pbar.update(1)
        pbar.set_description_str("Creating Tendon...")
        Tendon.create()
        pbar.update(1)
        pbar.set_description_str("Creating Construction Stages...")
        CS.create()
        pbar.update(1)
        pbar.set_description_str("Creating Moving Load...")
        MovingLoad.create()
        pbar.update(1)
        pbar.set_description_str("Creating Load Combination...")
        LoadCombination.create()
        pbar.update(1)
        pbar.set_description_str(Fore.GREEN+"Model creation complete"+Style.RESET_ALL)
        
    @staticmethod
    def clear():
        Material.clearAll()
        Section.clear()
        Thickness.clear()
        Node.clear()
        Element.clear()
        NodeLocalAxis.clear()
        Group.clear()
        Boundary.clear()
        Load.clear()
        Temperature.clear()
        Tendon.clear()
        Section.TaperedGroup.clear()
        LoadCombination.clear()
        

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
            if location.endswith('.mcb') or location.endswith('.mcbz'):
                MidasAPI("POST","/doc/SAVEAS",{"Argument":str(location)})#Dumy location
            else:
                print('⚠️  File extension is missing')
                
    @staticmethod
    def saveAs(location=""):
        """Saves the model at location provided   
         Model.saveAs("D:\\model2.mcb")"""
        if location.endswith('.mcb') or location.endswith('.mcbz'):
            MidasAPI("POST","/doc/SAVEAS",{"Argument":str(location)})
        else:
            print('⚠️  File extension is missing')
    
    @staticmethod
    def open(location=""):
        """Open Civil NX model file \n Model.open("D:\\model.mcb")"""
        if location.endswith('.mcb') or location.endswith('.mcbz'):
            MidasAPI("POST","/doc/OPEN",{"Argument":str(location)})
        else:
            print('⚠️  File extension is missing')
        
    @staticmethod
    def new():
        """Creates a new model"""
        MidasAPI("POST","/doc/NEW",{"Argument":{}})

    @staticmethod
    def close():
        """Closes the model"""
        MidasAPI("POST","/doc/CLOSE",{"Argument":{}})

    
    @staticmethod
    def saveStageAs(stageName="",filePath=""):
        """Save Construction Stage as separate model"""
        if filePath.endswith('.mcb') or filePath.endswith('.mcbz'):
            MidasAPI("POST","/doc/STAGAS",{"Argument":{"EXPORT_PATH":str(filePath), "STAGE_STEP":str(stageName)}})
        else:
            print('⚠️  File extension is missing')
        

    @staticmethod
    def info(project_name="",revision="",user="",title="",comment =""):
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
            if comment != "" :
                js["Assign"]["1"]["COMMENT"] = comment


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

    @staticmethod
    def visualise():
        if NX.visualiser:
            try:
                from ._visualise import displayWindow
                displayWindow()
            except:
                pass

    @staticmethod
    def snap():
        if NX.visualiser:
            try:
                from ._visualise import take_snapshot
                take_snapshot()
            except:
                pass





    class Select:

        @staticmethod
        def Line(point1:tuple = (0,0,0) , point2:tuple=(1,0,0) , output:_SelectOutput='NODE_ID',radius:float=0.001) -> set:
            final_output = []
            output_list = []    #Tuple (dist, nodeID)
            x1 = min(point1[0]-radius,point2[0]-radius)
            x2 = max(point1[0]+radius,point2[0]+radius)
            y1 = min(point1[1]-radius,point2[1]-radius)
            y2 = max(point1[1]+radius,point2[1]+radius)
            z1 = min(point1[2]-radius,point2[2]-radius)
            z2 = max(point1[2]+radius,point2[2]+radius)

            direction = np.subtract(point2,point1)

            bELEM = False
            bID = True
            
            if output == 'ELEM_ID': 
                gridStr = set(Element.Grid.keys())
                grid_complete = Element.Grid
                bELEM,bID = True,True
            elif output == 'ELEM': 
                gridStr = set(Element.Grid.keys())
                grid_complete = Element.Grid
                bELEM,bID = True,False
            elif output == 'NODE': 
                gridStr = set(Node.Grid.keys())
                grid_complete = Node.Grid
                bID = False
            else:
                gridStr = set(Node.Grid.keys())
                grid_complete = Node.Grid
            
            possible_gridStr = set()
            for i in np.arange(int(x1),int(x2)+1,1):
                for j in np.arange(int(y1),int(y2)+1,1):
                    for k in np.arange(int(z1),int(z2)+1,1):
                        possible_gridStr.add(f"{i},{j},{k}")
            
            common_gridStr = list(gridStr.intersection(possible_gridStr))

            for eachAvailGrid in common_gridStr:
                for elm in grid_complete[eachAvailGrid]:
                    point = elm.CENTER if bELEM else elm.LOC

                    if x1 <= point[0] <= x2 and y1 <= point[1] <= y2 and z1 <= point[2] <= z2 :
                        diff = np.subtract(point, point1)
                        cross = np.cross(diff, direction)
                        along_dist = np.linalg.norm(diff)
                        perp_dist = np.linalg.norm(cross) / np.linalg.norm(direction)
                        if perp_dist<radius:
                            output_list.append((along_dist,elm.ID if bID else elm))
            
            sorted_list = sorted(output_list)
            final_output = [elm for dist,elm in sorted_list]
            return final_output
        
        @staticmethod
        def __Line_along__(alongAxis = 'X',point:tuple = (0,0,0), output:_SelectOutput='NODE_ID',radius:float=0.001) -> set:
            Model.getBounds()
            final_output = []
            output_list = []    #Tuple (dist, nodeID)
            x1 = point[0]-radius
            x2 = point[0]+radius
            y1 = point[1]-radius
            y2 = point[1]+radius
            z1 = point[2]-radius
            z2 = point[2]+radius

            if alongAxis == 'Y':
                y1 = Model.bounds['Y_min']
                y2 = Model.bounds['Y_max']
            elif alongAxis == 'Z':
                z1 = Model.bounds['Z_min']
                z2 = Model.bounds['Z_max']
            else:
                x1 = Model.bounds['X_min']
                x2 = Model.bounds['X_max']
            bELEM = False
            bID = True
            
            if output == 'ELEM_ID': 
                gridStr = set(Element.Grid.keys())
                grid_complete = Element.Grid
                bELEM,bID = True,True
            elif output == 'ELEM': 
                gridStr = set(Element.Grid.keys())
                grid_complete = Element.Grid
                bELEM,bID = True,False
            elif output == 'NODE': 
                gridStr = set(Node.Grid.keys())
                grid_complete = Node.Grid
                bID = False
            else:
                gridStr = set(Node.Grid.keys())
                grid_complete = Node.Grid
            
            possible_gridStr = set()
            for i in np.arange(int(x1),int(x2)+1,1):
                for j in np.arange(int(y1),int(y2)+1,1):
                    for k in np.arange(int(z1),int(z2)+1,1):
                        possible_gridStr.add(f"{i},{j},{k}")
            
            common_gridStr = list(gridStr.intersection(possible_gridStr))
            for eachAvailGrid in common_gridStr:
                for elm in grid_complete[eachAvailGrid]:
                    point = elm.CENTER if bELEM else elm.LOC
                    

                    if x1 <= point[0] <= x2 and y1 <= point[1] <= y2 and z1 <= point[2] <= z2 :
                        diff = [np.subtract(point, (x1,y1,z1))]
                        along_dist = np.linalg.norm(diff)
                        output_list.append((along_dist,elm.ID if bID else elm))
            sorted_list = sorted(output_list)
            final_output = [elm for dist,elm in sorted_list]
            return final_output
        
        @staticmethod
        def Line_alongX(point:tuple = (0,0,0), output:_SelectOutput='NODE_ID',radius:float=0.001) -> set:
            return Model.Select.__Line_along__('X',point,output,radius)
        @staticmethod
        def Line_alongY(point:tuple = (0,0,0), output:_SelectOutput='NODE_ID',radius:float=0.001) -> set:
            return Model.Select.__Line_along__('Y',point,output,radius)
        @staticmethod
        def Line_alongZ(point:tuple = (0,0,0), output:_SelectOutput='NODE_ID',radius:float=0.001) -> set:
            return Model.Select.__Line_along__('Z',point,output,radius)
        


        @staticmethod
        def Box(point1:tuple = (0,0,0) , point2:tuple=(1,0,0) , output:_SelectOutput='NODE_ID') -> set:
            output_list = []

            tol:float=0.001
            x1 = min(point1[0]-tol,point2[0]-tol)
            x2 = max(point1[0]+tol,point2[0]+tol)
            y1 = min(point1[1]-tol,point2[1]-tol)
            y2 = max(point1[1]+tol,point2[1]+tol)
            z1 = min(point1[2]-tol,point2[2]-tol)
            z2 = max(point1[2]+tol,point2[2]+tol)

            bELEM = False
            bID = True
            
            if output == 'ELEM_ID': 
                gridStr = set(Element.Grid.keys())
                grid_complete = Element.Grid
                bELEM,bID = True,True
            elif output == 'ELEM': 
                gridStr = set(Element.Grid.keys())
                grid_complete = Element.Grid
                bELEM,bID = True,False
            elif output == 'NODE': 
                gridStr = set(Node.Grid.keys())
                grid_complete = Node.Grid
                bID = False
            else:
                gridStr = set(Node.Grid.keys())
                grid_complete = Node.Grid
            

            possible_gridStr = set()
            for i in np.arange(int(x1),int(x2)+1,1):
                for j in np.arange(int(y1),int(y2)+1,1):
                    for k in np.arange(int(z1),int(z2)+1,1):
                        possible_gridStr.add(f"{i},{j},{k}")
            
            common_gridStr = list(gridStr.intersection(possible_gridStr))

            for eachAvailGrid in common_gridStr:
                for elm in grid_complete[eachAvailGrid]:
                    point = elm.CENTER if bELEM else elm.LOC

                    if x1 <= point[0] <= x2 and y1 <= point[1] <= y2 and z1 <= point[2] <= z2 :
                        output_list.append(elm.ID if bID else elm)
            
            
            return set(output_list)
        
        @staticmethod
        def __Plane__(plane = 'XY' , point:tuple=(0,0,0) , output:_SelectOutput='NODE_ID') -> set:
            output_list = []
            Model.getBounds()

            radius:float=0.001

            x1 = Model.bounds['X_min']
            x2 = Model.bounds['X_max']
            y1 = Model.bounds['Y_min']
            y2 = Model.bounds['Y_max']
            z1 = Model.bounds['Z_min']
            z2 = Model.bounds['Z_max']

            if plane == 'YZ':
                x1 = point[0]-radius
                x2 = point[0]+radius
            elif plane == 'XZ':
                y1 = point[1]-radius
                y2 = point[1]+radius
            else:
                z1 = point[2]-radius
                z2 = point[2]+radius

            bELEM = False
            bID = True
            
            if output == 'ELEM_ID': 
                gridStr = set(Element.Grid.keys())
                grid_complete = Element.Grid
                bELEM,bID = True,True
            elif output == 'ELEM': 
                gridStr = set(Element.Grid.keys())
                grid_complete = Element.Grid
                bELEM,bID = True,False
            elif output == 'NODE': 
                gridStr = set(Node.Grid.keys())
                grid_complete = Node.Grid
                bID = False
            else:
                gridStr = set(Node.Grid.keys())
                grid_complete = Node.Grid
            

            possible_gridStr = set()
            for i in np.arange(int(x1),int(x2)+1,1):
                for j in np.arange(int(y1),int(y2)+1,1):
                    for k in np.arange(int(z1),int(z2)+1,1):
                        possible_gridStr.add(f"{i},{j},{k}")
            
            common_gridStr = list(gridStr.intersection(possible_gridStr))

            for eachAvailGrid in common_gridStr:
                for elm in grid_complete[eachAvailGrid]:
                    point = elm.CENTER if bELEM else elm.LOC

                    if x1 <= point[0] <= x2 and y1 <= point[1] <= y2 and z1 <= point[2] <= z2 :
                        output_list.append(elm.ID if bID else elm)
            
            
            return set(output_list)
        
        @staticmethod
        def Plane_XY(point:tuple=(0,0,0) , output:_SelectOutput='NODE_ID') -> set:
            return Model.Select.__Plane__('XY',point,output)
        
        @staticmethod
        def Plane_YZ(point:tuple=(0,0,0) , output:_SelectOutput='NODE_ID') -> set:
            return Model.Select.__Plane__('YZ',point,output)
        
        @staticmethod
        def Plane_XZ(point:tuple=(0,0,0) , output:_SelectOutput='NODE_ID') -> set:
            return Model.Select.__Plane__('XZ',point,output)

        @staticmethod
        def Element(type=None,matID=None,secID=None,output:_SelectOutputElem='ELEM_ID') -> set:
            output_list = []
            if output == 'ELEM_ID':
                bID = True
            else:
                bID = False

            _mat_list = []
            _sec_list = []
            _type_list = []

            _temp_list = set()

            bMat = True if matID!=None else False
            bSec = True if secID!=None else False
            bType = True if type!=None else False

            from ._utils import _convItem2List
            matID = _convItem2List(matID)
            secID = _convItem2List(secID)
            type = _convItem2List(type)

            for elm in Element.elements:
                if elm.SECT in secID:
                    _sec_list.append(elm)
                if elm.MATL in matID:
                    _mat_list.append(elm)
                if elm.TYPE in type:
                    _type_list.append(elm)

            bListAssigned = False
            if bMat: 
                _temp_list = set(_mat_list)
                bListAssigned = True

            if not bListAssigned:
                if bSec: _temp_list = set(_sec_list)
                elif bType: _temp_list = set(_type_list)

            # print(_temp_list)

            if bMat: _temp_list.intersection_update(set(_mat_list))
            if bSec: _temp_list.intersection_update(set(_sec_list))
            if bType: _temp_list.intersection_update(set(_type_list))

            if bID:
                output_list = {elm.ID for elm in _temp_list}
            else: output_list = _temp_list
                
            return output_list


    @staticmethod
    def IMAGE(location:str='',image_size:tuple = None , view:str='pre',CS_StageName:str='',_boutputImage:bool=True):
        ''' 
        Capture the image in the viewport
            Location - image location
            Image Size =  height and width of image captured
            View - 'pre' or 'post'
            stage - CS name
        '''
        from base64 import b64decode
        if image_size==None: image_size=View.Image_Size
        json_body = {
                "Argument": {
                    "SET_MODE":"pre",
                    "SET_HIDDEN":View.Hidden,
                    "HEIGHT": image_size[1],
                    "WIDTH": image_size[0]
                }
            }
        
        if View.Angle.__newH__ == True or View.Angle.__newV__ == True:
            json_body['Argument']['ANGLE'] = View.Angle._json()

        if View.Active.__default__ ==False:
            json_body['Argument']['ACTIVE'] = View.Active._json()
        
        if view=='post':
            json_body['Argument']['SET_MODE'] = 'post'
        elif view=='pre':
            json_body['Argument']['SET_MODE'] = 'pre'

        if CS_StageName != '':
            json_body['Argument']['STAGE_NAME'] = CS_StageName

        resp = MidasAPI('POST','/view/CAPTURE',json_body)

        bs64_img = b64decode(resp["base64String"])
        if location:
            __img_file = open(location, 'wb')  # Open image file to save.
            __img_file.write(bs64_img)  # Decode and write data.
            __img_file.close()

        if _boutputImage:
            from PIL import Image as ImagePIL
            from io import BytesIO
            # return bs64_img
            return ImagePIL.open(BytesIO(bs64_img))
        return resp
    
    @staticmethod
    def getSelected(item:_getSelectOutput = "ELEM_ID"):
        resp = MidasAPI("GET","/view/SELECT")

        if item == 'NODE_ID':
            return resp["SELECT"]["NODE_LIST"]
        elif item == 'ELEM_ID':
            return resp["SELECT"]["ELEM_LIST"]
        else:
            print("No item is selected...")
            return []