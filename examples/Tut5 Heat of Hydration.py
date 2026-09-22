#IMPORTING MIDAS CIVIL LIBRARY LOCALHOST
from midas_civil import *


# --- Inputs ---
MESH_SIZE = 80
MESH_SIZE_Z = 60

SUBSOIL_L_X = 1200
SUBSOIL_L_Y = 960
SUBSOIL_H_Z = 300

OFF_L_X = 480
OFF_L_Y = 480

MAT_H_LOWER_Z = 240
MAT_H_TOTAL_Z = 480


# --- Geometry ---
n_x = int(SUBSOIL_L_X / MESH_SIZE)
n_y = int(SUBSOIL_L_Y / MESH_SIZE)
n_sub_soil = int(SUBSOIL_H_Z / MESH_SIZE_Z)
offset_nplatesx = int(OFF_L_X / MESH_SIZE)
offset_nplatesy = int(OFF_L_Y / MESH_SIZE)

n_x_2 = n_x - offset_nplatesx
n_y_2 = n_y - offset_nplatesy

n_mat_foundation_lower = int(MAT_H_LOWER_Z / MESH_SIZE_Z)
n_mat_foundation_total = int(MAT_H_TOTAL_Z / MESH_SIZE_Z)
n_mat_foundation_upper = n_mat_foundation_total - n_mat_foundation_lower


# SubSoil level
Node.SE((0, 0, 0), (n_x * MESH_SIZE, 0, 0), n_x, group='#L0_A')
Node.SE((0, n_y * MESH_SIZE, 0), (n_x * MESH_SIZE, n_y * MESH_SIZE, 0), n_x, group='#L0_B')
Element.Plate.loftGroups(['#L0_A', '#L0_B'], nDiv=n_y, group='#PlateGrid_L0')
Element.Solid.extrudeFromPlates(elemsInGroup('#PlateGrid_L0'),(0, 0, MESH_SIZE_Z * n_sub_soil),n_sub_soil,mat=2,group='Subsoil',bDeletePlate=True)


# Mat Foundation (lower part)
z1 = MESH_SIZE_Z * n_sub_soil
x0 = offset_nplatesx * MESH_SIZE

Node.SE((x0, 0, z1), (x0 + n_x_2 * MESH_SIZE, 0, z1), n_x_2, group='#L1_A')
Node.SE((x0, n_y_2 * MESH_SIZE, z1), (x0 + n_x_2 * MESH_SIZE, n_y_2 * MESH_SIZE, z1), n_x_2, group='#L1_B')
Element.Plate.loftGroups(['#L1_A', '#L1_B'], nDiv=n_y_2, group='#PlateGrid_L1')
Element.Solid.extrudeFromPlates(elemsInGroup('#PlateGrid_L1'),(0, 0, MESH_SIZE_Z * n_mat_foundation_lower),n_mat_foundation_lower,mat=1,group='Mat Foundation (Lower Part)',bDeletePlate=True)

# Mat Foundation (upper part)
z2 = MESH_SIZE_Z * (n_sub_soil + n_mat_foundation_lower)

Node.SE((x0, 0, z2), (x0 + n_x_2 * MESH_SIZE, 0, z2), n_x_2, group='#L2_A')
Node.SE((x0, n_y_2 * MESH_SIZE, z2), (x0 + n_x_2 * MESH_SIZE, n_y_2 * MESH_SIZE, z2), n_x_2, group='#L2_B')
Element.Plate.loftGroups(['#L2_A', '#L2_B'], nDiv=n_y_2, group='#PlateGrid_L2')
Element.Solid.extrudeFromPlates(elemsInGroup('#PlateGrid_L2'),(0, 0, MESH_SIZE_Z * n_mat_foundation_upper),n_mat_foundation_upper,mat=1,group='Mat Foundation (Upper Part)',bDeletePlate=True)

# --- Supports ---

X_MAX = n_x * MESH_SIZE
Y_MAX = n_y * MESH_SIZE
Y_MAT = n_y_2 * MESH_SIZE          
Z_TOP = MESH_SIZE_Z * (n_sub_soil + n_mat_foundation_total)


# --- Roller face x = X_MAX, restrain DX ('1000000') ---  
roller_x_cs1 = set()
roller_x_cs1.update(Model.Select.Polygon([(X_MAX, 0, 0), (X_MAX, Y_MAX, 0), (X_MAX, Y_MAX, z1), (X_MAX, 0, z1)]))
roller_x_cs1.update(Model.Select.Polygon([(X_MAX, 0, z1), (X_MAX, Y_MAT, z1), (X_MAX, Y_MAT, z2), (X_MAX, 0, z2)]))
roller_x_cs2 = Model.Select.Polygon([(X_MAX, 0, z2), (X_MAX, Y_MAT, z2), (X_MAX, Y_MAT, Z_TOP), (X_MAX, 0, Z_TOP)])

# --- Roller face y = 0, restrain DY ('0100000') --- 
roller_y_cs1 = set()
roller_y_cs1.update(Model.Select.Polygon([(0, 0, 0), (X_MAX, 0, 0), (X_MAX, 0, z1), (0, 0, z1)]))
roller_y_cs1.update(Model.Select.Polygon([(x0, 0, z1), (X_MAX, 0, z1), (X_MAX, 0, z2), (x0, 0, z2)]))
roller_y_cs2 = Model.Select.Polygon([(x0, 0, z2), (X_MAX, 0, z2), (X_MAX, 0, Z_TOP), (x0, 0, Z_TOP)])

