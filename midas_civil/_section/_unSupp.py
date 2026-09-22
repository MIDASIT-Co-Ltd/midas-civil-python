from ._offsetSS import _common


def getSectCordPoints(secJS):
    sec_id = 1
    sample_js = {'SECT':{sec_id:secJS}}

    i_OuterJSON = sample_js["SECT"][sec_id]["SECT_BEFORE"]["SECT_I"]["OUTER_POLYGON"][0]["VERTEX"]
    I_OUTER_PTS = []
    for pts in i_OuterJSON:
        I_OUTER_PTS.append((pts['X'],pts['Y']))

    i_InnerJSON = sample_js["SECT"][sec_id]["SECT_BEFORE"]["SECT_I"]["INNER_POLYGON"][0]["VERTEX"]
    I_INNER_PTS = []
    for pts in i_InnerJSON:
        I_INNER_PTS.append((pts['X'],pts['Y']))

    I_INNER_PTS.reverse()

    I_MID_PTS = []
    for i in range(len(I_INNER_PTS)):
        I_MID_PTS.append((0.5*(I_OUTER_PTS[i][0]+I_INNER_PTS[i][0]),0.5*(I_OUTER_PTS[i][1]+I_INNER_PTS[i][1])))


    j_OuterJSON = sample_js["SECT"][sec_id]["SECT_BEFORE"]["SECT_J"]["OUTER_POLYGON"][0]["VERTEX"]
    J_OUTER_PTS = []
    for pts in j_OuterJSON:
        J_OUTER_PTS.append((pts['X'],pts['Y']))

    j_InnerJSON = sample_js["SECT"][sec_id]["SECT_BEFORE"]["SECT_J"]["INNER_POLYGON"][0]["VERTEX"]
    J_INNER_PTS = []
    for pts in j_InnerJSON:
        J_INNER_PTS.append((pts['X'],pts['Y']))

    J_INNER_PTS.reverse()

    J_MID_PTS = []
    for i in range(len(J_INNER_PTS)):
        J_MID_PTS.append((0.5*(J_OUTER_PTS[i][0]+J_INNER_PTS[i][0]),0.5*(J_OUTER_PTS[i][1]+J_INNER_PTS[i][1])))

    return (I_MID_PTS, J_MID_PTS , I_OUTER_PTS , J_OUTER_PTS)




class _SS_UNSUPP(_common):

    """ Store Unsupported section"""

    def __init__(self,id,name,type,shape,offset,uShear,u7DOF,js):  
        """ Shape = 'SB' 'SR' for rectangle \n For cylinder"""
        self.ID = id
        self.NAME = name
        self.TYPE = type
        self.SHAPE = shape
        self.OFFSET = offset
        self.USESHEAR = uShear
        self.USE7DOF = u7DOF
        self.DATATYPE = 2
        self.JS = js
    
    def __str__(self):
         return f'  >  ID = {self.ID}   |  Unsupported Section \nJSON = {self.JS}\n'


    def toJSON(sect):
        js = sect.JS
        js['SECT_NAME'] = sect.NAME
        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js
    

    def _centerLine(shape,end,*args):
        # TEMP IMPLEMENTATION FOR TAPERED VALUE THIN SECTION
        if shape.TYPE == 'TAPERED' and shape.SHAPE=='VALU':
            # print("CENTER ACCESSED....")
            mid_I_pts , mid_J_pts , out_I_pts , out_J_pts= getSectCordPoints(shape.JS)

            n_points = len(mid_I_pts)

            sect_lin_con = []
            for i in range(n_points-1):
                sect_lin_con.append([i+1,i+2])
            sect_lin_con.append([n_points,1])

            outer_pts = out_J_pts if end else out_I_pts
            min_x,max_x,min_y,max_y = 0,0,0,0

            for i in range(n_points):
                x,y = outer_pts[i]
                if x<min_x: min_x = x
                if x>max_x: max_x = x
                if y<min_y: min_y = y
                if y>max_y: max_y = y

            sect_cg_LT = [min_x,max_y]
            sect_cg_CC = [0.5*(min_x+max_x),0.5*(min_y+max_y)]
            sect_cg_RB = [max_x,min_y]


            sect_shape = mid_J_pts if end else mid_I_pts

            sect_thk = [0.05]*n_points
            sect_thk_off = [0]*n_points

        sect_cg = (sect_cg_LT,sect_cg_CC,sect_cg_RB)

        return sect_shape, sect_thk ,sect_thk_off, sect_cg , sect_lin_con
        return False



class _SS_STD_DB(_common):

    """ Store Unsupported section"""

    def __init__(self,id,name,type,shape,offset,uShear,u7DOF,js):  
        """ Shape = 'SB' 'SR' for rectangle \n For cylinder"""
        self.ID = id
        self.NAME = name
        self.TYPE = type
        self.SHAPE = shape
        self.OFFSET = offset
        self.USESHEAR = uShear
        self.USE7DOF = u7DOF
        self.DATATYPE = 2
        self.JS = js
    
    def __str__(self):
         return f'  >  ID = {self.ID}   |  STANDARD CODAL SECTION \nJSON = {self.JS}\n'


    def toJSON(sect):
        js = sect.JS
        js['SECT_NAME'] = sect.NAME
        js['SECT_BEFORE'].update(sect.OFFSET.JS)
        js['SECT_BEFORE']['USE_SHEAR_DEFORM'] = sect.USESHEAR
        js['SECT_BEFORE']['USE_WARPING_EFFECT'] = sect.USE7DOF
        return js