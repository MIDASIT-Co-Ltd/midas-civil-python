from ._mapi import MidasAPI
from ._utils import zz_add_to_dict,_convItem2List , sFlatten
from math import hypot
from ._group import _add_node_2_stGroup
from typing import Literal
import numpy as np
from ._group import Group

def dist_tol(a, b):
    """Return ``True`` if two nodes are within the merge tolerance (0.00001 units).

    Uses 3-D Euclidean distance. The tolerance is unit-independent — it is the
    caller's responsibility to work in consistent units.

    Args:
        a: Node-like object with ``X``, ``Y``, ``Z`` float attributes.
        b: Node-like object with ``X``, ``Y``, ``Z`` float attributes.

    Returns:
        bool: ``True`` when the distance between ``a`` and ``b`` is less than ``0.00001``.
    """
    return hypot((a.X-b.X),(a.Y-b.Y),(a.Z-b.Z)) < 0.00001  #TOLERANCE BUILT IN (UNIT INDEP)

def cell(point, size=1):
    """Return the spatial grid cell key for a node location.

    The grid is used to accelerate proximity searches (merge and closest-node
    lookups) by bucketing nodes into integer-unit cells.

    Args:
        point: Object with ``X``, ``Y``, ``Z`` float attributes.
        size (int): Intended cell size (currently unused — cells are always 1 unit wide).

    Returns:
        str: Cell key in the form ``"ix,iy,iz"`` where each component is ``int(coord)``.
    """
    # return str(f"{int(point.X//size)},{int(point.Y//size)},{int(point.Z//size)}")
    return str(f"{int(point.X)},{int(point.Y)},{int(point.Z)}")

# def _cellGrid():
#     [float(x.strip()) for x in list(Node.Grid.keys())split(",")]
# -------- FUNCTIONS ARE DEFINED BELOW TO RECOGNISE NODE CLASS ----------------


class _hNode:
    ID,X,Y,Z,AXIS,LOC = 0,0,0,0,0,0

