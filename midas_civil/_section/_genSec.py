from ._offsetSS import Offset
from ._offsetSS import _common 


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



class _SS_GENERAL(_common):
    
    def __init__(self,shape1,shape2=None,shape3=None,shape4=None, 
                 Name:str='TEST_NAME',Offset:Offset=Offset('CC'),useShear:bool=True,use7Dof:bool=False,id:int=None):
        self.N_PARTS = 0

        # if shape1!=None and not isinstance(shape1,SEC_SHAPE):
        #     shape1 = SEC_SHAPE(shape1)


        self.BASE_MAT = shape1.MAT

        self.PARTS = []
        for s in [shape1, shape2, shape3, shape4]:
            if s is not None:
                # if isinstance(s,SHAPE):
                #     s = SHAPE(s)
                self.PARTS.append(s)
                self.N_PARTS+=1

        # ONLY USED FOR PLOTTING
        self.PART_1 = shape1
        self.PART_2 = shape2
        self.PART_3 = shape3
        self.PART_4 = shape4


        self.ID = id
        self.NAME = Name

        if self.N_PARTS > 1:
            self.TYPE = 'COMPOSITE-GEN' # COMP GEN
            self.SHAPE = 'CP_G'
        else:
            self.TYPE = 'PSC' # VALUE
            self.SHAPE = 'VALU'

        self.OFFSET = Offset
        self.USESHEAR = useShear
        self.USE7DOF = use7Dof
        

    def plot(sect):
        import matplotlib.pyplot as plt

        if sect.PART_1 !=None: sect.PART_1.__createSHAPE__("#c394f840")
        if sect.PART_2 !=None: sect.PART_2.__createSHAPE__("#8ee6d740")
        if sect.PART_3 !=None: sect.PART_3.__createSHAPE__("#e26d9040")
        if sect.PART_4 !=None: sect.PART_4.__createSHAPE__("#dd986040")


        plt.grid(False)
        plt.axis('equal')   # Optional: equal scaling on both axes
        plt.show()
    
    def toJSON(sect):
        if sect.TYPE == 'COMPOSITE-GEN':
            _genPart = []
            _c_outer = 0
            _c_inner = 0

            _OUTERPOLY = []
            _INNERPOLY = []

            base_den = sect.BASE_MAT[2]
            for i,part in enumerate(sect.PARTS):
                _isBase = False
                if i==0: _isBase = True

                genJS = {
                        "DENS_RATIO": part.MAT[2]/base_den,
                        "ELAST": part.MAT[0],
                        "POISSON": part.MAT[1],
                        "USE_BASE_MATL": _isBase,
                        "USE_PLANE": True,
                        "IDX_START": [
                            _c_outer,
                            _c_inner,
                            0,
                            0,
                            0
                        ],
                        "IDX_END": [
                            _c_outer+part.N_OUTER,
                            _c_inner+part.N_INNER,
                            0,
                            0,
                            0
                        ]
                    }
                _genPart.append(genJS)
                _c_outer+=part.N_OUTER
                _c_inner+=part.N_INNER


                # OUTER POLY
                for outerPts in part.OUTER:
                    newPTS = _poly_dir(outerPts,'CCW')
                    vert = []
                    for loc in newPTS:
                        vert.append({"X":loc[0] , "Y":loc[1]})

                    _OUTERPOLY.append({"VERTEX":vert})
                
                # INNER POLY
                for innerPts in part.INNER:
                    newPTS = _poly_dir(innerPts,'CW')
                    vert = []
                    for loc in newPTS:
                        vert.append({"X":loc[0] , "Y":loc[1]})

                    _INNERPOLY.append({"VERTEX":vert})


            js =  {
                    "SECTTYPE": sect.TYPE,
                    "SECT_NAME": sect.NAME,
                    "SECT_BEFORE": {
                        "SHAPE": sect.SHAPE,
                        "SECT_I": {
                            "BUILT_FLAG":1,
                            "BEFORE_PART_NUM":1,
                            "GENERAL_PART":_genPart,
                        },
                        "CALC_STIFF_OPT":1
                    }
                }
            # for part in sect.SHAPE.PARTS:

            if _OUTERPOLY: js['SECT_BEFORE']["SECT_I"]["OUTER_POLYGON"] = _OUTERPOLY
            if _INNERPOLY: js['SECT_BEFORE']["SECT_I"]["INNER_POLYGON"] = _INNERPOLY

        elif sect.TYPE == 'PSC':
            js =  {
                    "SECTTYPE": sect.TYPE,
                    "SECT_NAME": sect.NAME,
                    "CALC_OPT": True,
                    "SECT_BEFORE": {
                        "SHAPE": sect.SHAPE,
                        "SECT_I": {
                            "SECT_NAME": "",
                            "vSIZE": [0.1, 0.1, 0.1, 0.1],
                        },
                        "SHEAR_CHK": True,
                        "SHEAR_CHK_POS": [[0, 0, 0], [0, 0, 0]],
                        "USE_AUTO_QY": [[True, True, True], [False, False, False]],
                        "WEB_THICK": [0, 0],
                        "USE_WEB_THICK_SHEAR": [[True, True, True], [False, False, False]]
                    }
                }
            _OUTERPOLY = []
            _INNERPOLY = []


            part = sect.PARTS[0]
            for outerPts in part.OUTER:
                    newPTS = _poly_dir(outerPts,'CCW')
                    vert = []
                    for loc in newPTS:
                        vert.append({"X":loc[0] , "Y":loc[1]})

                    _OUTERPOLY.append({"VERTEX":vert})
                
            # INNER POLY
            for innerPts in part.INNER:
                newPTS = _poly_dir(innerPts,'CW')
                vert = []
                for loc in newPTS:
                    vert.append({"X":loc[0] , "Y":loc[1]})

                _INNERPOLY.append({"VERTEX":vert})







            if _OUTERPOLY: js['SECT_BEFORE']["SECT_I"]["OUTER_POLYGON"] = _OUTERPOLY
            if _INNERPOLY: js['SECT_BEFORE']["SECT_I"]["INNER_POLYGON"] = _INNERPOLY


        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js

