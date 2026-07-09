from ._mapi import MidasAPI



class Story:
    data:list['Story'] = []

    def __init__(self,name:str,level:float,
                 floor_width_X = 0, floor_width_Y = 0, floor_cent_X=0, floor_cent_Y=0,  wind_ecc_X =0 ,  wind_ecc_Y =0 , 
                 seis_acc_ecc_X = 0,seis_acc_ecc_Y = 0, seis_inh_ecc_X = 0,seis_inh_ecc_Y = 0, seis_torAmp_fac_X = 1 , seis_torAmp_fac_Y = 1,
                 bFloorDiaph=True,
                 id:int=None):
        
        self.LEVEL = level
        self.NAME = name

        self.WIDTH_X = floor_width_X
        self.WIDTH_Y = floor_width_Y

        self.CENTER_X = floor_cent_X
        self.CENTER_Y = floor_cent_Y

        self.WIND_ECCEN_X = wind_ecc_X
        self.WIND_ECCEN_Y = wind_ecc_Y

        self.SEIS_ACC_ECCEN_X = seis_acc_ecc_X
        self.SEIS_ACC_ECCEN_Y = seis_acc_ecc_Y

        self.SEIS_INH_ECCEN_X = seis_inh_ecc_X
        self.SEIS_INH_ECCEN_Y = seis_inh_ecc_Y

        self.SEIS_TOR_AMPFAC_X = seis_torAmp_fac_X
        self.SEIS_TOR_AMPFAC_Y = seis_torAmp_fac_Y

        self.bFLOOR_DIAPH = bFloorDiaph


        if id is None: self.ID = len(Story.data) + 1
        else: self.ID = id

        Story.data.append(self)

    @classmethod
    def json(cls):
        """Creates JSON from objects defined in Python"""
        json_data = {"Assign": {}}
        for story in cls.data:
            json_data["Assign"][str(story.ID)] = {
                "STORY_NAME": story.NAME,
                "STORY_LEVEL": story.LEVEL,
                "bFLOOR_DIAPHRAGM": story.bFLOOR_DIAPH,
                "WIND_FLOOR_WIDTH_X": story.WIDTH_X,
                "WIND_FLOOR_WIDTH_Y": story.WIDTH_Y,
                "WIND_CENTER_X": story.CENTER_X,
                "WIND_CENTER_Y": story.CENTER_Y,
                "WIND_ECCENT_X": story.WIND_ECCEN_X,
                "WIND_ECCENT_Y": story.WIND_ECCEN_Y,
                "SEIS_ACC_ECCENT_X": story.SEIS_ACC_ECCEN_X,
                "SEIS_ACC_ECCENT_Y": story.SEIS_ACC_ECCEN_Y,
                "SEIS_INHERENT_ECCENT_X": story.SEIS_INH_ECCEN_X,
                "SEIS_INHERENT_ECCENT_Y": story.SEIS_INH_ECCEN_Y,
                "SEIS_TORSIONAL_AMP_FACTOR_X": story.SEIS_TOR_AMPFAC_X,
                "SEIS_TORSIONAL_AMP_FACTOR_Y": story.SEIS_TOR_AMPFAC_Y
            }
        return json_data
    
    @staticmethod
    def create():
        """Creates Story in MIDAS Civil NX"""
        MidasAPI("PUT", "/db/STOR", Story.json())
    
    @staticmethod
    def get():
        """Get the JSON from MIDAS Civil NX"""
        return MidasAPI("GET", "/db/STOR")
    
    @staticmethod
    def delete():
        """Delete from MIDAS Civil NX and Python"""
        Story.clear()
        return MidasAPI("DELETE", "/db/STOR")

    @staticmethod
    def clear():
        """Delete data from Python"""
        Story.data = []

    @staticmethod
    def sync():
        """Retrieve all data from MIDAS Civil NX and rebuild the local database.

        Clears the current database, fetches all nodes via ``GET /db/STOR``,
        and recreates the local database.
        """
        Story.clear()
        a = Story.get()
        if a != {'message': ''}:
            if list(a['STOR'].keys()) != []:
                for j in a['STOR'].keys():
                    Story(a["STOR"][j]['STORY_LEVEL'],a["STOR"][j]['STORY_NAME'],int(j))

    @staticmethod
    def autoGenerate():
        '''AUTO GENERATE STORY DATA'''
        from ._model import Model,Node
        Story.clear()

        floorKeys = {}
        for nd in Node.nodes:
            floorKeys[int(nd.Z*100)]=None

        floor_levels = [float(key)/100 for key in floorKeys.keys()]

        nFloorLevels = len(floor_levels)
        for i in range(nFloorLevels):

            level= floor_levels[i]

            lvl_Nodes = Model.Select.Plane_XY((0,0,level),'NODE')

            min_x = 0
            max_x = 0
            min_y = 0
            max_y = 0

            for nd in lvl_Nodes:
                min_x = min(min_x,nd.X)
                max_x = max(max_x,nd.X)
                min_y = min(min_y,nd.Y)
                max_y = max(max_y,nd.Y)

            WIDTH_X = max_x-min_x
            WIDTH_Y = max_y-min_y

            CEN_X = 0.5*(max_x+min_x)
            CEN_Y = 0.5*(max_y+min_y)

            # print(f'HEIGHT = {level} | {WIDTH_X=}  |  {WIDTH_Y=}')

            if i==0:
                Story('GF',level,WIDTH_X,WIDTH_Y,CEN_X,CEN_Y,bFloorDiaph=False)
            elif i==nFloorLevels-1:
                Story('Roof',level,WIDTH_X,WIDTH_Y,CEN_X,CEN_Y,)
            else:
                Story(f'{i} F',level,WIDTH_X,WIDTH_Y,CEN_X,CEN_Y)

