# from ._model import *
# from ._mapi import *
from __future__ import annotations
from math import hypot,sqrt
import numpy as np
from typing import Literal

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
    return [item for elem in list_of_list for item in (elem if isinstance(elem, (list,np.ndarray)) else [elem])]

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

def getLOC(objects):
    ''' Get location for multiple node objects'''
    _getLOC2(objects)
    return objects

def _getLOC2(objects):
    for i in range(len(objects)):
        if isinstance(objects[i], list):
            _getLOC2(objects[i])  # Recursive call for sublist
        else:
            objects[i] = objects[i].LOC

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


_alignType = Literal['cubic','akima','makima','pchip']

class utils:
    ''' Contains helper function and utilities'''
    __RC_Grillage_nSpan = 1
    class Alignment:
        '''Defines alignment object passing through the points
        X -> monotonous increasing'''
        
        def __init__(self,points,type: _alignType = 'cubic'):
            ''' 
            **POINTS** -> Points on the alignment [[x,y] , [x,y] , [x,y] ....]   
            **TYPE** -> Type of interpolating curve
                    cubic , akima , makima , pchip
            '''
            from scipy.interpolate import CubicSpline , Akima1DInterpolator , PchipInterpolator

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

            _n=100
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

        def getPoint(self,distance):
            x_interp = np.interp(distance,self.CUMLENGTH,self.X_FINE)
            y_interp = np.interp(distance,self.CUMLENGTH,self.Y_FINE)
            return x_interp , y_interp
        
        def getSlope(self,distance):
            'Returns theta in radians (-pi/2  to pi/2)'
            x_interp = np.interp(distance,self.CUMLENGTH,self.X_FINE)
            slope = self.ALIGNMENT(x_interp,1) # Tan theta
            angle = np.atan(slope)
            return angle


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
        def modifyNXModel(initial_align:utils.Alignment,final_align:utils.Alignment,bElement:bool=True,bUpdateModel=True,bSync=True):
            '''
            Modifies CIVIL NX model as per new alignment.  
            Meant for **standalone** use  
            Use transformPoint in other cases
            
            :param initial_align: Intitial alignment of the model
            :type initial_align: utils.Alignment
            :param final_align: Final alignment of the model
            :type final_align: utils.Alignment
            :param bElement: If beta angle of element should be modified
            :type bElement: bool
            '''
            from midas_civil import Node,Element,MidasAPI,nodeByID
            if bSync:
                Node.sync()
                if bElement: Element.sync()

            ptsXY = [(nd.X , nd.Y , nd.ID ) for nd in Node.nodes]
            dist_range = 0.25*initial_align.TOTALLENGTH    # 0.1 * total length

            dist_array = [dist_range*0.5-i*dist_range/50 for i in range(51)]    # 50 divisions

            finalXY = []
            for pt in ptsXY:
                ptx = pt[0]
                pty = pt[1]

                if ptx < initial_align.PT_X[0]:
                    x_onLine1 = initial_align.PT_X[0]
                    y_onLine1 = initial_align.PT_Y[0]
                    slope_onLine1 = initial_align.ALIGNMENT(x_onLine1,1)
                    angle_onLine1 = np.atan(slope_onLine1)

                    dist = hypot(ptx-x_onLine1,pty-y_onLine1)
                    tangent_angleO = np.atan((pty-y_onLine1)/(ptx-x_onLine1))    # Radian theta

                    x_onLine2 = final_align.PT_X[0]
                    y_onLine2 = final_align.PT_Y[0]
                    slope_onLine2 = final_align.ALIGNMENT(x_onLine2,1)
                    angle_onLine2 = np.atan(slope_onLine2)

                    totalAngle = angle_onLine2-angle_onLine1+tangent_angleO
                    x_off = np.cos(totalAngle)
                    y_off = np.sin(totalAngle)
                    angle = np.degrees(angle_onLine2-angle_onLine1)

                    finalXY.append([x_onLine2-x_off*dist,y_onLine2-y_off*dist,angle]) 

                elif ptx > initial_align.PT_X[-1]:
                    x_onLine1 = initial_align.PT_X[-1]
                    y_onLine1 = initial_align.PT_Y[-1]
                    slope_onLine1 = initial_align.ALIGNMENT(x_onLine1,1)
                    angle_onLine1 = np.atan(slope_onLine1)

                    dist = hypot(ptx-x_onLine1,pty-y_onLine1)
                    off = np.sign(pty-y_onLine1)*dist
                    tangent_angleO = np.atan((pty-y_onLine1)/(ptx-x_onLine1))    # Radian theta

                    x_onLine2 = final_align.PT_X[-1]
                    y_onLine2 = final_align.PT_Y[-1]
                    slope_onLine2 = final_align.ALIGNMENT(x_onLine2,1)
                    angle_onLine2 = np.atan(slope_onLine2)
                    
                    totalAngle = angle_onLine2-angle_onLine1+tangent_angleO

                    x_off = np.cos(totalAngle)
                    y_off = np.sin(totalAngle)
                    angle = np.degrees(angle_onLine2-angle_onLine1)

                    finalXY.append([x_onLine2+x_off*dist,y_onLine2+y_off*dist,angle]) 

                else:
                    x_onLine1 = np.add(ptx,dist_array)
                    y_onLine1 = initial_align.ALIGNMENT(x_onLine1)

                    sqDist = np.sum((np.array([ptx,pty]) - np.array(list(zip(x_onLine1,y_onLine1)))) ** 2, axis=1)
                    min_index = np.argmin(sqDist)

                    x_ref = x_onLine1[min_index]
                    y_ref = y_onLine1[min_index]
                    dist_ref = sqrt(sqDist[min_index])

                    final_u = np.interp(x_ref,initial_align.X_FINE,initial_align.U_FINE)
                    off = np.sign(pty-y_ref)*dist_ref
                    x2_interp = np.interp(final_u,final_align.U_FINE,final_align.X_FINE)
                    y2_interp = final_align.ALIGNMENT(x2_interp)  

                    slope = final_align.ALIGNMENT(x2_interp,1) # Tan theta
                    norm = sqrt(1+slope*slope)
                    x_off = -slope/norm
                    y_off = 1/norm

                    angle = np.degrees(np.atan(slope))

                    finalXY.append([x2_interp+x_off*off,y2_interp+y_off*off,angle])

            for i,nod in enumerate(Node.nodes):
                nod.X , nod.Y , nod.TEMP_ANG = float(finalXY[i][0]),float(finalXY[i][1]),float(finalXY[i][2])

            if bUpdateModel: Node.create()

            #---------------- BLOCK START FOR VERTICAL ELEMENT -------------------------------------------
            if bElement:
                editedElemsJS = {"Assign":{}}
                for elm in Element.elements:
                    if elm.TYPE in ['BEAM','TRUSS','TENSTR','COMPTR']:
                        if elm.LOCALX[0]==0 and elm.LOCALX[1]==0 :
                            elm.ANGLE += np.sign(elm.LOCALX[2])*nodeByID(elm.NODE[0]).TEMP_ANG

                            editedElemsJS["Assign"][elm.ID] = {"ANGLE":elm.ANGLE}
                if bUpdateModel: MidasAPI("PUT","/db/ELEM",editedElemsJS)

            
    
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

    @staticmethod
    def RC_Grillage(span_length = 20, width = 8, support:Literal['fix','pin']='fix', dia_no=2,start_loc = [0,0,0], girder_depth = 0, girder_width = 0, girder_no = 0, 
            web_thk = 0, slab_thk = 0, dia_depth = 0, dia_width = 0, overhang = 0, skew = 0, mat_E = 30_000_000):
        
        """
        RC Grillage Utility wizard
        Use Model.create() to create model in CIVIL NX
        
        Parameters
        ----------
        span_length : float, optional
            Span length of the structure (default is 20).
        width : float, optional
            Overall deck width (default is 8).
        support : {'fix', 'pin'}, optional
            Support condition at the ends of the span.
            'fix' for fixed support, 'pin' for pinned support (default is 'fix').
        dia_no : int, optional
            No of diaphragms (default is 2).
        start_loc : list, optional
            Start location for Grillage placement (default is [0,0,0]).
        girder_depth : float, optional
            Depth of the girder section (default is 0).
        girder_width : float, optional
            Width of the girder section (default is 0).
        girder_no : int, optional
            Number of girders in the system (default is 0).
        web_thk : float, optional
            Thickness of the girder web (default is 0).
        slab_thk : float, optional
            Thickness of the deck slab (default is 0).
        dia_depth : float, optional
            Depth of the diaphragm (default is 0).
        dia_width : float, optional
            Width of the diaphragm (default is 0).
        overhang : float, optional
            Overhang length beyond the outer girder (default is 0).
        skew : float, optional
            Skew angle of the structure in degrees (default is 0).
        mat_E : float, optional
            Modulus of elasticity of the material (default is 30,000,000).
        """
        from midas_civil import Model,Material,Section,Offset,nodesInGroup,Element,Boundary,Load,elemsInGroup,Node,Group
        import math

        Model.units()

        cos_theta = math.cos(math.radians(skew))
        tan_theta = math.tan(math.radians(skew))
        nSec = len(Section.sect)
        nMat = len(Material.mats)

        # dia_no = 2
        if span_length > 0 and width > 0:
            #Data proofing and initial calcs:
            if girder_depth == 0: girder_depth = max(1, round(span_length/20,3))
            if girder_no == 0: girder_no = int(width/2)
            if girder_width == 0: girder_width = width/girder_no
            if slab_thk == 0: slab_thk = round(span_length/100,1)+0.05
            if web_thk == 0: web_thk = round(girder_width/8,3)
            if dia_depth == 0: dia_depth = girder_depth - slab_thk
            if dia_width == 0: dia_width = web_thk
            if dia_no <=1:
                print("At least 2 diaphragms are required.  No. of diaphragm is changed to 2.")
                dia_no = 2
            if dia_no >= 2: 
                overhang = max(overhang, dia_width/2)
                cc_diaph = span_length / (dia_no - 1)
            elem_len = round(cc_diaph / (round(cc_diaph,0)), 6)
            if overhang > elem_len/2:
                o_div = int(round(overhang/elem_len + 1, 0))
                o_elem_len = overhang / o_div
            if overhang > 0 and overhang <= elem_len/2:
                o_div = 1
                o_elem_len = overhang
            if overhang == 0:
                o_div = 0
                o_elem_len = 0

        Material.CONC.User('Concrete',mat_E,0.2,25,0,1.2e-5,id=nMat+1)
        Material.CONC.User('Dummy',mat_E,0.2,0,0,1.2e-5,id=nMat+2)

        if overhang > 0:
            if o_div > 1: 
                Section.DBUSER(f"Overhang_Span{utils.__RC_Grillage_nSpan}",'SB',[slab_thk,o_elem_len*cos_theta],Offset('CT'),id=nSec+1)                                            
            Section.DBUSER(f"Start_Span{utils.__RC_Grillage_nSpan}",'SB',[slab_thk,o_elem_len*cos_theta/2],Offset('RT'),id=nSec+2)                                                        
            Section.DBUSER(f"End_Span{utils.__RC_Grillage_nSpan}",'SB',[slab_thk,o_elem_len*cos_theta/2],Offset('LT'),id=nSec+3)                                                     
        if dia_no >=2:
            Section.DBUSER(f"Diap_Span{utils.__RC_Grillage_nSpan}",'SB',[dia_depth,dia_width*cos_theta],Offset('CT',UsrOffOpt=1,VOffOpt=1,VOffset=-slab_thk),id=nSec+4)                        
        Section.DBUSER(f"T Beam_Span{utils.__RC_Grillage_nSpan}",'T',[girder_depth,girder_width,web_thk,slab_thk],Offset('CT'),id=nSec+5)                    
        Section.DBUSER(f"Slab_Span{utils.__RC_Grillage_nSpan}",'SB',[slab_thk,elem_len*cos_theta],Offset('CT'),id=nSec+6)                                                              
        Section.DBUSER(f"Slab_sup_st_Span{utils.__RC_Grillage_nSpan}",'SB',[slab_thk,(elem_len + o_elem_len)*cos_theta / 2],Offset('RT',UsrOffOpt=1,HOffOpt=1,HOffset=cos_theta*o_elem_len/2),id=nSec+7)  
        Section.DBUSER(f"Slab_sup_en_Span{utils.__RC_Grillage_nSpan}",'SB',[slab_thk,(elem_len + o_elem_len)*cos_theta / 2],Offset('LT',UsrOffOpt=1,HOffOpt=1,HOffset=cos_theta*o_elem_len/2),id=nSec+8)

        Section.DBUSER("Dummy CB",'SB',[0.1,0.1],Offset('CC'),id=9)   

        offTrans = 0.5*width/girder_no
        # Longitudinal
        Element.Beam.SDL(np.add([0,0,0],start_loc),[1,0,0],span_length,int(span_length),nMat+2,9,group=f'CrashBarrier_R {utils.__RC_Grillage_nSpan}')
        for i in range(girder_no):
            Element.Beam.SDL(np.add([(2*i*offTrans+offTrans)*tan_theta,2*i*offTrans+offTrans,0],start_loc),[1,0,0],span_length,int(span_length),nMat+1,nSec+5,group=f'Girder {i+1} Span {utils.__RC_Grillage_nSpan}')
            Boundary.Support(nodesInGroup(f'Girder {i+1} Span {utils.__RC_Grillage_nSpan}')[0],support,'Support')
            Boundary.Support(nodesInGroup(f'Girder {i+1} Span {utils.__RC_Grillage_nSpan}')[-1],support,'Support')
        Element.Beam.SDL(np.add([width*tan_theta,width,0],start_loc),[1,0,0],span_length,int(span_length),nMat+2,9,group=f'CrashBarrier_L {utils.__RC_Grillage_nSpan}')


        spacing = span_length/int(span_length)
        # Cross
        Element.Beam.SE(start_loc,np.add([width*tan_theta,width,0],start_loc),2*girder_no,nMat+1,nSec+4,group=f'Diaphragm {utils.__RC_Grillage_nSpan}')
        Element.Beam.SE(start_loc,np.add([width*tan_theta,width,0],start_loc),2*girder_no,nMat+2,nSec+7,group=f'CrossEnd {utils.__RC_Grillage_nSpan}')
        for i in range(int(span_length)-1):
            Element.Beam.SE(np.add([(i+1)*spacing,0,0],start_loc),np.add([(i+1)*spacing+width*tan_theta,width,0],start_loc),2*girder_no,nMat+2,nSec+6,group=f'Cross Slab {utils.__RC_Grillage_nSpan}')

        Element.Beam.SE(np.add([span_length,0,0],start_loc),np.add([span_length+width*tan_theta,width,0],start_loc),2*girder_no,nMat+2,nSec+8,group=f'CrossEnd {utils.__RC_Grillage_nSpan}')
        Element.Beam.SE(np.add([span_length,0,0],start_loc),np.add([span_length+width*tan_theta,width,0],start_loc),2*girder_no,nMat+1,nSec+4,group=f'Diaphragm {utils.__RC_Grillage_nSpan}')


        # # Overhang
        if o_elem_len!=0:
            Element.Beam.SE(np.add([-o_elem_len,0,0],start_loc),np.add([width*tan_theta-o_elem_len,width,0],start_loc),2*girder_no,nMat+2,nSec+2)
            Element.Beam.SE(np.add([span_length+o_elem_len,0,0],start_loc),np.add([width*tan_theta+span_length+o_elem_len,width,0],start_loc),2*girder_no,nMat+2,nSec+3)

            Element.Beam.SDL(np.add([-o_elem_len,0,0],start_loc),[1,0,0],o_elem_len,1,nMat+2,9,group=f'CrashBarrier_R {utils.__RC_Grillage_nSpan}')
            Element.Beam.SDL(np.add([span_length,0,0],start_loc),[1,0,0],o_elem_len,1,nMat+2,9,group=f'CrashBarrier_R {utils.__RC_Grillage_nSpan}')
            for i in range(girder_no):
                Element.Beam.SDL(np.add([-o_elem_len+(2*i*offTrans+offTrans)*tan_theta,2*i*offTrans+offTrans,0],start_loc),[1,0,0],o_elem_len,1,nMat+1,nSec+5,group=f'Girder {i+1} Span {utils.__RC_Grillage_nSpan}')
                Element.Beam.SDL(np.add([span_length+(2*i*offTrans+offTrans)*tan_theta,2*i*offTrans+offTrans,0],start_loc),[1,0,0],o_elem_len,1,nMat+1,nSec+5,group=f'Girder {i+1} Span {utils.__RC_Grillage_nSpan}')
            Element.Beam.SDL(np.add([-o_elem_len+width*tan_theta,width,0],start_loc),[1,0,0],o_elem_len,1,nMat+2,9,group=f'CrashBarrier_L {utils.__RC_Grillage_nSpan}')
            Element.Beam.SDL(np.add([span_length+width*tan_theta,width,0],start_loc),[1,0,0],o_elem_len,1,nMat+2,9,group=f'CrashBarrier_L {utils.__RC_Grillage_nSpan}')

        # extra diaphragm
        span_idx = list(range(int(span_length+1)))

        if dia_no > 2:
            for i in range(dia_no-2):
                Element.Beam.SE(np.add([span_idx[int((i+1)*span_length/(dia_no-1))]*spacing,0,0],start_loc),np.add([span_idx[int((i+1)*span_length/(dia_no-1))]*spacing+width*tan_theta,width,0],start_loc),2*girder_no,nMat+2,nSec+4,group='Diaphragm')


        if utils.__RC_Grillage_nSpan == 1 :
            Load.SW('Self Weight',load_group='Self Weight')

        # WCloading = -1.9
        WCloading = -22 * 0.075 * cos_theta
        Load.Beam(elemsInGroup(f'Cross Slab {utils.__RC_Grillage_nSpan}'),'Wearing Course','Wearing Course',WCloading)
        Load.Beam(elemsInGroup(f'CrossEnd {utils.__RC_Grillage_nSpan}'),'Wearing Course','Wearing Course',WCloading*0.5)


        CBloading = -22 * 0.5
        Load.Beam(elemsInGroup([f'CrashBarrier_R {utils.__RC_Grillage_nSpan}',f'CrashBarrier_L {utils.__RC_Grillage_nSpan}']),'Crash Barrier','Crash Barrier',CBloading)
        Group.Structure.clear()

        utils.__RC_Grillage_nSpan+=1
        #---------------------------------------------------------------------------------------
        # Model.create()