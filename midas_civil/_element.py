from ._mapi import *
from ._node import *
from ._group import _add_elem_2_stGroup
from ._group import _add_node_2_stGroup,Group,nodesInGroup
import numpy as np
from scipy.interpolate import splev, splprep , interp1d , Akima1DInterpolator
from math import hypot
import math
from ._utils import _convItem2List , _longestList

def _SInterp(angle,num_points):
    ''' Angle -> Input list | Num Points -> Output length'''

    angle = _convItem2List(angle)
    if len(angle) == 1 : 
        angle.append(angle[0])
        angle.append(angle[0])
    if len(angle) == 2 : 
        angle.append(angle[-1])
        angle[1] = (angle[0]+angle[2])*0.5

    num_angle = len(angle)
    angle_intrp_x = [0]
    angle_intrp_y = [angle[0]]
    for a in range(num_angle-1):
        angle_intrp_x.append((a+1)*(num_points-1)/(num_angle-1))
        angle_intrp_y.append(angle[a+1])

    _alignment = Akima1DInterpolator(angle_intrp_x, angle_intrp_y,method='makima')
    angle_intrp_func = interp1d(angle_intrp_x, angle_intrp_y)

    angle_intrp_finalY = []
    for i in range(num_points):
        angle_intrp_finalY.append(_alignment(i))

    return angle_intrp_finalY

def _interpolateAlignment(pointsArray,n_seg=10,deg=1,mSize=0,includePoint:bool=True,div_axis="L") -> list:
    ''' Returns point list and beta angle list'''
    pointsArray = np.array(pointsArray)
    x_p, y_p , z_p  = pointsArray[:,0] , pointsArray[:,1] , pointsArray[:,2]

    if deg < 1 :
        deg = 1
    if deg > len(pointsArray)-1:
        deg = len(pointsArray)-1

    #-- Actual length ----

    tck, u = splprep([x_p, y_p, z_p], s=0, k=deg)

    u_fine = np.linspace(0, 1, 500)
    x_den, y_den, z_den = splev(u_fine, tck)

    dx = np.diff(x_den)
    dy = np.diff(y_den)
    dz = np.diff(z_den)
    dl=[]
    for i in range(len(dx)):
        dl.append(hypot(dx[i],dy[i],dz[i]))

    cum_l = np.insert(np.cumsum(dl),0,0)
    total_l = cum_l[-1]


    if n_seg==0 or mSize!=0:
        n_seg=int(total_l/mSize)


    if div_axis == "X":
        eq_x = np.linspace(x_p[0],x_p[-1],n_seg+1)
        interp_u = np.interp(eq_x,x_den,u_fine)
    elif div_axis == "Y":
        eq_y = np.linspace(y_p[0],y_p[-1],n_seg+1)
        interp_u = np.interp(eq_y,y_den,u_fine)
    elif div_axis == "Z":
        eq_z = np.linspace(z_p[0],z_p[-1],n_seg+1)
        interp_u = np.interp(eq_z,z_den,u_fine)
    else :
        eq_len = np.linspace(0,total_l,n_seg+1)
        interp_u = np.interp(eq_len,cum_l,u_fine)


    if includePoint:
        interp_u = np.sort(np.append(interp_u,u[1:-1])).tolist()

        eq_u = 1/n_seg # for filtering close points
    
        new_u = []
        skip=0
        for i in range(len(interp_u)-1):
            if skip == 1:
                skip = 0 
                continue
            if interp_u[i+1]-interp_u[i] < 0.2*eq_u:
                if interp_u[i] in u:
                    new_u.append(interp_u[i])
                    skip=1
                else:
                    new_u.append(interp_u[i+1])
                    skip=1
            else:
                new_u.append(interp_u[i])
        new_u.append(interp_u[-1])
    else:
        new_u = interp_u


    interp_x, interp_y , interp_z = splev(new_u, tck)


    align_fine_points  = [ [round(x,6), round(y,6), round(z,6)] for x, y, z in zip(interp_x, interp_y , interp_z) ]

    return align_fine_points



def _nodeDIST(a:Node,b:Node):
    return round(hypot((a.X-b.X),(a.Y-b.Y),(a.Z-b.Z)),6)

def _nodeAngleVector(b:Node,a:Node):

    Z_new = np.array([0.000001,0,1])
    X_new = np.array([(a.X-b.X),(a.Y-b.Y),(a.Z-b.Z)])
    Y_new = np.cross(Z_new, X_new)

    Z_new = np.cross(X_new, Y_new) # Recomputing

    X_new = X_new / (np.linalg.norm(X_new)+0.000001)
    Y_new = Y_new / (np.linalg.norm(Y_new)+0.000001)
    Z_new = Z_new / (np.linalg.norm(Z_new)+0.000001)


    return [X_new,Y_new,Z_new]


def _triangleAREA(a:Node,b:Node,c:Node):
    v1 = np.array([a.X-b.X,a.Y-b.Y,a.Z-b.Z])
    v2 = np.array([b.X-c.X,b.Y-c.Y,b.Z-c.Z])
    mag = np.linalg.norm(np.cross(v1, v2))
    return float(0.5 * mag) , np.cross(v1, v2)/mag

