from ._offsetSS import Offset
from ._offsetSS import _common


from math import hypot

def _poly_dir(poly,rot='CCW'):
    import numpy as np
    outer_cg = np.mean(poly,axis=0)
    outer_t = np.subtract(poly,outer_cg)
    dir = 0
    for i in range(len(poly)-1):
        dir+=outer_t[i][0]*outer_t[i+1][1]-outer_t[i][1]*outer_t[i+1][0]
    if dir < 0:
        poly.reverse()
    
    if rot == 'CW':
        poly.reverse()

    return poly







class _SS_TAP_PSC_Value(_common):
    def __init__(self,Name:str,
                    OuterPolygon_I:list,OuterPolygon_J:list,
                    InnerPolygon_I:list=[],InnerPolygon_J:list=[],
                    Offset:Offset=Offset.CC(),useShear=True,use7Dof=False,id:int=0):
        
        '''
            Outer Polygon -> List of points ; Last input is different from first
                [(0,0),(1,0),(1,1),(0,1)]
            Inner Polygon -> List of points ; Last input is different from first
                Only one inner polygon
        '''
        
        self.ID = id
        self.NAME = Name
        self.SHAPE = 'VALU'
        self.TYPE = 'TAPERED'

        self.OFFSET = Offset
        self.USESHEAR = bool(useShear)
        self.USE7DOF = bool(use7Dof)

        self.OUTER_POLYGON_I = _poly_dir(OuterPolygon_I)
        self.INNER_POLYGON_I = []
        self.N_INNER_POLYGON = 0

        self.OUTER_POLYGON_J = _poly_dir(OuterPolygon_J)
        self.INNER_POLYGON_J = []

        temp_arr_I = [] 
        temp_arr_J = []

        n_inner_J = 0


        # Finding no. of internal polygons
        if InnerPolygon_I != []:
            if not isinstance(InnerPolygon_I[0][0],(int,float)):
                self.N_INNER_POLYGON = len(InnerPolygon_I)
                temp_arr_I = InnerPolygon_I 
                
            else:
                temp_arr_I.append(InnerPolygon_I) #Convert to list
                self.N_INNER_POLYGON = 1

        for i in range(len(temp_arr_I)):
            self.INNER_POLYGON_I.append(_poly_dir(temp_arr_I[i],'CW'))

        
        if InnerPolygon_J != []:
            if not isinstance(InnerPolygon_J[0][0],(int,float)):
                n_inner_J = len(InnerPolygon_J)
                temp_arr_J = InnerPolygon_J 
            else:
                temp_arr_J.append(InnerPolygon_J) #Convert to list
                n_inner_J = 1

        for i in range(len(temp_arr_J)):
            self.InnerPolygon_J.append(_poly_dir(temp_arr_J[i],'CW'))

        if n_inner_J != self.N_INNER_POLYGON:
            print("  ⚠️ Number of inner polygons don't match")


    def __str__(self):
         return f'  >  ID = {self.ID}   |  PSC VALUE SECTION \nJSON = {self.toJSON()}\n'


    def toJSON(sect):
        js =  {
                    "SECTTYPE": sect.TYPE,
                    "SECT_NAME": sect.NAME,
                    "CALC_OPT": True,
                    "SECT_BEFORE": {
                        "SHAPE": sect.SHAPE,
                        "SECT_I": {
                            "vSIZE": [0.1, 0.1, 0.1, 0.1],
                            "OUTER_POLYGON": [
                                {
                                    "VERTEX": [
                                        {"X": 5, "Y": 5},
                                        {"X": -5, "Y": 5}
                                    ]
                                }
                            ]
                        },
                        "SECT_J": {
                            "vSIZE": [0.1, 0.1, 0.1, 0.1],
                            "OUTER_POLYGON": [
                                {
                                    "VERTEX": [
                                        {"X": 5, "Y": 5},
                                        {"X": -5, "Y": 5}
                                    ]
                                }
                            ]
                        },
                        "Y_VAR": 1,
                        "Z_VAR": 1,
                        "SHEAR_CHK": True,
                        "SHEAR_CHK_POS": [[0.1, 0, 0.1], [0, 0, 0]],
                        "USE_AUTO_QY": [[True, True, True], [False, False, False]],
                        "WEB_THICK": [0, 0],
                        "USE_WEB_THICK_SHEAR": [[True, True, True], [False, False, False]]
                    }
                }
        
        v_list_I = []
        v_list_J = []
        for i in sect.OUTER_POLYGON_I:
            v_list_I.append({"X":i[0],"Y":i[1]})
        js["SECT_BEFORE"]["SECT_I"]["OUTER_POLYGON"][0]["VERTEX"] =v_list_I

        for i in sect.OUTER_POLYGON_J:
            v_list_J.append({"X":i[0],"Y":i[1]})
        js["SECT_BEFORE"]["SECT_J"]["OUTER_POLYGON"][0]["VERTEX"] =v_list_J

        

        if sect.N_INNER_POLYGON > 0 :

            js["SECT_BEFORE"]["SECT_I"]["INNER_POLYGON"]= []
            js["SECT_BEFORE"]["SECT_J"]["INNER_POLYGON"]= []

            mult_ver_I = []
            mult_ver_J = []
            for n in range(sect.N_INNER_POLYGON):
                vi_list_I = []
                vi_list_J = []

                js["SECT_BEFORE"]["SECT_I"]["INNER_POLYGON"]= [
                    {
                        "VERTEX": []
                    }
                ]
                js["SECT_BEFORE"]["SECT_J"]["INNER_POLYGON"]= [
                    {
                        "VERTEX": []
                    }
                ]

                for i in sect.INNER_POLYGON_I[n]:
                    vi_list_I.append({"X":i[0],"Y":i[1]})
                for i in sect.INNER_POLYGON_J[n]:
                    vi_list_J.append({"X":i[0],"Y":i[1]})

                ver_json_I = {"VERTEX": vi_list_I}
                mult_ver_I.append(ver_json_I)
                ver_json_J = {"VERTEX": vi_list_J}
                mult_ver_J.append(ver_json_J)

            js["SECT_BEFORE"]["SECT_I"]["INNER_POLYGON"] = vi_list_I
            js["SECT_BEFORE"]["SECT_J"]["INNER_POLYGON"] = vi_list_J

        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js
    

    # @staticmethod
    # def _objectify(id,name,type,shape,offset,uShear,u7DOF,js):

    #     outer_pt = []
    #     for pt in js["SECT_BEFORE"]["SECT_I"]["OUTER_POLYGON"][0]["VERTEX"]:
    #         outer_pt.append((pt['X'],pt['Y']))

    #     inner_pt = []
    #     if 'INNER_POLYGON' in js["SECT_BEFORE"]["SECT_I"]:
    #         innerJSON = js["SECT_BEFORE"]["SECT_I"]['INNER_POLYGON']
    #         for n_holes in innerJSON:
    #             h_pt = []
    #             for pt in n_holes['VERTEX']:
    #                 h_pt.append([pt['X'],pt['Y']])
    #             inner_pt.append(h_pt)

    #     return _SS_Tap_PSC_Value(name,outer_pt,inner_pt,outer_pt,inner_pt,offset,uShear,u7DOF,id)