class Node:
    """Represents a single node in the MIDAS Civil NX model.

    Class Attributes:
        nodes (list[_hNode]): All node objects in the current session.
        ids (list[int]): IDs of all registered nodes (parallel to ``nodes``).

    Example::

        n1 = Node(0, 0, 0, id=1, group='Support')
        n2 = Node(5, 0, 0)          # auto-incremented ID
        n3 = Node(0, 0, 0, merge=True)  # returns n1 — no duplicate created
    """

    nodes: list[_hNode] = []
    ids: list[int] = []
    Grid = {}
    __nodeDic__ = {}

    def __init__(self, x: float, y: float, z: float, id: int = None, group: str = '', merge: bool = True):
        """Create (or retrieve) a node at the given coordinates.

        Parameters:
            x: X - ordinate of node
            y: Y - ordinate of node 
            z: Z - ordinate of node
            id: Node ID (default 0 for auto-increment)
            mat: Material property number (default 1)
            group: Structure group of the element (str or list; 'SG1' or ['SG1','SG2'])
            merge: If enabled, checks for existing nodes and return their IDs. No additional/duplicate node will be created.
        

        Example::

            Node(0, 0, 0, id=1, group='Support', merge=True)
            Node(5, 0, 0)                # auto-ID, no group

        **ID assignment:**
        - ``id=None`` (default) → auto-incremented to ``max(existing IDs) + 1``.
        - ``id`` already exists in the database → the existing node is
          *replaced* with the new coordinates (no merge check).
        - ``id`` is new → a new node is created with that exact ID.

        """

        if id == None: id =0
        #----------------- ORIGINAL -----------------------
    
        if Node.ids == []: 
            node_count = 1
        else:
            node_count = max(Node.ids)+1
        
        
        self.X = round(x,6)
        self.Y = round(y,6)
        self.Z = round(z,6)
        self.AXIS = [[0,0,0],[0,0,0],[0,0,0]]

        if id == 0 : self.ID = node_count
        if id != 0 : self.ID = id


        #REPLACE - No merge check
        if id in Node.ids:

            index=Node.ids.index(id)
            n_orig = Node.nodes[index]
            loc_orig = str(cell(n_orig))
            Node.Grid[loc_orig].remove(n_orig)

            loc_new = str(cell(self))
            
            zz_add_to_dict(Node.Grid,loc_new,self)
            Node.nodes[index]=self
            Node.__nodeDic__[str(id)] = self


        #CREATE NEW - Merge Check based on input
        else:
            cell_loc = str(cell(self))      

            if cell_loc in Node.Grid:

                if merge :
                    chk=0   #OPTIONAL
                    for node in Node.Grid[cell_loc]:
                        if dist_tol(self,node):
  
                            chk=1
                            self.ID=node.ID
                            self.AXIS = node.AXIS
                    if chk==0:

                        Node.nodes.append(self)
                        Node.ids.append(self.ID)
                        Node.Grid[cell_loc].append(self)
                        

                else:

                    Node.nodes.append(self)
                    Node.ids.append(self.ID)
                    Node.Grid[cell_loc].append(self)
            else:

                Node.Grid[cell_loc]=[]
                Node.nodes.append(self)
                Node.ids.append(self.ID)
                Node.Grid[cell_loc].append(self)
            Node.__nodeDic__[str(self.ID)] = self
            
        if group !="":
            _add_node_2_stGroup(self.ID,group)

    @property
    def LOC(self):
        """Return the node coordinates as a ``(X, Y, Z)`` tuple."""
        return (self.X,self.Y,self.Z)

    def __str__(self):
        return f"NODE ID : {self.ID} | X:{self.X} , Y:{self.Y} , Z:{self.Z} \n{self.__dict__}"

    @classmethod
    def json(cls):
        """Serialise all nodes to the MIDAS API JSON format.

        Returns:
            dict: ``{"Assign": {id: {"X": x, "Y": y, "Z": z}, ...}}`` ready
            for the ``/db/NODE`` endpoint.
        """
        json = {"Assign":{}}
        for i in cls.nodes:
            json["Assign"][i.ID]={"X":i.X,"Y":i.Y,"Z":i.Z}
        return json

    @classmethod
    def create(cls):
        """Send all nodes to MIDAS Civil NX (PUT /db/NODE).

        """
        __maxNos__ = 40_000  #40_000 nodes can be sent in a single request
        __numItem__ = len(cls.nodes)
        __nTime__ = int(__numItem__/__maxNos__)+1

        if __nTime__ == 1:
            MidasAPI("PUT","/db/NODE",Node.json())
        else:
            __remainItem__ = __numItem__
            for n in range(__nTime__):
                json = {"Assign":{}}
                __nNode_c__ = min(__maxNos__,__remainItem__)
                for q in range(__nNode_c__):
                    i=cls.nodes[n*__maxNos__+q]
                    json["Assign"][i.ID]={"X":i.X,"Y":i.Y,"Z":i.Z}
                MidasAPI("PUT","/db/NODE",json)
                __remainItem__ -= __maxNos__

        
    @staticmethod
    def get():
        """Retrieve all nodes from MIDAS Civil NX (GET /db/NODE).

        Returns:
            dict: Raw API response containing the ``'NODE'`` dictionary keyed
            by node ID strings.
        """
        return MidasAPI("GET","/db/NODE")

    @staticmethod
    def sync():
        """Retrieve all nodes from MIDAS Civil NX and rebuild the local database.

        Clears the current database, fetches all nodes via ``GET /db/NODE``,
        and recreates the local database.
        """
        Node.clear()
        a = Node.get()
        if a != {'message': ''}:
            if list(a['NODE'].keys()) != []:
                for j in a['NODE'].keys():
                    Node(round(a['NODE'][j]['X'],6), round(a['NODE'][j]['Y'],6), round(a['NODE'][j]['Z'],6), id=int(j), group='', merge=False)

    @staticmethod
    def delete():
        """Delete all nodes from MIDAS Civil NX and clear the local database."""
        MidasAPI("DELETE","/db/NODE")
        Node.clear()

    @staticmethod
    def clear():
        """Clear the local node database without affecting the MIDAS model."""
        Node.nodes=[]
        Node.ids=[]
        Node.Grid={}
        Node.__nodeDic__ = {}

    @staticmethod
    def SE(s_loc: list, e_loc: list, n: int = 1, id: int = None, group: str = '', merge: bool = True):
        """Create ``n+1`` equally spaced nodes along a straight line (Start–End).

        Args:
            s_loc (list[float] | Node): Start location ``[x, y, z]`` or a
                ``Node`` object.
            e_loc (list[float] | Node): End location ``[x, y, z]`` or a
                ``Node`` object.
            n (int): Number of divisions. Creates ``n+1`` nodes including both
                end points. Default ``1`` (just the two end nodes).
            id (int | None): Starting ID for the first node. Subsequent nodes
                receive ``id+1``, ``id+2``, … Auto-assigned when ``None``.
            group (str | list[str]): Structure group(s) to assign each node to.
            merge (bool): Enable duplicate-node suppression. Default ``True``.

        Returns:
            list[Node]: ``n+1`` node objects from start to end inclusive.

        Example::

            nodes = Node.SE([0,0,0], [10,0,0], n=5)   # 6 nodes at x = 0,2,4,6,8,10
        """
        id_new = None
        if isinstance(s_loc,Node):
            s_loc = (s_loc.X,s_loc.Y,s_loc.Z)
        if isinstance(e_loc,Node):
            e_loc = (e_loc.X,e_loc.Y,e_loc.Z)

        beam_nodes =[]
        i_loc = np.linspace(s_loc,e_loc,n+1)
        for i in range(n+1):
            if id != None : id_new = id+i
            beam_nodes.append(Node(i_loc[i][0].item(),i_loc[i][1].item(),i_loc[i][2].item(),id_new,group,merge))

        return beam_nodes

    @staticmethod
    def SDL(s_loc: list, dir: list, l: float, n: int = 1, id: int = None, group: str = '', merge: bool = True):
        """Create ``n+1`` equally spaced nodes along a direction vector (Start–Direction–Length).

        Args:
            s_loc (list[float] | Node): Start location ``[x, y, z]`` or a
                ``Node`` object.
            dir (list[float]): Direction vector ``[dx, dy, dz]``. Does not
                need to be a unit vector — it is normalised internally.
            l (float): Total length along the direction.
            n (int): Number of divisions. Creates ``n+1`` nodes. Default ``1``.
            id (int | None): Starting ID for the first node. Subsequent nodes
                receive ``id+1``, ``id+2``, … Auto-assigned when ``None``.
            group (str | list[str]): Structure group(s) to assign each node to.
            merge (bool): Enable duplicate-node suppression. Default ``True``.

        Returns:
            list[Node]: ``n+1`` node objects along the specified direction.

        Example::

            nodes = Node.SDL([0,0,0], [1,0,0], l=10, n=4)  # 5 nodes at x=0,2.5,5,7.5,10
        """
        if isinstance(s_loc,Node):
            s_loc = (s_loc.X,s_loc.Y,s_loc.Z)

        beam_nodes =[]
        s_locc = np.array(s_loc)
        unit_vec = np.array(dir)/np.linalg.norm(dir)

        for i in range(n+1):
            if id != None : id_new = id+i
            else: id_new = None
            locc = s_locc+i*l*unit_vec/n
            beam_nodes.append(Node(locc[0].item(),locc[1].item(),locc[2].item(),id_new,group,merge))

        return beam_nodes

    @staticmethod
    def fromList(nodesList: list, id: int = None, group: str = '', merge: bool = True):
        """Create nodes from a list of coordinate triplets.

        Args:
            nodesList (list[list[float]]): List of ``[x, y, z]`` coordinate
                lists, e.g. ``[[0,0,0], [1,0,0], [2,0,0]]``.
            id (int | None): Starting ID for the first node. Subsequent nodes
                receive ``id+1``, ``id+2``, … Auto-assigned when ``None``.
            group (str | list[str]): Structure group(s) to assign each node to.
            merge (bool): Enable duplicate-node suppression. Default ``True``.

        Returns:
            list[Node]: Node objects created from the input list, in order.

        Example::

            pts = [[0,0,h] for h in range(10)]
            nodes = Node.fromList(pts, group='Column')
        """
        beam_nodes=[]
        for i,pt in enumerate(nodesList):
            if id != None : id_new = id+i
            else: id_new = None
            beam_nodes.append(Node(pt[0],pt[1],pt[2],id_new,group,merge))

        return beam_nodes
    