# --- Shared edge x = X_MAX, y = 0, restrain DX+DY ('1100000') ---  
edge_cs1 = Model.Select.Box((X_MAX, 0, 0), (X_MAX, 0, z2), output="NODE_ID")
edge_cs2 = Model.Select.Box((X_MAX, 0, z2), (X_MAX, 0, Z_TOP), output="NODE_ID")

# --- Pin faces: far boundary + base --- 
pin_nodes = set()
pin_nodes.update(Model.Select.Polygon([(0, 0, 0), (0, Y_MAX, 0), (0, Y_MAX, z1), (0, 0, z1)]))            
pin_nodes.update(Model.Select.Polygon([(0, 0, 0), (X_MAX, 0, 0), (X_MAX, Y_MAX, 0), (0, Y_MAX, 0)]))      
pin_nodes.update(Model.Select.Polygon([(0, Y_MAX, 0), (X_MAX, Y_MAX, 0), (X_MAX, Y_MAX, z1), (0, Y_MAX, z1)]))  

# --- Assign supports ---
Boundary.Support(roller_x_cs1, '1000000', 'CS1')
Boundary.Support(roller_x_cs2, '1000000', 'CS2')
Boundary.Support(roller_y_cs1, '0100000', 'CS1')
Boundary.Support(roller_y_cs2, '0100000', 'CS2')
Boundary.Support(edge_cs1, '1100000', 'CS1')
Boundary.Support(edge_cs2, '1100000', 'CS2')
Boundary.Support(pin_nodes, 'pin', 'CS1')

# --- Material ---

# Material.CONC("Mat Foundation","ASTM(RC)","Grade C4000",spec_heat = 1046.5,heat_conduct=96.278,id = 1)
# Material.USER("Subsoil",1e+04,0.2,0.0018,therm=1e-05,spec_heat = 837.2,heat_conduct=71.162,id = 2)
CreepShrinkage.ACI("Creep/Shrinkage",270,70,3,12,4,0.85,"MOIST","CODE",0.00032,12,40,4)
CompStrength.ACI("Elasticity",270,13.9,0.86)
TDMatLink(1,"Creep/Shrinkage","Elasticity")

# --- Load Case and Self weight ---

Load_Case("CS","Self")
Load.SW("Self","Z",load_group="Self")

# --- Heat of Hydration ---
mat_elems = set(elemsInGroup(["Mat Foundation (Lower Part)","Mat Foundation (Upper Part)"]))


Group.Boundary("CS1-Boundary Surface")

# --- HoH definitions other than convection boundary: unchanged ---
HoH.Ambient_Temperature_Function.Constant("Ambient Temperature", 20)
HoH.Convection.Coefficient_Function.Constant("Convection Coeff", 5.0232)
HoH.PrescribedTemperature(list(pin_nodes), 20, "CS1")   
HoH.HeatSource.Function.Code("Heat Source Function", False, 33.97, 0.605)
HoH.HeatSource.AssignHeatSource(mat_elems, func_name="Heat Source Function")

# --- Convection boundary surfaces ---
X_MAX = n_x * MESH_SIZE
Y_MAX = n_y * MESH_SIZE
Y_MAT = n_y_2 * MESH_SIZE         
Z_TOP = MESH_SIZE_Z * (n_sub_soil + n_mat_foundation_total)


def rect(p1, p2, p3, p4):
    return Model.Select.Polygon([p1, p2, p3, p4])

# (node selection, boundary/stage group)
convection_surfaces = [
    (rect((x0, 0, z2), (X_MAX, 0, z2), (X_MAX, Y_MAT, z2), (x0, Y_MAT, z2)), "CS1-Boundary Surface"),  
    (rect((x0, 0, Z_TOP), (X_MAX, 0, Z_TOP), (X_MAX, Y_MAT, Z_TOP), (x0, Y_MAT, Z_TOP)), "CS2"),       
    (rect((0, 0, z1), (x0, 0, z1), (x0, Y_MAX, z1), (0, Y_MAX, z1)), "CS1"),                           
    (rect((x0, Y_MAT, z1), (X_MAX, Y_MAT, z1), (X_MAX, Y_MAX, z1), (x0, Y_MAX, z1)), "CS1"),           
    (rect((x0, 0, z1), (x0, Y_MAT, z1), (x0, Y_MAT, z2), (x0, 0, z2)), "CS1"),                         
    (rect((x0, 0, z2), (x0, Y_MAT, z2), (x0, Y_MAT, Z_TOP), (x0, 0, Z_TOP)), "CS2"),                   
    (rect((x0, Y_MAT, z1), (X_MAX, Y_MAT, z1), (X_MAX, Y_MAT, z2), (x0, Y_MAT, z2)), "CS1"),           
    (rect((x0, Y_MAT, z2), (X_MAX, Y_MAT, z2), (X_MAX, Y_MAT, Z_TOP), (x0, Y_MAT, Z_TOP)), "CS2"),     
]

for nodes, grp in convection_surfaces:
    HoH.Convection.Boundary.bySelectedNodes(nodes, "Convection Coeff", "Ambient Temperature", grp)

HoH.CS.STAGE("CS1",20,[10,20,30,50,80,120,170],["Subsoil","Mat Foundation (Lower Part)"],["CS1","CS1-Boundary Surface"],act_load=["Self"],act_day=["10"],id=1)
HoH.CS.STAGE("CS2",19,[10,20,30,50,80,120,170,300,400,500,600,750,930],["Mat Foundation (Upper Part)"],["CS2"],["CS1-Boundary Surface"],id=2)

Model.create()