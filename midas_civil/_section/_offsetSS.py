from midas_civil import MidasAPI

class Offset:
    def __init__(self,OffsetPoint='CC',CenterLocation=0,HOffset=0,HOffOpt=0,VOffset=0,VOffOpt=0,UsrOffOpt=0):

        # self.OFFSET_PT =OffsetPoint
        # self.OFFSET_CENTER =CenterLocation
        # self.HORZ_OFFSET_OPT = HOffOpt
        # self.USERDEF_OFFSET_YI = HOffset
        # self.USERDEF_OFFSET_YJ = HOffset
        # self.VERT_OFFSET_OPT = VOffOpt
        # self.USERDEF_OFFSET_ZI = VOffset
        # self.USERDEF_OFFSET_ZJ = VOffset
        # self.USER_OFFSET_REF = UsrOffOpt

        self.JS = {
            "OFFSET_PT": OffsetPoint,
            "OFFSET_CENTER": CenterLocation,

            "USER_OFFSET_REF": UsrOffOpt,
            "HORZ_OFFSET_OPT": HOffOpt,
            "USERDEF_OFFSET_YI": HOffset,

            "USERDEF_OFFSET_YJ": HOffset,   #Tapered only

            "VERT_OFFSET_OPT": VOffOpt,
            "USERDEF_OFFSET_ZI": VOffset,

            "USERDEF_OFFSET_ZJ": VOffset,   #Tapered only
        }


    def __str__(self):
        return str(self.JS)
    
    @staticmethod
    def CC():
        return Offset()
    
    @staticmethod
    def CT():
        return Offset('CT')
    
    @staticmethod
    def CB():
        return Offset('CB')
    

class _common:
    def update(self):
        js2s = {'Assign':{self.ID : self.toJSON()}}
        MidasAPI('PUT','/db/sect',js2s)
        return js2s