# ---- GET NODE OBJECT FROM ID ----------

# def nodeByID(nodeID:int) -> Node:
#     ''' Return Node object with the input ID '''
#     for node in Node.nodes:
#         if node.ID == nodeID:
#             return node
        
#     print(f'There is no node with ID {nodeID}')
#     return None

def nodesInGroup(groupName: str, unique: bool = True, reverse: bool = False, output: Literal['ID','NODE'] = 'ID') -> list:
    """Return node IDs (or Node objects) belonging to one or more structure groups.

    Args:
        groupName (str | list[str]): Structure group name or list of names.
            E.g. ``'SG_A'`` or ``['SG_1', 'SG_2', 'SG_3']``.
        unique (bool): When ``True``, duplicate IDs that appear in multiple
            groups are removed, preserving first-occurrence order. Default ``True``.
        reverse (bool): Reverse the node list of every group before returning.
            Default ``False``.
        output (Literal['ID', 'NODE']): Return format.
            - ``'ID'`` (default) → list of integer node IDs.
            - ``'NODE'`` → list of ``Node`` objects.

    Returns:
        list[int] | list[Node]: Node IDs or Node objects, depending on
        ``output``.

    Example::

        ids = nodesInGroup('Deck')
        ids = nodesInGroup(['Pier_1', 'Pier_2'], unique=True)
        nodes = nodesInGroup('Support', reverse=True, output='NODE')  # reversed order
    """
    groupNames = _convItem2List(groupName)
    nlist = []
    for gName in groupNames:
        chk=1
        for i in Group.Structure.Groups:
                if i.NAME == gName:
                    chk=0
                    nIDlist = i.NLIST
                    if reverse: nIDlist = list(reversed(nIDlist))
                    nlist.append(nIDlist)
        if chk:
            print(f'⚠️   "{gName}" - Structure group not found !')
    if unique:
        finalNlist = list(dict.fromkeys(sFlatten(nlist)))
    else:
        finalNlist = sFlatten(nlist)

    if output == 'NODE':
        finoutput = []
        for nod in finalNlist:
            finoutput.append(nodeByID(nod))
        finalNlist:Node = finoutput

    return finalNlist

