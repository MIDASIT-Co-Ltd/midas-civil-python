# Importing the midas-gen package
from midas_gen import *

# Sets the MAPI Key 
MAPI_KEY('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

# ============= INPUT =========================================================

Floor_Height = 3.15
Num_of_Floors = 15
Grnd_Floor_Height = 4
length = 8     # Bay Width in X Direction
width = 6.75   # Bay Width in Y Direction
Num_x = 10     # Number of Bay in X Direction
Num_y = 5      # Number of Bay in Y Direction


#================================= Main Code===================================
from math import atan2
def find_all_closed_loops(edge_list):
    """Finds all minimal closed faces (slab panels) from a list of 2D edges."""
    unique_edges = set()
    for a, b in edge_list:
        unique_edges.add((min(a, b), max(a, b)))

    adj = {}
    for (a, b) in unique_edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)

    for pt, nbrs in adj.items():
        nbrs.sort(key=lambda n: atan2(n[1] - pt[1], n[0] - pt[0]))

    def next_half_edge(u, v):
        nbrs = adj[v]
        idx  = nbrs.index(u)
        w    = nbrs[(idx - 1) % len(nbrs)]
        return w

    visited = set()
    faces   = []

    for (a, b) in unique_edges:
        for (start_u, start_v) in [(a, b), (b, a)]:
            if (start_u, start_v) in visited:
                continue

            face   = []
            u, v   = start_u, start_v
            safety = 0
            max_steps = len(unique_edges) * 2 + 10

            while (u, v) not in visited:
                visited.add((u, v))
                face.append(u)
                u, v   = v, next_half_edge(u, v)
                safety += 1
                if safety > max_steps:
                    break

            if len(face) >= 3:
                faces.append(face)

    def signed_area(poly):
        n, acc = len(poly), 0.0
        for i in range(n):
            x0, y0 = poly[i]
            x1, y1 = poly[(i + 1) % n]
            acc   += (x0 * y1 - x1 * y0)
        return acc / 2.0

    if not faces:
        return []

    outer_idx   = max(range(len(faces)), key=lambda i: abs(signed_area(faces[i])))
    inner_faces = [f for i, f in enumerate(faces) if i != outer_idx]

    result = []
    for f in inner_faces:
        if signed_area(f) < 0:
            f = f[::-1]
        result.append(f)

    return result

# ====================================================================
# 2D GRID GENERATION

nodes_xy = set()
beams_xy = []
walls_xy = []

# Generate all XY Nodes
for i in range(Num_x + 1):
    for j in range(Num_y + 1):
        nodes_xy.add((i * length, j * width))

# Generate Beams in X-direction
for i in range(Num_x):
    for j in range(Num_y + 1):
        s = (i * length, j * width)
        t = ((i + 1) * length, j * width)
        beams_xy.append((s, t))

# Generate Beams and Walls in Y-direction
for i in range(Num_x + 1):
    for j in range(Num_y):
        s = (i * length, j * width)
        t = (i * length, (j + 1) * width)

        # Original script logic: walls are located at X=1 & X=Num_x-1, spanning Y=1 to Y=2.
        if (i == 1 or i == Num_x - 1) and (j == 1):
            walls_xy.append((s, t))
        else:
            beams_xy.append((s, t))


all_horizontal_edges_xy = beams_xy + walls_xy
all_loops_xy = find_all_closed_loops(all_horizontal_edges_xy)

# ====================================================================
# Define Material & Section
Model.units()  

Material.CONC('M30', "IS(RC)", 'M30', 1)
CreepShrinkage.IRC("M30", fck = 40000)               
CompStrength.IRC("M30", 2011, 42000, 2)       
TDMatLink(1, "M30", "M30")

Section.DBUSER("Column", "SB", [0.6, 0.6], Offset.CC(), True, False, 1)   
Section.DBUSER("Beam", "SB", [0.5, 0.6], Offset.CC(), True, False, 2)     
Thickness(0.45, name="1")

# ====================================================================
# Model Creation

