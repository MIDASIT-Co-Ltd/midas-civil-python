import polars as pl
import json
import xlsxwriter
from ._mapi import *
from ._model import *

from ._mapi import _getUNIT
from ._mapi import _setUNIT
# js_file = open('JSON_Excel Parsing\\test.json','r')

# print(js_file)
# js_json = json.load(js_file)


#---- INPUT: JSON -> OUTPUT : Data FRAME --------- ---------
def _JSToDF_ResTable(js_json):
    res_json = {}

    c=0
    for heading in js_json["SS_Table"]["HEAD"]:
        for dat in js_json["SS_Table"]["DATA"]:
            try:
                res_json[heading].append(dat[c])
            except:
                res_json[heading]=[]
                res_json[heading].append(dat[c])

        c+=1

    res_df = pl.DataFrame(res_json)
    return(res_df)


def _Head_Data_2_DF_JSON(head,data):
    res_json = {}
    c=0
    for heading in head:
        for dat in data:
            try:
                res_json[heading].append(dat[c])
            except:
                res_json[heading]=[]
                res_json[heading].append(dat[c])

        c+=1
    return res_json
    

def _JSToDF_UserDefined(tableName,js_json,summary):

    if 'message' in js_json:
        print(f'⚠️  {tableName} table name does not exist.')
        Result.UserDefinedTables_print()
        return 'Check table name'
    
    if summary == 0:
        head = js_json[tableName]["HEAD"]
        data = js_json[tableName]["DATA"]
    elif summary > 0 :
        try :
            sub_tab1 = js_json[tableName]["SUB_TABLES"][summary-1]
            key_name = next(iter(sub_tab1))
            head = sub_tab1[key_name]["HEAD"]
            data = sub_tab1[key_name]["DATA"]
        except :
            print(' ⚠️  No Summary table exist')
            return 'No Summary table exist'


    res_json = _Head_Data_2_DF_JSON(head,data)
    res_df = pl.DataFrame(res_json)
    return(res_df)

    






# js_dat = {
#     "Argument": {
#         "TABLE_NAME": "SS_Table",
#         "TABLE_TYPE": "REACTIONG",
#         "UNIT": {
#             "FORCE": "kN",
#             "DIST": "m"
#         },
#         "STYLES": {
#             "FORMAT": "Fixed",
#             "PLACE": 12
#         }
#     }
# }

# MAPI_KEY('eyJ1ciI6InN1bWl0QG1pZGFzaXQuY29tIiwicGciOiJjaXZpbCIsImNuIjoib3R3aXF0NHNRdyJ9.da8f9dd41fee01425d8859e0091d3a46b0f252ff38341c46c73b26252a81571d')
# ss_json = MidasAPI("POST","/post/table",js_dat)
# df4 = JSToDF(ss_json)








# print(df4)
# df4.write_excel("new.xlsx",
#                 "Plate Forces",
#                 header_format={"bold":True},
#                 autofit=True,
#                 autofilter=True,
#                 table_style="Table Style Light 8"
#                 )


# with xlsxwriter.Workbook("test2.xlsx") as Wb:
#     ws = Wb.add_worksheet()

#     df4.write_excel(Wb,"Sheet 1",table_style="Table Style Light 8",autofit=True)

#     df4.write_excel(Wb,"Sheet 1",table_style="Table Style Light 8",autofit=True,autofilter=False,position="A31",include_header=False)