def _calcVector(deltaLocation,angle=0): # Returns normalised local X,Y,Z for line
    Z_new = np.array([0.000001,0,1])
    X_new = np.array(deltaLocation)
    Y_new = np.cross(Z_new, X_new)

    Z_new = np.cross(X_new, Y_new) # Recomputing

    X_new = X_new / (np.linalg.norm(X_new)+0.000001)
    Y_new = Y_new / (np.linalg.norm(Y_new)+0.000001)
    Z_new = Z_new / (np.linalg.norm(Z_new)+0.000001)

    from scipy.spatial.transform import Rotation as R
    p_y = np.array(Y_new)
    p_z = np.array(Z_new)

    axis = np.array(X_new)
    theta = np.deg2rad(angle)               # or radians directly
    rot = R.from_rotvec(axis * theta)           # axis-angle as rotation vector
    
    rt_y = rot.apply(p_y)                         # rotated point around axis through origin
    rt_z = rot.apply(p_z)  
    
    return [X_new,rt_y,rt_z]

def _rotatePT(pt,axis,deg):
    from scipy.spatial.transform import Rotation as R
    p = np.array(pt)
    axis = np.array(axis)
    theta = np.deg2rad(deg)               # or radians directly
    rot = R.from_rotvec(axis * theta)           # axis-angle as rotation vector
    return rot.apply(p)                         # rotated point around axis through origin

def _pointOffset(pts,yEcc=0,zEcc=0,angle=0):
    from ._utils import _matchArray

    angle2 = _matchArray(pts,angle)
    yEcc2 = _matchArray(pts,yEcc)
    zEcc2 = _matchArray(pts,zEcc)

    norm = []
    norm.append(_calcVector(np.subtract(pts[1],pts[0]),angle2[0]))    # first X- along vector

    for i in range(len(pts)-2): # Averaged X- along vector for middle points
        X_new1 = np.array(np.subtract(pts[i+1],pts[i]))
        X_new2 = np.array(np.subtract(pts[i+2],pts[i+1]))

        X_new1 = X_new1 / (np.linalg.norm(X_new1)+0.000001)
        X_new2 = X_new2 / (np.linalg.norm(X_new2)+0.000001)

        norm.append(_calcVector(np.add(X_new1,X_new2),angle2[i+1]))

    norm.append(_calcVector(np.subtract(pts[-1],pts[-2]),angle2[-1])) # last X- along vector

    # print(norm)

    pt_new = []
    for i in range(len(pts)):
        pt_new.append(pts[i]+yEcc2[i]*norm[i][1]+zEcc2[i]*norm[i][2])

    return pt_new


def _ADD(self):
    """
    Adds an element to the main list. If the ID is 0, it auto-increments.
    If the ID already exists, it replaces the existing element.
    """

    # ------------  ID assignment -----------------------
    if NX.dummy_elems == False :
        id = int(self.ID)
        if not Element.ids:
            count = 1
        else:
            count = max(Element.ids) + 1

        if id == 0:
            self.ID = count
            Element.elements.append(self)
            Element.ids.append(int(self.ID))
        elif id in Element.ids:
            self.ID = int(id)
            print(f'⚠️  Element with ID {id} already exists! It will be replaced.')
            index = Element.ids.index(id)
            Element.elements[index] = self
        else:
            self.ID = id
            Element.elements.append(self)
            Element.ids.append(int(self.ID))
        Element.__elemDIC__[str(self.ID)] = self
        
        # ------------  Group assignment -----------------------
        if self._GROUP == "" :
            pass
        elif isinstance(self._GROUP, list):
            for gpName in self._GROUP:
                _add_elem_2_stGroup(self.ID,gpName)
                for nd in self.NODE:
                    _add_node_2_stGroup(nd,gpName)
        elif isinstance(self._GROUP, str):
            _add_elem_2_stGroup(self.ID,self._GROUP)
            for nd in self.NODE:
                _add_node_2_stGroup(nd,self._GROUP)
    else:
        if self._GROUP == "" :
            pass
        elif isinstance(self._GROUP, list):
            for gpName in self._GROUP:
                for nd in self.NODE:
                    _add_node_2_stGroup(nd,gpName)
        elif isinstance(self._GROUP, str):
            for nd in self.NODE:
                _add_node_2_stGroup(nd,self._GROUP)
            





def _updateElem(self):
    """Sends a PUT request to update a single element in Midas."""
    js2s = {'Assign': {self.ID: _Obj2JS(self)}}
    MidasAPI('PUT', '/db/elem', js2s)
    return js2s

