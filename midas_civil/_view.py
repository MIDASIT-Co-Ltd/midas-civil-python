from ._mapi import *
from ._model import *



class View:

    def Capture(location="D:\\API_temp\\img3.jpg",img_w = 1280 , img_h = 720,view='',stage:str=''):
        ''' Location - image location
            Image height and width
            View - 'pre' or 'post'
            stage - CS name
        '''
        json_body = {
                "Argument": {
                    "EXPORT_PATH": location,
                    "HEIGHT": img_h,
                    "WIDTH": img_w,
                    "ZOOM_LEVEL" : 100
                }
            }
        
        if view=='post':
            json_body['Argument']['SET_MODE'] = 'post'
        elif view=='pre':
            json_body['Argument']['SET_MODE'] = 'pre'

        if stage != '':
            json_body['Argument']['STAGE_NAME'] = stage

        MidasAPI('POST','/view/CAPTURE',json_body)