def nodeByID(nodeID: int) -> Node:
    """Return the Node object for the given ID .

    Args:
        nodeID (int): Node database ID to look up.

    Returns:
        Node | None: The matching node object, or ``None`` if no node with
        that ID exists.

    Example::

        n = nodeByID(42)
        print(n.X, n.Y, n.Z)
    """
    try:
        return (Node.__nodeDic__[str(nodeID)])
    except:
        print(f'There is no node with ID {nodeID}')
        return None

def closestNode(point_location) -> Node:
    """Find the nearest node in the model to a given point.

    When ``point_location`` is a ``Node`` or integer node ID, the input node
    itself is excluded from the result so the *second*-closest node is returned
    — useful for connectivity queries.

    Args:
        point_location (list[float] | Node | int):
            - ``[x, y, z]`` — find the node closest to this coordinate.
            - ``Node`` object — find the closest *other* node to this node.
            - ``int`` (node ID) — find the closest *other* node to that node.

    Returns:
        Node: The nearest node object (excluding the input node if it is a
        ``Node`` or ID).

    Example::

        n = closestNode([5.1, 0, 0])
        n = closestNode(nodeByID(10))   # nearest neighbour of node 10
    """
    gridStr = list(Node.Grid.keys())
    gridInt = []
    for key in gridStr:
        gridInt.append([int(x) for x in key.split(",")])

    bNode = False
    bNodeID = 0
    if isinstance(point_location,int):
        bNode = True
        bNodeID = point_location
        nodeP = nodeByID(point_location)
        point_location = (nodeP.X,nodeP.Y,nodeP.Z)
    elif isinstance(point_location,Node):
        bNode = True
        bNodeID = point_location.ID
        point_location = (point_location.X,point_location.Y,point_location.Z)
    pGridInt = [int(point_location[0]),int(point_location[1]),int(point_location[2])]
    pGridStr = f"{int(point_location[0])},{int(point_location[1])},{int(point_location[2])}"

    min_edge_dist = round(min(point_location[0]-pGridInt[0],point_location[1]-pGridInt[1],point_location[2]-pGridInt[2]),3)
    max_edge_dist = round(max(point_location[0]-pGridInt[0],point_location[1]-pGridInt[1],point_location[2]-pGridInt[2]),3)

    if min_edge_dist > 0.5 : min_edge_dist = round(1-min_edge_dist,3)
    if max_edge_dist > 0.5 : max_edge_dist = round(1-max_edge_dist,3)

    min_edge_dist = min(min_edge_dist,max_edge_dist)

    min_dist = 10000000000  #Large value for initial value
    min_node = 0
    checked_GridInt = []

    if bNode and len(Node.Grid[pGridStr]) == 1:
        gridDist = []
        for gInt in gridInt:
            gridDist.append(abs(gInt[0]-pGridInt[0])+abs(gInt[1]-pGridInt[1])+abs(gInt[2]-pGridInt[2]))
        gridDistSort = sorted(gridDist)

        nearestGridIdx = gridDist.index(gridDistSort[1])
        nearestGridInt = gridInt[nearestGridIdx]
        nearestGridStr = gridStr[nearestGridIdx]
    else:
        if pGridInt in gridInt :
            nearestGridInt = pGridInt
            nearestGridStr = pGridStr
        else :
            gridDist = []
            for gInt in gridInt:
                gridDist.append(abs(gInt[0]-pGridInt[0])+abs(gInt[1]-pGridInt[1])+abs(gInt[2]-pGridInt[2]))

            nearestGridIdx = gridDist.index(min(gridDist))
            nearestGridInt = gridInt[nearestGridIdx]
            nearestGridStr = gridStr[nearestGridIdx]

    for nd in Node.Grid[nearestGridStr]:
        dist = hypot(nd.X-point_location[0],nd.Y-point_location[1],nd.Z-point_location[2])
        if dist < min_dist and nd.ID !=bNodeID:
            min_dist = dist
            min_node = nd
    checked_GridInt.append(nearestGridInt)
    if min_dist < min_edge_dist :
        return min_node
    
    else:
        # COMBINATION POSSIBLE FOR CELLS
        minX = int(point_location[0]-min_dist)
        maxX = int(point_location[0]+min_dist)
        minY = int(point_location[1]-min_dist)
        maxY = int(point_location[1]+min_dist)
        minZ = int(point_location[2]-min_dist)
        maxZ = int(point_location[2]+min_dist)
        possible = maxX+maxY+maxZ-minX-minY-minZ
        if possible == 0:
            return min_node

        for i in np.arange(minX,maxX+1,1):
            for j in np.arange(minY,maxY+1,1):
                for k in np.arange(minZ,maxZ+1,1):
                    cgridStr = f"{i},{j},{k}"
                    cgridInt = [i,j,k]

                    if cgridInt in checked_GridInt:
                        continue
                    else:
                        if cgridInt in gridInt:
                            for nd in Node.Grid[cgridStr]:
                                dist = hypot(nd.X-point_location[0],nd.Y-point_location[1],nd.Z-point_location[2])
                                if dist < min_dist and nd.ID !=bNodeID:
                                    min_dist = dist
                                    min_node = nd
                        checked_GridInt.append(cgridInt)
        return min_node

