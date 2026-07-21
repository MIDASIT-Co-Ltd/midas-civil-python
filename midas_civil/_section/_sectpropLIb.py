from ._offsetSS import Offset
from ._offsetSS import _common
from math import sin , cos , pi
from typing import TypeVar

sectionProp = TypeVar('sectionproperties.analysis.Section')

class _SS_SECTPROP(_common):

    """ Create section from section properties"""
    from sectionproperties.analysis import Section

    def __init__(self,section:sectionProp,Name='',Offset=Offset(),useShear=True,use7Dof=False,id:int=0):  
        """ Shape = 'SB' 'SR' for rectangle \n For cylinder"""


        self.ID = id
        self.NAME = Name
        self.TYPE = 'VALUE'
        self.OFFSET = Offset
        self.USESHEAR = useShear
        self.USE7DOF = use7Dof
        self.SECTION = section
    
    def __str__(self):
         return f'  >  ID = {self.ID}   |  USER DEFINED STANDARD SECTION \nJSON = {self.toJSON()}\n'


    def toJSON(sect):
        js =  {
                "SECTTYPE": sect.TYPE,
                "SECT_NAME": sect.NAME,
                "SECT_BEFORE": {
                    "SHAPE": "GEN",
                    "SECT_I": {
                        "PERIIN":0,
                        "PERIOUT":0,
                        "BUILT_FLAG":1,
                        "OUTER_POLYGON":[],
                        "INNER_POLYGON":[],
                        "STIFF":{"AREA":1},
                        "DESIGN" : {}
                    },
                    "CALC_STIFF_OPT":1
                }
            }

        # GET VERTEX DATA
        geometry = sect.SECTION.geometry
        _avail_data = geometry.__dict__.keys()

        if 'geoms' in _avail_data:
            print("IT IS A MULTI SECTION")
            geos = geometry.geoms
        else:
            print("THIS IS A SIMPLE SECTION")
            geos = [geometry]



        #-------- MULTIPLE ONE ----------------
        outerP = []
        innerP = []
        peri_inner = 0
        min_x, min_y , max_x, max_y = 0,0,0,0
        for g in geos:
            _min_x, _min_y , _max_x, _max_y = g.geom.bounds
            min_x = min(min_x,_min_x)
            min_y = min(min_y,_min_y)
            max_x = max(max_x,_max_x)
            max_y = max(max_y,_max_y)

            vert = []
            coords = list(g.geom.exterior.coords)
            for loc in coords:
                vert.append({"X":loc[0] , "Y":loc[1]})

            outerP.append({"VERTEX":vert})

            for hole in g.geom.interiors:
                peri_inner+=hole.length
                vert = []
                coords = list(hole.coords)
                for loc in coords:
                    vert.append({"X":loc[0] , "Y":loc[1]})
                
                innerP.append({"VERTEX":vert})

        #---- GET SECT PROPS ----
        sect.SECTION.calculate_geometric_properties()
        # sect.SECTION.calculate_warping_properties()
        # sect.SECTION.calculate_plastic_properties()

        js['SECT_BEFORE']['SECT_I']['STIFF']['AREA'] = sect.SECTION.get_area()
        # js['SECT_BEFORE']['SECT_I']['STIFF']['ASY'] = sect.SECTION.get_as()[0]
        # js['SECT_BEFORE']['SECT_I']['STIFF']['ASZ'] = sect.SECTION.get_as()[1]


        cx,cy = sect.SECTION.get_c()
        js['SECT_BEFORE']['SECT_I']['STIFF']['CYM'] = cx
        js['SECT_BEFORE']['SECT_I']['STIFF']['CZM'] = cy

        # js['SECT_BEFORE']['SECT_I']['STIFF']['CYP'] = sect.SECTION.get_pc()[0]
        # js['SECT_BEFORE']['SECT_I']['STIFF']['CZP'] = sect.SECTION.get_pc()[1]


        # js['SECT_BEFORE']['SECT_I']['STIFF']['RYY'] = sect.SECTION.get_ic()[0]
        # js['SECT_BEFORE']['SECT_I']['STIFF']['RZZ'] = sect.SECTION.get_ic()[1]
        # js['SECT_BEFORE']['SECT_I']['STIFF']['RXX'] = sect.SECTION.get_j()

        js['SECT_BEFORE']['SECT_I']['STIFF']['Y'] = [min_x-cx,max_x-cx,max_x-cx,min_x-cx]
        js['SECT_BEFORE']['SECT_I']['STIFF']['Z'] = [max_y-cy,max_y-cy,min_y-cy,min_y-cy]

        # js['SECT_BEFORE']['SECT_I']['PERIOUT'] = sect.SECTION.get_perimeter()
        # js['SECT_BEFORE']['SECT_I']['PERIIN'] = peri_inner
        js['SECT_BEFORE']['SECT_I']['DESIGN'] = {"YBAR":cx , "ZBAR":cy}

        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['SECT_I']['OUTER_POLYGON'] = outerP
        js['SECT_BEFORE']['SECT_I']['INNER_POLYGON'] = innerP
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js
