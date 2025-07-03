from ._mapi import *



def _ThikADD(self):
    # Commom HERE ---------------------------------------------
    id = int(self.ID)
    if Thickness.ids == []: 
        count = 1
    else:
        count = max(Thickness.ids)+1

    if id==0 :
        self.ID = count
        Thickness.thick.append(self)
        Thickness.ids.append(int(self.ID))
    elif id in Thickness.ids:
        self.ID=int(id)
        print(f'⚠️  Thickness with ID {id} already exist! It will be replaced.')
        index=Thickness.ids.index(id)
        Thickness.thick[index]=self
    else:
        self.ID=id        
        Thickness.thick.append(self)
        Thickness.ids.append(int(self.ID))
    # Common END -------------------------------------------------------


def _updateThik(self):
    js2s = {'Assign':{self.ID : _Obj2JS(self)}}
    MidasAPI('PUT','/db/sect',js2s)
    return js2s


def _Obj2JS(obj):

    js={
            "NAME": obj.NAME,
            "TYPE": obj.TYPE,
            "bINOUT": obj.bINOUT,
            "T_IN": obj.T_IN,
            "T_OUT": obj.T_OUT,
            "OFFSET": obj.OFF_TYPE,
            "O_VALUE": obj.OFFSET
        }
    return js



def _JS2Obj(id,js):
    name = js['NAME']
    type = js['TYPE']
    binout = js['bINOUT']
    t_in = js['T_IN']
    t_out = js['T_OUT']
    offset = js['OFFSET']
    off_value = js['O_VALUE']

    t_out2=-1
    if binout:t_out2 = t_out

    if type == 'VALUE':
        Thickness(t_in,t_out2,off_value,offset,name,id)
    


class _common:
    def __str__(self):
        return str(f'ID = {self.ID}  \nJSON : {_Obj2JS(self)}\n')

    def update(self):
        return _updateThik(self)


class Thickness(_common):
    """Create Thicknes"""
    thick = []
    ids = []

    def __init__(self,thick=0.0,thick_out=-1,offset=0,off_type='rat',name="",id=0):  
            self.ID = id
            self.NAME = name
            self.TYPE = 'VALUE'
            self.T_IN = thick
            self.bINOUT = True

            if thick_out==-1:
                self.T_OUT = thick
                self.bINOUT = False
            else: self.T_OUT = thick_out

            self.OFFSET = offset

            if off_type=='rat':
                self.OFF_TYPE = 1
            else: self.OFF_TYPE = 2

            if offset==0:
                self.OFF_TYPE =0

            _ThikADD(self)


    @classmethod
    def json(cls):
        json = {"Assign":{}}
        for sect in cls.thick:
            js = _Obj2JS(sect)
            json["Assign"][sect.ID] = js
        return json
    
    @staticmethod
    def create():
        MidasAPI("PUT","/db/THIK",Thickness.json())
        
    @staticmethod
    def get():
        return MidasAPI("GET","/db/THIK")
    
    
    @staticmethod
    def delete():
        MidasAPI("DELETE","/db/THIK")
        Thickness.thick=[]
        Thickness.ids=[]


    @staticmethod
    def sync():
        a = Thickness.get()
        if a != {'message': ''}:
            if list(a['THIK'].keys()) != []:
                Thickness.thick = []
                Thickness.ids=[]
                for sect_id in a['THIK'].keys():
                    _JS2Obj(sect_id,a['THIK'][sect_id])