def _Obj2JS(obj):
    """Converts a Python element object to its JSON dictionary representation."""
    # Base attributes common to many elements
    js = {
        "TYPE": obj.TYPE,
        "MATL": obj.MATL,
        "SECT": obj.SECT,
        "NODE": obj.NODE,
    }
    
    # Add optional attributes if they exist on the object
    if hasattr(obj, 'ANGLE'): js["ANGLE"] = obj.ANGLE
    if hasattr(obj, 'STYPE'): js["STYPE"] = obj.STYPE
    
    # Handle type-specific and subtype-specific attributes
    if obj.TYPE == 'TENSTR': # Tension/Hook/Cable
        # Tension-only (stype=1) - can have TENS parameter
        if obj.STYPE == 1:
            if hasattr(obj, 'TENS'): js["TENS"] = obj.TENS
            if hasattr(obj, 'T_LIMIT'): js["T_LIMIT"] = obj.T_LIMIT
            if hasattr(obj, 'T_bLMT'): js["T_bLMT"] = obj.T_bLMT
        
        # Hook (stype=2) - has NON_LEN parameter
        elif obj.STYPE == 2:
            if hasattr(obj, 'NON_LEN'): js["NON_LEN"] = obj.NON_LEN
        
        # Cable (stype=3) - has CABLE, NON_LEN, and TENS parameters
        elif obj.STYPE == 3:
            if hasattr(obj, 'CABLE'): js["CABLE"] = obj.CABLE
            if hasattr(obj, 'NON_LEN'): js["NON_LEN"] = obj.NON_LEN
            if hasattr(obj, 'TENS'): js["TENS"] = obj.TENS

    elif obj.TYPE == 'COMPTR': # Compression/Gap
        # Compression-only (stype=1) - can have TENS, T_LIMIT, T_bLMT
        if obj.STYPE == 1:
            if hasattr(obj, 'TENS'): js["TENS"] = obj.TENS
            if hasattr(obj, 'T_LIMIT'): js["T_LIMIT"] = obj.T_LIMIT
            if hasattr(obj, 'T_bLMT'): js["T_bLMT"] = obj.T_bLMT
        
        # Gap (stype=2) - has NON_LEN parameter
        elif obj.STYPE == 2:
            if hasattr(obj, 'NON_LEN'): js["NON_LEN"] = obj.NON_LEN
            
    return js

def _JS2Obj(id, js):
    """Converts a JSON dictionary back into a Python element object during sync."""
    elem_type = js.get('TYPE')
    
    # Prepare arguments for constructors
    args = {
        'id': int(id),
        'mat': js.get('MATL'),
        'sect': js.get('SECT'),
        'node': js.get('NODE'),
        'angle': js.get('ANGLE'),
        'stype': js.get('STYPE')
    }
    
    # Prepare individual parameters for optional/subtype-specific parameters
    non_len = js.get('NON_LEN')
    cable_type = js.get('CABLE')
    tens = js.get('TENS')
    t_limit = js.get('T_LIMIT')

    if elem_type == 'BEAM':
        Element.Beam(args['node'][0], args['node'][1], args['mat'], args['sect'], args['angle'], '', args['id'])
    elif elem_type == 'TRUSS':
        Element.Truss(args['node'][0], args['node'][1], args['mat'], args['sect'], args['angle'],'',  args['id'])
    elif elem_type == 'PLATE':
        Element.Plate(args['node'], args['stype'], args['mat'], args['sect'], args['angle'], '', args['id'])
    elif elem_type == 'TENSTR':
        Element.Tension(args['node'][0], args['node'][1], args['stype'], args['mat'], args['sect'], args['angle'], '', args['id'], non_len, cable_type, tens, t_limit)
    elif elem_type == 'COMPTR':
        Element.Compression(args['node'][0], args['node'][1], args['stype'], args['mat'], args['sect'], args['angle'], '', args['id'], tens, t_limit, non_len)
    elif elem_type == 'SOLID':
        Element.Solid(nodes=args['node'], mat=args['mat'], sect=args['sect'],group='', id=args['id'])


class _common:
    """Common base class for all element types."""
    def __str__(self):
        return str(f'ID = {self.ID} \nJSON : {_Obj2JS(self)}\n')

    def update(self):
        return _updateElem(self)