class Result :

    # ---------- User defined TABLE (Dynamic Report Table) ------------------------------
    @staticmethod
    def UserDefinedTable(tableName:str, summary=0, force_unit='KN',len_unit='M'):
        js_dat = {
            "Argument": {
                "TABLE_NAME": tableName,
                "STYLES": {
                    "FORMAT": "Fixed",
                    "PLACE": 5
                }
            }
        }
        currUNIT = _getUNIT()
        Model.units(force=force_unit,length=len_unit)
        ss_json = MidasAPI("POST","/post/TABLE",js_dat)
        _setUNIT(currUNIT)
        return _JSToDF_UserDefined(tableName,ss_json,summary)
    
    # ---------- LIST ALL USER DEFINED TABLE ------------------------------
    @staticmethod
    def UserDefinedTables_print():
        ''' Print all the User defined table names '''
        ss_json = MidasAPI("GET","/db/UTBL",{})
        table_name =[]
        try:
            for id in ss_json['UTBL']:
                table_name.append(ss_json["UTBL"][id]['NAME'])
            
            print('Available user-defined tables in Civil NX are : ')
            print(*table_name,sep=' , ')
        except:
            print(' ⚠️  There are no user-defined tables in Civil NX')



    # ---------- Result TABLE (For ALL TABLES)------------------------------
    @staticmethod
    def ResultTable(tabletype:str,keys=[],loadcase:list=[],cs_stage=[],force_unit='KN',len_unit='M'):
        '''
            TableType : REACTIONG | REACTIONL | DISPLACEMENTG | DISPLACEMENTL | TRUSSFORCE | TRUSSSTRESS
            Keys : List{int} -> Element/ Node IDs  |  str -> Structure Group Name
            Loadcase : Loadcase/Combination name followed by type. eg. DeadLoad(ST)
        '''

        js_dat = {
            "Argument": {
                "TABLE_NAME": "SS_Table",
                "TABLE_TYPE": tabletype,
                "STYLES": {
                    "FORMAT": "Fixed",
                    "PLACE": 5
                }
            }
        }

        if cs_stage !=[]:
            if cs_stage == 'all' :
                js_dat["Argument"]['OPT_CS'] = True
            else:
                js_dat["Argument"]['OPT_CS'] = True
                js_dat["Argument"]['STAGE_STEP'] = cs_stage


        if isinstance(keys,list):
            if keys!=[]:
                js_dat["Argument"]['NODE_ELEMS'] = {"KEYS": keys}
        elif isinstance(keys,str):
            js_dat["Argument"]['NODE_ELEMS'] = {"STRUCTURE_GROUP_NAME": keys}


        if loadcase!=[]: js_dat["Argument"]['LOAD_CASE_NAMES'] = loadcase

        currUNIT = _getUNIT()
        Model.units(force=force_unit,length=len_unit)
        ss_json = MidasAPI("POST","/post/table",js_dat)
        _setUNIT(currUNIT)
        return _JSToDF_ResTable(ss_json)
    

    class TABLE :
        
        @staticmethod
        def BeamForce_VBM(keys=[],loadcase:list=[],items=['all'],parts=["PartI", "PartJ"],components=['all'],force_unit='KN',len_unit='M'):
            '''
                Keys : List{int} -> Element/ Node IDs  |  str -> Structure Group Name
                Loadcase : Loadcase/Combination name followed by type. eg. ["DeadLoad(ST)"]
                Items to display : [ "Axial" , "Shear-y" , "Shear-z" , "Torsion" , "Moment-y" , "Moment-z"]
                Parts : ["PartI", "Part1/4", "Part2/4", "Part3/4", "PartJ"]
                Components (colms of tabulart result): [ "Elem", "Load", "Part", "Component", "Axial", "Shear-y", "Shear-z", "Torsion", "Moment-y", "Moment-z" ]
                
            '''

            js_dat = {
                "Argument": {
                    "TABLE_NAME": "SS_Table",
                    "TABLE_TYPE": "BEAMFORCEVBM",
                    "STYLES": {
                        "FORMAT": "Fixed",
                        "PLACE": 5
                    },
                    "PARTS" : parts
                }
            }


            if isinstance(keys,list):
                if keys!=[]:
                    js_dat["Argument"]['NODE_ELEMS'] = {"KEYS": keys}
            elif isinstance(keys,str):
                js_dat["Argument"]['NODE_ELEMS'] = {"STRUCTURE_GROUP_NAME": keys}


            if loadcase!=[]: js_dat["Argument"]['LOAD_CASE_NAMES'] = loadcase

            if components!=['all']:
                if "Elem" not in components: components.append("Elem")
                if "Load" not in components: components.append("Load")
                if "Part" not in components: components.append("Part")
                if "Component" not in components: components.append("Component")
                js_dat["Argument"]['COMPONENTS'] = components
            
            if items!=['all']:
                js_dat["Argument"]['ITEM_TO_DISPLAY'] = items



            currUNIT = _getUNIT()
            Model.units(force=force_unit,length=len_unit)
            ss_json = MidasAPI("POST","/post/table",js_dat)
            _setUNIT(currUNIT)
            return _JSToDF_ResTable(ss_json)