def _ifNodeExist_(x, y, z) -> tuple:
    """Check whether a node already exists at the given coordinates.

    Searches the spatial grid cell that contains ``(x, y, z)`` and tests each
    node in that cell against the standard merge tolerance (``0.00001`` units).

    Args:
        x (float): X-coordinate.
        y (float): Y-coordinate.
        z (float): Z-coordinate.

    Returns:
        tuple[bool, int]: ``(True, node_id)`` if a matching node exists,
        otherwise ``(False, 0)``.
    """
    cell_loc = str(f"{int(x)},{int(y)},{int(z)}")
    if cell_loc in Node.Grid:
        for node in Node.Grid[cell_loc]:
            if hypot((x-node.X),(y-node.Y),(z-node.Z)) < 0.00001 :
                return True,node.ID
    return False,0


def nodesInRadius(point_location, radius: float = 0, output: Literal['ID','NODE'] = 'ID', includeSelf: bool = False) -> list:
    """Return all nodes within a spherical radius of a given point.

    Args:
        point_location (list[float] | Node | int):
            - ``[x, y, z]`` — centre of the search sphere.
            - ``Node`` object — search around that node's coordinates.
            - ``int`` (node ID) — search around the node with that ID.
        radius (float): Search radius in model units. Default ``0`` (returns
            only coincident nodes).
        output (Literal['ID', 'NODE']): Return format.
            - ``'ID'`` (default) → list of integer node IDs.
            - ``'NODE'`` → list of ``Node`` objects.
        includeSelf (bool): When ``point_location`` is a ``Node`` or ID,
            include that node itself in the result. Default ``False``.

    Returns:
        list[int] | list[Node]: Nodes within the radius, depending on
        ``output``.

    Example::

        ids = nodesInRadius([5, 0, 0], radius=2.0)
        ids = nodesInRadius(nodeByID(10), radius=1.5, includeSelf=True)
    """
    gridStr = list(Node.Grid.keys())

    bNode = False
    id2Remove = 0
    if isinstance(point_location,int):
        bNode = True
        id2Remove = point_location
        nodeP = nodeByID(point_location)
        point_location = (nodeP.X,nodeP.Y,nodeP.Z)
        
    elif isinstance(point_location,Node):
        bNode = True
        id2Remove = point_location.ID
        point_location = (point_location.X,point_location.Y,point_location.Z)

    if not includeSelf and not bNode:
        bNode,id2Remove = _ifNodeExist_(point_location[0],point_location[1],point_location[2])

    ifRemove = bNode and not includeSelf

    checked_GridStr = []
    close_nodes:list[int] = []
    close_nodesID:list[Node] = []


    minX = int(point_location[0]-radius)
    maxX = int(point_location[0]+radius)
    minY = int(point_location[1]-radius)
    maxY = int(point_location[1]+radius)
    minZ = int(point_location[2]-radius)
    maxZ = int(point_location[2]+radius)

    for i in np.arange(minX,maxX+1,1):
        for j in np.arange(minY,maxY+1,1):
            for k in np.arange(minZ,maxZ+1,1):
                cgridStr = f"{i},{j},{k}"
                if cgridStr in checked_GridStr:
                    # print("Grid already checked")
                    continue
                else:
                    if cgridStr in gridStr:
                        for nd in Node.Grid[cgridStr]:
                            dist = hypot(nd.X-point_location[0],nd.Y-point_location[1],nd.Z-point_location[2])
                            if dist <= radius+0.0001 :
                                close_nodes.append(nd)
                                close_nodesID.append(nd.ID)
                    checked_GridStr.append(cgridStr)

    if output == 'NODE':
        if ifRemove:
            close_nodes.remove(nodeByID(id2Remove))
            return close_nodes
    if ifRemove:
        close_nodesID.remove(id2Remove)
    return close_nodesID