# --- Main Element Class ---
class Element:
    """
    Main class to create and manage structural elements like Beams, Trusses,
    Plates, Tension/Compression-only elements, and Solids.
    """
    elements = []
    ids = []
    __elemDIC__ = {}

    
    lastLoc = (0,0,0) #Last Location created using Beam element
    '''Last Node Location created by Beam / Truss element - (x,y,z)'''

    @classmethod
    def json(cls):
        json_data = {"Assign": {}}
        for elem in cls.elements:
            js = _Obj2JS(elem)
            json_data["Assign"][elem.ID] = js
        return json_data

    @classmethod
    def create(cls):
        if cls.elements:
            MidasAPI("PUT", "/db/ELEM", Element.json())

    @staticmethod
    def get():
        return MidasAPI("GET", "/db/ELEM")

    @staticmethod
    def sync():
        a = Element.get()
        if a and 'ELEM' in a and a['ELEM']:
            Element.elements = []
            Element.ids = []
            Element.__elemDIC__={}
            for elem_id, data in a['ELEM'].items():
                _JS2Obj(elem_id, data)

    @staticmethod
    def delete():
        MidasAPI("DELETE", "/db/ELEM")
        Element.elements = []
        Element.ids = []
        Element.__elemDIC__={}
    
    @staticmethod
    def clear():
        Element.elements = []
        Element.ids = []
        Element.__elemDIC__={}

    # --- Element Type Subclasses ---

    class Beam(_common):

        def __init__(self, i: int, j: int, mat: int = 1, sect: int = 1, angle: float = 0, group = "" , id: int = 0,bLocalAxis=False):
            """
            Creates a BEAM element for frame analysis.
            
            Parameters:
                i: Start node ID
                j: End node ID  
                mat: Material property number (default 1)
                sect: Section property number (default 1)
                angle: Beta angle for section orientation in degrees (default 0.0)
                group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
                id: Element ID (default 0 for auto-increment)
                
            
            Examples:
                ```python
                # Simple beam with default properties
                Element.Beam(1, 2)
                
                # Beam with specific material and section
                Element.Beam(1, 2, mat=2, sect=3)
                
                # Beam with 90° rotation (strong axis vertical)
                Element.Beam(1, 2, mat=1, sect=1, angle=90.0)
                
                # Beam with specific ID
                Element.Beam(1, 2, mat=1, sect=1, angle=0.0, id=100)
                ```
            """
            self.ID = id
            self.TYPE = 'BEAM'
            self.MATL = mat
            self.SECT = sect
            self.NODE = [i, j]
            self.ANGLE = angle
            self._GROUP = group

            _n1 = nodeByID(i)
            _n2 = nodeByID(j)
            self.LENGTH = _nodeDIST(_n1,_n2)

            if bLocalAxis:
                _tempAngle = _nodeAngleVector(_n1,_n2)
                _n1.AXIS = np.add(_n1.AXIS,_tempAngle)
                _n2.AXIS = np.add(_n2.AXIS,_tempAngle)

                _norm1 = np.linalg.norm(_n1.AXIS ,axis=1,keepdims=True)
                _n1.AXIS = _n1.AXIS /_norm1

                _norm2 = np.linalg.norm(_n2.AXIS ,axis=1,keepdims=True)
                _n2.AXIS = _n2.AXIS /_norm2

            Element.lastLoc = (_n2.X,_n2.Y,_n2.Z)

            _ADD(self)

        @staticmethod
        def SDL(s_loc:list,dir:list,l:float,n:int=1,mat:int=1,sect:int=1,angle:float=0, group = "" , id: int = 0,bLocalAxis=False): #CHANGE TO TUPLE
                if isinstance(s_loc,Node):
                    s_loc = (s_loc.X,s_loc.Y,s_loc.Z)

                beam_nodes =[]
                beam_obj = []
                s_locc = np.array(s_loc)
                unit_vec = np.array(dir)/np.linalg.norm(dir)

                for i in range(n+1):
                    locc = s_locc+i*l*unit_vec/n
                    Enode=Node(locc[0].item(),locc[1].item(),locc[2].item())
                    beam_nodes.append(Enode.ID)
                Element.lastLoc = (locc[0].item(),locc[1].item(),locc[2].item())
                for i in range(n):
                    if id == 0 : id_new = 0
                    else: id_new = id+i
                    beam_obj.append(Element.Beam(beam_nodes[i],beam_nodes[i+1],mat,sect,angle,group,id_new,bLocalAxis))
                
                return beam_obj
                    

        @staticmethod
        def SE(s_loc:list,e_loc:list,n:int=1,mat:int=1,sect:int=1,angle:float=0, group = "" , id: int = 0,bLocalAxis=False):
                if isinstance(s_loc,Node):
                    s_loc = (s_loc.X,s_loc.Y,s_loc.Z)
                if isinstance(e_loc,Node):
                    e_loc = (e_loc.X,e_loc.Y,e_loc.Z)

                beam_nodes =[]
                beam_obj = []
                i_loc = np.linspace(s_loc,e_loc,n+1)
                for i in range(n+1):
                    Enode=Node(i_loc[i][0].item(),i_loc[i][1].item(),i_loc[i][2].item())
                    beam_nodes.append(Enode.ID)
                for i in range(n):
                    if id == 0 : id_new = 0
                    else: id_new = id+i
                    beam_obj.append(Element.Beam(beam_nodes[i],beam_nodes[i+1],mat,sect,angle,group,id_new,bLocalAxis))
                
                return beam_obj
        
        @staticmethod
        def PLine(points_loc:list,n_div:int=0,deg:int=1,includePoint:bool=False,mat:int=1,sect:int=1,angle:float=0, group = "" , id: int = 0,bLocalAxis=False,div_axis="L"):
                '''
                angle : float of list(float)
                '''

                beam_nodes =[]
                beam_obj = []
                if n_div == 0 :
                    i_loc = points_loc
                else:
                    i_loc = _interpolateAlignment(points_loc,n_div,deg,0,includePoint,div_axis)

                num_points = len(i_loc)                
                angle_intrp_finalY = _SInterp(angle,num_points-1) #Beta Angle to be applied to Elements So, n-1

                for i in i_loc:
                    Enode=Node(i[0],i[1],i[2])
                    beam_nodes.append(Enode.ID)
                for i in range(len(i_loc)-1):
                    if id == 0 : id_new = 0
                    else: id_new = id+i
                    beam_obj.append(Element.Beam(beam_nodes[i],beam_nodes[i+1],mat,sect,angle_intrp_finalY[i].item(),group,id_new,bLocalAxis))
                
                return beam_obj
        
        @staticmethod
        def PLine2(points_loc:list,n_div:int=0,deg:int=1,includePoint:bool=False,mat:int=1,sect:int=1,angle:list[float]=0, group = "" , id: int = 0,bLocalAxis=False,div_axis="L",yEcc:list[float]=0,zEcc:list[float]=0,bAngleInEcc:bool=True):
                '''
                Creates a polyline with Eccentricity considering the beta angle provided   
                angle , yEcc , zEcc : float or list(float)   
                        [0,10] -> Angle at start = 0 | Angle at end = 10   
                        [0,10,0] -> Angle at start = 0 |  Angle at mid = 10  |  Angle at end = 0   
                        Inbetween values are **MAKIMA 1D** interpolated. (not cubic)
                '''
                from ._utils import _matchArray
                
                beam_nodes =[]
                beam_obj = []
                if n_div == 0 :
                    i_loc = points_loc
                else:
                    i_loc = _interpolateAlignment(points_loc,n_div,deg,0,includePoint,div_axis)
                
                
                num_points = len(i_loc)                
                if bAngleInEcc:
                    angle_intrp_Ecc = _SInterp(angle,num_points)
                else:
                    angle_intrp_Ecc = _matchArray(i_loc,[0])
                angle_intrp_finalY = _SInterp(angle,num_points-1) #Beta Angle to be applied to Elements So, n-1
                
                yEcc_intrp = _SInterp(yEcc,num_points)
                zEcc_intrp = _SInterp(zEcc,num_points)

                i_loc2 = _pointOffset(i_loc,yEcc_intrp,zEcc_intrp,angle_intrp_Ecc)
                for i in i_loc2:
                    Enode=Node(i[0],i[1],i[2])
                    beam_nodes.append(Enode.ID)
                

                for i in range(len(i_loc2)-1):
                    if id == 0 : id_new = 0
                    else: id_new = id+i
                    beam_obj.append(Element.Beam(beam_nodes[i],beam_nodes[i+1],mat,sect,angle_intrp_finalY[i].item(),group,id_new,bLocalAxis))
                
                return beam_obj

    class Truss(_common):
        def __init__(self, i: int, j: int, mat: int = 1, sect: int = 1, angle: float = 0, group = "" , id: int = 0):
            """
            Creates a TRUSS element
            
            Parameters:
                i: Start node ID
                j: End node ID
                mat: Material property number (default 1)
                sect: Section property number (default 1)
                angle: Beta angle for section orientation in degrees (default 0.0)
                group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
                id: Element ID (default 0 for auto-increment)
            
            Examples:
                ```python
                # Simple truss member
                Element.Truss(1, 2)
                
                # Truss with specific material and section
                Element.Truss(1, 2, mat=3, sect=2)
                
                # Diagonal truss member
                Element.Truss(3, 4, mat=1, sect=1, id=50)
                ```
            """
            self.ID = id
            self.TYPE = 'TRUSS'
            self.MATL = mat
            self.SECT = sect
            self.NODE = [i, j]
            self.ANGLE = angle
            self._GROUP = group
            _n2 = nodeByID(j)
            self.LENGTH = _nodeDIST(nodeByID(i),_n2)
            Element.lastLoc = (_n2.X,_n2.Y,_n2.Z)
            _ADD(self)

        @staticmethod
        def SDL(s_loc:list,dir:list,l:float,n:int=1,mat:int=1,sect:int=1,angle:float=0, group = "" , id: int = 0):
            if isinstance(s_loc,Node):
                    s_loc = (s_loc.X,s_loc.Y,s_loc.Z)

            beam_nodes =[]
            beam_obj =[]
            s_locc = np.array(s_loc)
            unit_vec = np.array(dir)/np.linalg.norm(dir)

            for i in range(n+1):
                locc = s_locc+i*l*unit_vec/n
                Enode=Node(locc[0].item(),locc[1].item(),locc[2].item())
                beam_nodes.append(Enode.ID)
            
            for i in range(n):
                if id == 0 : id_new = 0
                else: id_new = id+i
                beam_obj.append(Element.Truss(beam_nodes[i],beam_nodes[i+1],mat,sect,angle,group,id_new))
            
            return beam_obj
                

        @staticmethod
        def SE(s_loc:list,e_loc:list,n:int=1,mat:int=1,sect:int=1,angle:float=0, group = "" , id: int = 0):
            
            if isinstance(s_loc,Node):
                s_loc = (s_loc.X,s_loc.Y,s_loc.Z)
            if isinstance(e_loc,Node):
                s_loc = (e_loc.X,e_loc.Y,e_loc.Z)

            beam_nodes =[]
            beam_obj = []
            i_loc = np.linspace(s_loc,e_loc,n+1)
            for i in range(n+1):
                Enode=Node(i_loc[i][0].item(),i_loc[i][1].item(),i_loc[i][2].item())
                beam_nodes.append(Enode.ID)
            
            for i in range(n):
                if id == 0 : id_new = 0
                else: id_new = id+i
                beam_obj.append(Element.Truss(beam_nodes[i],beam_nodes[i+1],mat,sect,angle,group,id_new))
            
            return beam_obj 
          
    class Plate(_common):
        def __init__(self, nodes: list, stype: int = 1, mat: int = 1, sect: int = 1, angle: float = 0, group = "" , id: int = 0):
            """
            Creates a PLATE element.
            
            Parameters:
                nodes: List of node IDs [n1, n2, n3] for triangular or [n1, n2, n3, n4] for quadrilateral
                stype: Plate subtype (1=Thick plate, 2=Thin plate, 3=With drilling DOF) (default 1)
                mat: Material property number (default 1)
                sect: Section (thickness) property number (default 1)
                angle: Material angle for orthotropic materials in degrees (default 0.0)
                group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
                id: Element ID (default 0 for auto-increment)
            
            Examples:
                ```python
                # Triangular thick plate
                Element.Plate([1, 2, 3], stype=1, mat=1, sect=1)
                
                # Quadrilateral thin plate
                Element.Plate([1, 2, 3, 4], stype=2, mat=2, sect=1)
                
                # Plate with drilling DOF for shell analysis
                Element.Plate([5, 6, 7, 8], stype=3, mat=1, sect=2, angle=45.0)
                ```
            """
            self.ID = id
            self.TYPE = 'PLATE'
            self.MATL = mat
            self.SECT = sect
            
            self.ANGLE = angle
            self.STYPE = stype
            self._GROUP = group

            uniq_nodes = list(dict.fromkeys(nodes))
            self._NPOINT=len(uniq_nodes)
            if len(uniq_nodes)==3:
                self.NODE = uniq_nodes
                self.AREA,self.NORMAL = _triangleAREA(nodeByID(uniq_nodes[0]),nodeByID(uniq_nodes[1]),nodeByID(uniq_nodes[2]))
            elif len(uniq_nodes)==4:
                self.NODE = nodes
                a1 , n1 = _triangleAREA(nodeByID(nodes[0]),nodeByID(nodes[1]),nodeByID(nodes[2]))
                a2 , n2 = _triangleAREA(nodeByID(nodes[2]),nodeByID(nodes[3]),nodeByID(nodes[0]))
                self.AREA = a1+a2
                self.NORMAL = (n1+n2)/np.linalg.norm((n1+n2+0.000001))
                


            _ADD(self)

        # @staticmethod
        # def fromPoints(points: list, meshSize:float=0, stype: int = 1, mat: int = 1, sect: int = 1, angle: float = 0, group = "" , id: int = 0): #CHANGE TO TUPLE
        #         # INPUTS POINTS and create a triangular meshing with given mesh size  |  If meshSize = 0 , half of shortest length will be taken as mesh size
        #         return 0
        
        @staticmethod
        def loftGroups(strGroups: list, stype: int = 1, mat: int = 1, sect: int = 1, angle: float = 0, group = "" , id: int = 0): #CHANGE TO TUPLE
                # INPUTS 2 or more structure groups to create rectangular plates between the nodes | No. of nodes should be same in the Str Group
            """
            INPUTS 2 or more structure groups to create rectangular plates between the nodes  
            No. of nodes should be same in the Str Group
            """
            n_groups = len(strGroups)
            if n_groups < 2 :
                print("⚠️ No. of structure groups in Plate.loftGroups in less than 2")
                return False
            plate_obj = []
            for ng in range(n_groups-1):
                nID_A = nodesInGroup(strGroups[ng])   
                nID_B = nodesInGroup(strGroups[ng+1])

                max_len = max(len(nID_A),len(nID_B))
                if max_len < 2 :
                    print("⚠️ No. of nodes in Plate.loftGroups in less than 2")
                    return False

                nID_A , nID_B = _longestList(nID_A , nID_B)
                for i in range(max_len-1):
                    pt_array = [nID_A[i],nID_B[i],nID_B[i+1],nID_A[i+1]]
                    plate_obj.append(Element.Plate(pt_array,stype,mat,sect,angle,group,id))

            return plate_obj
            
    class Tension(_common):
     def __init__(self, i: int, j: int, stype: int, mat: int = 1, sect: int = 1, angle: float = 0, group = "" , id: int = 0, non_len: float = None, cable_type: int = None, tens: float = None, t_limit: float = None):
        """
        Creates a TENSTR (Tension-only) element.
        
        Parameters:
            i: Start node ID
            j: End node ID
            stype: Tension element subtype (1=Tension-only, 2=Hook, 3=Cable)
            mat: Material property number (default 1)
            sect: Section property number (default 1)
            angle: Beta angle for section orientation in degrees (default 0.0)
            group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
            id: Element ID (default 0 for auto-increment)
            non_len: Non-linear length parameter for Hook/Cable (default None)
            cable_type: Cable type for stype=3 (1=Pretension, 2=Horizontal, 3=Lu) (default None)
            tens: Initial tension force or allowable compression (default None)
            t_limit: Tension limit value. If provided, the tension limit flag is set to True. (default None)
        
        Examples:
            ```python
            # Simple tension-only member
            Element.Tension(1, 2, stype=1)
            
            # Tension-only with allowable compression and a tension limit
            Element.Tension(1, 2, stype=1, tens=0.5, t_limit=-15)
            
            # Hook element with slack length
            Element.Tension(3, 4, stype=2, non_len=0.5)
            
            # Cable with initial tension and catenary effects
            Element.Tension(5, 6, stype=3, cable_type=3, tens=1000.0, non_len=0.1)
            ```
        """
        self.ID = id
        self.TYPE = 'TENSTR'
        self.MATL = mat
        self.SECT = sect
        self.NODE = [i, j]
        self.ANGLE = angle
        self.STYPE = stype
        self._GROUP = group
        self.LENGTH = _nodeDIST(nodeByID(i),nodeByID(j))
        
        # Handle subtype-specific parameters
        if stype == 1:  # Tension-only specific
            if tens is not None:
                self.TENS = tens
            if t_limit is not None:
                self.T_LIMIT = t_limit
                self.T_bLMT = True
                
        elif stype == 2:  # Hook specific
            if non_len is not None:
                self.NON_LEN = non_len
                
        elif stype == 3:  # Cable specific
            if cable_type is not None:
                self.CABLE = cable_type
            if non_len is not None:
                self.NON_LEN = non_len
            if tens is not None:
                self.TENS = tens
        _ADD(self)

    class Compression(_common):
        def __init__(self, i: int, j: int, stype: int, mat: int = 1, sect: int = 1, angle: float = 0, group = "" , id: int = 0, tens: float = None, t_limit: float = None, non_len: float = None):
            """
            Creates a COMPTR (Compression-only) element.
            
            Parameters:
                i: Start node ID
                j: End node ID
                stype: Compression element subtype (1=Compression-only, 2=Gap)
                mat: Material property number (default 1)
                sect: Section property number (default 1)
                angle: Beta angle for section orientation in degrees (default 0.0)
                group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
                id: Element ID (default 0 for auto-increment)
                tens: Allowable tension or initial compression force (default None)
                t_limit: Compression limit value. If provided, the compression limit flag is set to True. (default None)
                non_len: Non-linear length parameter for gap (default None)
            
            Examples:
                ```python
                # Simple compression-only member
                Element.Compression(1, 2, stype=1)
                
                # Compression-only with tension limit and buckling limit
                Element.Compression(1, 2, stype=1, tens=27, t_limit=-15)
                
                # Gap element with initial gap
                Element.Compression(3, 4, stype=2, non_len=0.25)
                ```
            """
            self.ID = id
            self.TYPE = 'COMPTR'
            self.MATL = mat
            self.SECT = sect
            self.NODE = [i, j]
            self.ANGLE = angle
            self.STYPE = stype
            self._GROUP = group
            self.LENGTH = _nodeDIST(nodeByID(i),nodeByID(j))
            
            # Handle subtype-specific parameters
            if stype == 1:  # Compression-only specific
                if tens is not None:
                    self.TENS = tens
                if t_limit is not None:
                    self.T_LIMIT = t_limit
                    self.T_bLMT = True
                    
            elif stype == 2:  # Gap specific
                if non_len is not None:
                    self.NON_LEN = non_len
            _ADD(self)

    class Solid(_common):
        def __init__(self, nodes: list, mat: int = 1, sect: int = 0, group = "" , id: int = 0):
            """
            Creates a SOLID element for 3D analysis.
            
            Parameters:
                nodes: List of node IDs defining the solid element
                       - 4 nodes: Tetrahedral element
                       - 6 nodes: Pentahedral element  
                       - 8 nodes: Hexahedral element
                mat: Material property number (default 1)
                group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
                id: Element ID (default 0 for auto-increment)
            
            Examples:
                ```python
                # Tetrahedral solid element
                Element.Solid([1, 2, 3, 4], mat=1)
                
                # Wedge solid element
                Element.Solid([1, 2, 3, 4, 5, 6], mat=2)
                
                # Hexahedral solid element
                Element.Solid([1, 2, 3, 4, 5, 6, 7, 8], mat=1, id=200)
                ```
            """
            if len(nodes) not in [4, 6, 8]:
                raise ValueError("Solid element must have 4, 6, or 8 nodes.")
            self.ID = id
            self.TYPE = 'SOLID'
            self.MATL = mat
            self.SECT = sect # Solid elements don't use section properties
            self.NODE = nodes
            self._GROUP = group
            _ADD(self)

    