z_levels = [0.0, Grnd_Floor_Height]
for i in range(1, Num_of_Floors + 1):
    z_levels.append(Grnd_Floor_Height + i * Floor_Height)

node_id_counter = [0]
xyz_to_node_id  = {}

def _r(v): return round(v, 3)

def register_node(x, y, z):
    """Simulates MIDAS implicit node numbering so we can access IDs for Loads/Walls."""
    key = (_r(x), _r(y), _r(z))
    if key not in xyz_to_node_id:
        node_id_counter[0] += 1
        xyz_to_node_id[key] = node_id_counter[0]
    return xyz_to_node_id[key]

nodes_xy_list = sorted(list(nodes_xy))

# ──  Columns (Vertical Elements) ──
for (x, y) in nodes_xy_list:
    for i in range(len(z_levels) - 1):
        z1 = z_levels[i]
        z2 = z_levels[i + 1]
        register_node(x, y, z1)
        register_node(x, y, z2)
        Element.Beam.SE([x, y, z1], [x, y, z2], n=1, mat=1, sect=1, angle=0, group=f'CS{i+1}')

# ──  Beams (Horizontal Elements) ──
for (s_xy, e_xy) in beams_xy:
    for i in range(1, len(z_levels)):
        z = z_levels[i]
        register_node(s_xy[0], s_xy[1], z)
        register_node(e_xy[0], e_xy[1], z)
        Element.Beam.SE([s_xy[0], s_xy[1], z], [e_xy[0], e_xy[1], z], n=1, mat=1, sect=2, angle=0, group=f'CS{i}')

# ──  Walls (Vertical Panels) ──
for (s_xy, e_xy) in walls_xy:
    for i in range(1, len(z_levels)):
        z1 = z_levels[i-1]
        z2 = z_levels[i]

        n1 = register_node(s_xy[0], s_xy[1], z1)
        n2 = register_node(e_xy[0], e_xy[1], z1)
        n3 = register_node(e_xy[0], e_xy[1], z2)
        n4 = register_node(s_xy[0], s_xy[1], z2)

        Element.Wall([n1, n2, n3, n4], 1, 0, group=f'CS{i}')


# ====================================================================
# SUPPORTS & LOAD CASES

Boundary.Support(Model.Select.Plane_XY((0, 0, 0), "NODE_ID"), 1111111, "Supports")

Load_Case("D", "DL")
Load_Case("L", "LL")
Load_Case("L", "FL1")
Load_Case("L", "FL2")

Group.Load("SW")
for i in range(1, len(z_levels)):
    Group.Load(f'CS{i}')

Load.SW("DL", "Z", -1, "SW")

Load.FloorLoadDefine("FL Type 1", [["FL1", -6.5, True], ["LL", -2, False]])
Load.FloorLoadDefine("FL Type 2", [["FL2", -5.5, True]])

# ====================================================================
# FLOOR LOAD ASSIGNMENTS

for floor_idx in range(1, len(z_levels)):
    z = z_levels[floor_idx]

    for loop_idx, loop_xy in enumerate(all_loops_xy):
        loop_node_ids = []
        for (x, y) in loop_xy:
            key = (_r(x), _r(y), _r(z))
            if key in xyz_to_node_id:
                loop_node_ids.append(xyz_to_node_id[key])

        if len(loop_node_ids) >= 3:
            Load.FloorLoadAssign("FL Type 1", distribution_type=2, direction="GZ", node_list=loop_node_ids, group=f'CS{floor_idx}')
            Load.FloorLoadAssign("FL Type 2", distribution_type=2, direction="GZ", node_list=loop_node_ids, group=f'CS{floor_idx}')

# ====================================================================
# CONSTRUCTION STAGES

for k in range(1, len(z_levels)):
    b_group = "Supports" if k == 1 else None
    l_group = ["SW", "CS1"] if k == 1 else f'CS{k}'
    CS.STAGE(f'CS{k}', 7, f'CS{k}', 7, b_group=b_group, l_group=l_group)

Model.create()