class NodeLocalAxis:
    """Define a local coordinate axis for one or more nodes.

    In MIDAS Civil NX, nodes can have a local axis orientation different from
    the global axis. This is used to apply boundary conditions or interpret
    results in a skewed (rotated) coordinate system.

    Two definition methods are supported:

    - **Angle** (``type='X'``, ``'Y'``, ``'Z'``, or ``'XYZ'``): Rotations
      about one or more global axes in degrees. Corresponds to API
      ``iMETHOD = 1``.
    - **Vector** (``type='Vector'``): Explicit definition of the local X and Y
      axes as unit vectors. Corresponds to API ``iMETHOD = 3``.

    If a ``NodeLocalAxis`` is created for a node that already has an entry,
    the existing entry is updated (axes are composed for single-axis types).

    Class Attributes:
        skew (list): All ``NodeLocalAxis`` objects in the current session.
        ids (list[int]): Node IDs with a registered local axis.

    Example::

        NodeLocalAxis(5, 'Z', 30)               # rotate node 5 by 30° about Z
        NodeLocalAxis(5, 'X', 15)               # compose: now Z=30, X=15
        NodeLocalAxis(7, 'XYZ', [0, 0, 45])     # full Euler angle triplet
        NodeLocalAxis(9, 'Vector', [[1,0,0],[0,0,1]])  # explicit local X and Y
    """

    skew = []
    ids = []

    def __init__(self, nodeID: int, type: Literal['X', 'Y', 'Z', 'XYZ', 'Vector'], angle):
        """Define or update the local axis orientation for a node.

        Args:
            nodeID (int): ID of the node to assign the local axis to.
            type (Literal['X', 'Y', 'Z', 'XYZ', 'Vector']): Definition method:
                - ``'X'`` — rotation angle (degrees) about the global X-axis.
                - ``'Y'`` — rotation angle (degrees) about the global Y-axis.
                - ``'Z'`` — rotation angle (degrees) about the global Z-axis.
                - ``'XYZ'`` — list of three rotation angles ``[rx, ry, rz]``
                  applied as Euler angles.
                - ``'Vector'`` — list of two direction vectors
                  ``[[v1x,v1y,v1z], [v2x,v2y,v2z]]`` defining the local X
                  and Y axes explicitly.
            angle (float | list): Angle value(s) or vector list, matching the
                ``type`` chosen above.

        Note:
            When updating an existing entry with a single-axis type (``'X'``,
            ``'Y'``, or ``'Z'``), the other two axis angles are preserved from
            the existing definition.

        Example::

            NodeLocalAxis(10, 'Z', 30)
            NodeLocalAxis(10, 'X', 15)              # updates node 10: Z=30, X=15
            NodeLocalAxis(20, 'XYZ', [0, 45, 0])
            NodeLocalAxis(30, 'Vector', [[1,0,0], [0,0,1]])
        """

        self.ID = nodeID

        if nodeID in NodeLocalAxis.ids:
            index = NodeLocalAxis.ids.index(nodeID)
            intial_angle = NodeLocalAxis.skew[index].ANGLE
            if intial_angle == [[0,0,0],[0,0,0],[0,0,0]]:
                intial_angle = [[1,0,0],[0,1,0],[0,0,1]]

            if type == 'Vector':
                self.TYPE = 'VEC'
                self.VEC = angle
            elif type == 'X':
                self.TYPE = 'ANGLE'
                self.ANGLE = [angle,intial_angle[1],intial_angle[2]]
            elif type == 'Y':
                self.TYPE = 'ANGLE'
                self.ANGLE = [intial_angle[0],angle,intial_angle[2]]
            elif type == 'Z':
                self.TYPE = 'ANGLE'
                self.ANGLE = [intial_angle[0],intial_angle[1],angle]
            elif type == 'XYZ':
                self.TYPE = 'ANGLE'
                self.ANGLE = angle
            NodeLocalAxis.skew[index] = self
        else:
            if type == 'Vector':
                self.TYPE = 'VEC'
                self.VEC = angle
                self.ANGLE = [0,0,0]
            elif type == 'X':
                self.TYPE = 'ANGLE'
                self.ANGLE = [angle,0,0]
            elif type == 'Y':
                self.TYPE = 'ANGLE'
                self.ANGLE = [0,angle,0]
            elif type == 'Z':
                self.TYPE = 'ANGLE'
                self.ANGLE = [0,0,angle]
            elif type == 'XYZ':
                self.TYPE = 'ANGLE'
                self.ANGLE = angle
        
            NodeLocalAxis.skew.append(self)
            NodeLocalAxis.ids.append(self.ID)

    @classmethod
    def json(cls):
        """Serialise all local axis definitions to the MIDAS API JSON format.

        Returns:
            dict: ``{"Assign": {node_id: {...}, ...}}`` ready for the
            ``/db/SKEW`` endpoint.
        """
        json = {"Assign":{}}
        for i in cls.skew:
            if i.TYPE == 'ANGLE':
                json["Assign"][i.ID]={
                                    "iMETHOD": 1,
                                    "ANGLE_X": i.ANGLE[0],
                                    "ANGLE_Y": i.ANGLE[1],
                                    "ANGLE_Z": i.ANGLE[2]
                                }
            elif i.TYPE == 'VEC':
                json["Assign"][i.ID]={
                                    "iMETHOD": 3,
                                    "V1X": i.VEC[0][0],
                                    "V1Y": i.VEC[0][1],
                                    "V1Z": i.VEC[0][2],
                                    "V2X": i.VEC[1][0],
                                    "V2Y": i.VEC[1][1],
                                    "V2Z": i.VEC[1][2]
                                }
        return json

    @staticmethod
    def create():
        """Push all local axis definitions to MIDAS Civil NX (PUT /db/SKEW)."""
        MidasAPI("PUT","/db/SKEW",NodeLocalAxis.json())

    @staticmethod
    def delete():
        """Delete all local axis definitions from MIDAS Civil NX and clear the local database."""
        MidasAPI("DELETE","/db/SKEW")
        NodeLocalAxis.clear()

    @staticmethod
    def clear():
        """Clear the local axis database without affecting the MIDAS model."""
        NodeLocalAxis.skew=[]
        NodeLocalAxis.ids=[]

    @staticmethod
    def get():
        """Retrieve all node local axis definitions from MIDAS Civil NX (GET /db/SKEW).

        Returns:
            dict: Raw API response containing the ``'SKEW'`` dictionary keyed
            by node ID strings.
        """
        return MidasAPI("GET","/db/SKEW")
    
    # @staticmethod
    # def sync():
    #     NodeLocalAxis.skew=[]
    #     NodeLocalAxis.ids=[]
    #     a = NodeLocalAxis.get()
    #     if a != {'message': ''}:
    #         if list(a['NODE'].keys()) != []:

    #             for j in a['NODE'].keys():

    #                 Node(round(a['NODE'][j]['X'],6), round(a['NODE'][j]['Y'],6), round(a['NODE'][j]['Z'],6), id=int(j), group='', merge=0)