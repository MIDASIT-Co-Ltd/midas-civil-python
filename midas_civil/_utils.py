# from ._model import *
# from ._mapi import *
from __future__ import annotations
from scipy.interpolate import splev, splrep ,CubicSpline , Akima1DInterpolator , PchipInterpolator
from math import hypot,sqrt
import numpy as np
from ._mapi  import MidasAPI


#Function to remove duplicate set of values from 2 lists
# def unique_lists(li1, li2):
#     if type (li1) == list and type (li2) == list:
#         if len(li1) == len(li2):
#             indices_to_remove = []
#             for i in range(len(li1)):
#                 for j in range(i+1,len(li1)):
#                     if li1[i] == li1[j] and li2[i] == li2[j]:
#                         indices_to_remove.append(j)
#             for index in sorted(indices_to_remove, reverse = True):
#                 del li1[index]
#                 del li2[index]


# def sect_inp(sec):
#     """Section ID.  Enter one section id or list of section IDs.  Sample:  sect_inp(1) OR sect_inp([3,2,5])"""
#     Model.units()
#     a = MidasAPI("GET","/db/SECT",{"Assign":{}})
#     if type(sec)==int: sec = [sec]
#     b={}
#     for s in sec:
#         if str(s) in a['SECT'].keys() : b.update({s : a['SECT'][str(s)]})
#     # if elem = [0] and sec!=0: b.update({sec : })
#     if b == {}: b = "The required section ID is not defined in connected model file."
#     return(b)
#---------------------------------------------------------------------------------------------------------------



def sFlatten(list_of_list):
    # list_of_list = [list_of_list]
    return [item for elem in list_of_list for item in (elem if isinstance(elem, list) else [elem])]

# def getID_orig(element_list):
#     """Return ID of Node and Element"""
#     return [beam.ID for beam in sFlatten(element_list)]

def getID(*objects):
    objects = list(objects)
    _getID2(objects)
    return objects

def _getID2(objects):
    for i in range(len(objects)):
        if isinstance(objects[i], list):
            _getID2(objects[i])  # Recursive call for sublist
        else:
            objects[i] = objects[i].ID



def getNodeID(*objects):
    objects = list(objects)
    _getNodeID2(objects)
    return objects

def _getNodeID2(objects):
    for i in range(len(objects)):
        if isinstance(objects[i], list):
            _getNodeID2(objects[i])  # Recursive call for sublist
        else:
            objects[i] = objects[i].NODES




# def getNodeID_orig(element_list):
#     """Return Node IDs of Element"""
#     # return list(sFlatten([beam.NODES for beam in sFlatten(element_list)]))
#     return list(sFlatten([beam.NODES for beam in sFlatten(element_list)]))


def arr2csv(nlist):
    strinff = ",".join(map(str,nlist))
    return strinff

def zz_add_to_dict(dictionary, key, value):
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]


def _convItem2List(item):
    if isinstance(item,(list,np.ndarray)):
        return item
    return [item]

def _matchArray(A,B):
    '''Matches B to length of A   
    Return B'''
    A = _convItem2List(A)
    B = _convItem2List(B)
    n = len(A)
    if len(B) >= n:
        return B[:n]
    return B + [B[-1]] * (n - len(B))

def _longestList(A,B):
    """ Matches A , B list and returns the list with longest length with last element repeated """
    A = _convItem2List(A)
    B = _convItem2List(B)
    nA = len(A)
    nB = len(B)

    if nA >= nB:
        return (A , B + [B[-1]] * (nA - nB))
    return (A + [A[-1]] * (nB - nA),B)