#-----------------------------------------------Stiffness Scale Factor------------------------------

    class StiffnessScaleFactor:
    
        data = []
        
        def __init__(self, 
                    element_id,
                    area_sf: float = 1.0,
                    asy_sf: float = 1.0,
                    asz_sf: float = 1.0,
                    ixx_sf: float = 1.0,
                    iyy_sf: float = 1.0,
                    izz_sf: float = 1.0,
                    wgt_sf: float = 1.0,
                    group: str = "",
                    id: int = None):
            """
                element_id: Element ID(s) where scale factor is applied (can be int or list)
                area_sf: Cross-sectional area scale factor
                asy_sf: Effective Shear Area scale factor (y-axis)
                asz_sf: Effective Shear Area scale factor (z-axis)
                ixx_sf: Torsional Resistance scale factor (x-axis)
                iyy_sf: Area Moment of Inertia scale factor (y-axis)
                izz_sf: Area Moment of Inertia scale factor (z-axis)
                wgt_sf: Weight scale factor
                group: Group name (default "")
                id: Scale factor ID (optional, auto-assigned if None)
            
            Examples:
                StiffnessScaleFactor(908, area_sf=0.5, asy_sf=0.6, asz_sf=0.7, 
                                ixx_sf=0.8, iyy_sf=0.8, izz_sf=0.9, wgt_sf=0.95)
                
            """
            
            # Check if group exists, create if not
            if group != "":
                chk = 0
                a = [v['NAME'] for v in Group.Boundary.json()["Assign"].values()]
                if group in a:
                    chk = 1
                if chk == 0:
                    Group.Boundary(group)
            
            # Handle element_id as single int or list
            if isinstance(element_id, (list, tuple)):
                self.ELEMENT_IDS = list(element_id)
            else:
                self.ELEMENT_IDS = [element_id]
            
            self.AREA_SF = area_sf
            self.ASY_SF = asy_sf
            self.ASZ_SF = asz_sf
            self.IXX_SF = ixx_sf
            self.IYY_SF = iyy_sf
            self.IZZ_SF = izz_sf
            self.WGT_SF = wgt_sf
            self.GROUP_NAME = group
            
            # Auto-assign ID if not provided
            if id is None:
                self.ID = len(Element.StiffnessScaleFactor.data) + 1
            else:
                self.ID = id
            
            # Add to static list
            Element.StiffnessScaleFactor.data.append(self)
        
        @classmethod
        def json(cls):
            """
            Converts StiffnessScaleFactor data to JSON format
            """
            json_data = {"Assign": {}}
            
            for scale_factor in cls.data:
                # Create scale factor item
                scale_factor_item = {
                    "ID": scale_factor.ID,
                    "AREA_SF": scale_factor.AREA_SF,
                    "ASY_SF": scale_factor.ASY_SF,
                    "ASZ_SF": scale_factor.ASZ_SF,
                    "IXX_SF": scale_factor.IXX_SF,
                    "IYY_SF": scale_factor.IYY_SF,
                    "IZZ_SF": scale_factor.IZZ_SF,
                    "WGT_SF": scale_factor.WGT_SF,
                    "GROUP_NAME": scale_factor.GROUP_NAME
                }
                
                # Assign to each element ID
                for element_id in scale_factor.ELEMENT_IDS:
                    if str(element_id) not in json_data["Assign"]:
                        json_data["Assign"][str(element_id)] = {"ITEMS": []}
                    
                    json_data["Assign"][str(element_id)]["ITEMS"].append(scale_factor_item)
            
            return json_data
        
        @classmethod
        def create(cls):
            """
            Sends all StiffnessScaleFactor data to the API
            """
            MidasAPI("PUT", "/db/essf", cls.json())
        
        @classmethod
        def get(cls):
            """
            Retrieves StiffnessScaleFactor data from the API
            """
            return MidasAPI("GET", "/db/essf")
        
        @classmethod
        def sync(cls):
            """
            Updates the StiffnessScaleFactor class with data from the API
            """
            cls.data = []
            response = cls.get()
            
            if response != {'message': ''}:
                processed_ids = set()  # To avoid duplicate processing
                
                for element_data in response.get("ESSF", {}).items():
                    for item in element_data.get("ITEMS", []):
                        scale_factor_id = item.get("ID", 1)
                        
                        # Skip if already processed (for multi-element scale factors)
                        if scale_factor_id in processed_ids:
                            continue
                        
                        # Find all elements with the same scale factor ID
                        element_ids = []
                        for eid, edata in response.get("ESSF", {}).items():
                            for eitem in edata.get("ITEMS", []):
                                if eitem.get("ID") == scale_factor_id:
                                    element_ids.append(int(eid))
                        
                        # Create StiffnessScaleFactor object
                        Element.StiffnessScaleFactor(
                            element_id=element_ids if len(element_ids) > 1 else element_ids[0],
                            area_sf=item.get("AREA_SF", 1.0),
                            asy_sf=item.get("ASY_SF", 1.0),
                            asz_sf=item.get("ASZ_SF", 1.0),
                            ixx_sf=item.get("IXX_SF", 1.0),
                            iyy_sf=item.get("IYY_SF", 1.0),
                            izz_sf=item.get("IZZ_SF", 1.0),
                            wgt_sf=item.get("WGT_SF", 1.0),
                            group=item.get("GROUP_NAME", ""),
                            id=scale_factor_id
                        )
                        
                        processed_ids.add(scale_factor_id)
        
        @classmethod
        def delete(cls):
            """
            Deletes all stiffness scale factors from the database and resets the class.
            """
            cls.data = []
            return MidasAPI("DELETE", "/db/essf")




# ---- GET ELEMENT OBJECT FROM ID ----------

# def elemByID2(elemID:int) -> Element:
#     ''' Return Element object with the input ID '''
#     for elem in Element.elements:
#         if elem.ID == elemID:
#             return elem
        
#     print(f'There is no element with ID {elemID}')
#     return None

def elemByID(elemID:int) -> Element:
    ''' Return Element object with the input ID '''
    try:
        return (Element.__elemDIC__[str(elemID)])
    except:
        print(Fore.RED +f'There is no element with ID {elemID}'+Style.RESET_ALL)
        return None