class utils:
    ''' Contains helper function and utilities'''
    class Alignment:
        '''Defines alignment object passing through the points'''
        def __init__(self,points,type: str = 'cubic'):
            ''' 
            **POINTS** -> Points on the alignment [[x,y] , [x,y] , [x,y] ....]   
            **TYPE** -> Type of interpolating curve
                    cubic , akima , makima , pchip
            '''


            _pt_x = [pt[0] for pt in points]
            _pt_y = [pt[1] for pt in points]

            # _alignment = splrep(_pt_x, _pt_y)
            if type == 'akima':
                _alignment = Akima1DInterpolator(_pt_x, _pt_y,method='akima')
            elif type == 'makima':
                _alignment = Akima1DInterpolator(_pt_x, _pt_y,method='makima')
            elif type == 'pchip':
                _alignment = PchipInterpolator(_pt_x, _pt_y)
            else :
                _alignment = CubicSpline(_pt_x, _pt_y)

            # _alignSlope = Akima1DInterpolator(_pt_x, _pt_y,method='akima') # Used for slope calculation

            _n=500
            # INITIAL ALGINMENT - Mapping U parameter to X (based on Distance)
            _x_fine = np.linspace(_pt_x[0],_pt_x[-1],_n)

            _y_fine = _alignment(_x_fine)

            _dx = np.diff(_x_fine)
            _dy = np.diff(_y_fine)

            _dl=[]
            for i in range(len(_dx)):
                _dl.append(hypot(_dx[i],_dy[i]))

            _cumLength = np.insert(np.cumsum(_dl),0,0)
            _totalLength = _cumLength[-1]

            _u_fine = _cumLength/_totalLength

            self.ALIGNMENT = _alignment
            # self.ALIGNSLOPE = _alignSlope
            self.TOTALLENGTH = _totalLength
            self.CUMLENGTH = _cumLength
            self.PT_X = _pt_x
            self.PT_Y = _pt_y
            self.X_FINE = _x_fine
            self.Y_FINE = _y_fine
            self.U_FINE = _u_fine

        @staticmethod
        def transformPoint(point:tuple,initial_align:utils.Alignment,final_align:utils.Alignment) -> list :
            ''' 
            Transforms a point (x,y) => [X , Y]    
            Maps a point (x,y) wrt Initial alignment curve to a new Final alignment (X,Y)
            '''
            ptx = point[0]
            pty = point[1]
            distx = 100000 #Initial high distance
            idx = 0
            y_ref = 0
            fact = 10000
            for q in range(101):
                x_onLine1 = ptx+initial_align.TOTALLENGTH*(q-50)/fact
                if x_onLine1 < initial_align.PT_X[0]:
                    continue
                if x_onLine1 > initial_align.PT_X[-1]:
                    break
                # y_onLine1 = splev(x_onLine1, initial_align.ALIGNMENT)
                y_onLine1 = initial_align.ALIGNMENT(x_onLine1)
                dist = hypot(ptx-x_onLine1,pty-y_onLine1)
                if dist <= distx:
                    distx = dist
                    idx = q
                    y_ref = y_onLine1
                # print(f"  > X location of line = {x_onLine1}  Y on Line = {y_onLine1}|   Distance = {dist}  |  Index = {q}")

            final_u = np.interp(ptx+initial_align.TOTALLENGTH*(idx-50)/fact,initial_align.X_FINE,initial_align.U_FINE)
            off = np.sign(pty-y_ref)*distx
            x2_interp = np.interp(final_u,final_align.U_FINE,final_align.X_FINE)

            # y2_interp = splev(x2_interp, final_align.ALIGNMENT)
            y2_interp = final_align.ALIGNMENT(x2_interp)

            slope = final_align.ALIGNMENT(x2_interp,1) # Tan theta

            norm = sqrt(1+slope*slope)
            x_off = -slope/norm
            y_off = 1/norm

            # print(f"Point loc = [{point}] , Index match = {idx} , Point X on Initial = {ptx+initial_align.TOTALLENGTH*(idx-50)/8000} , Point Y = {y_ref} , Distance = {off} , Xoff = {slope}")

            return (round(x2_interp+x_off*off,5),round(y2_interp+y_off*off,5))

    
    
    @staticmethod
    def LineToPlate(nDiv:int = 10 , mSizeDiv:float = 0, bRigdLnk:bool=True , meshSize:float=0.5, elemList:list=None):
        '''
        Converts selected/entered line element to Shell elements   
        **nDiv** - No. of Division along the length of span    
        **mSizeDiv** - Division based on mesh size(in meter) along the length of span   
                division based on number -> **mSizeDiv  = 0**  
                division based on meshSize(in meter) -> **nDiv = 0**   
        **bRigdLnk** - Whether to create Rigid links at the span ends  
        **meshSize** - Mesh size(in meter) of the plate elements   
        **elemList** - Element list which are to be converted . If None is passed, element are taken from selected elements in CIVIL NX  

        '''
        from ._utilsFunc._line2plate import SS_create
        SS_create(nDiv , mSizeDiv , bRigdLnk , meshSize ,elemList)
