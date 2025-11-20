import pyvista as pv
from midas_civil import Node,Element,Group
import numpy as np

class Visual:
    n_snap = 0  # Goes from 1 to snaps taken
    cur_snap = 0
    visual_info = {}
    plotter = pv.Plotter(window_size=[700,400],title="Sumit's Visualiser TEST")
    
    # plotter.camera.clipping_range = (0.000001, 1e6)
    plotter.set_background("white")
    plotter.enable_parallel_projection()
    plotter.show_axes()
    # plotter.ren_win.SetBorders(0)
    plotter.ren_win.SetPosition(600,100)

    first_launch = True

    min_z = 0
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    
    toggle_NodeIDs = True
    toggle_Beam = True
    toggle_Plate = True
    toggle_GroupNodeIDs = False
    toggle_Grid = False

def take_snapshot():
    Visual.n_snap+=1
    Visual.cur_snap+=1

    points = []
    point_ids = []

    for nd in Node.nodes:
        points.append([nd.X,nd.Y,nd.Z])
        point_ids.append(nd.ID)
    
    point_Group_ids = ["." for _ in point_ids]

    for grup in Group.Structure.Groups:
        if grup.NLIST !=[]:
            idx = 0
            for nID in grup.NLIST:
                n_idx = point_ids.index(nID)
                point_Group_ids[n_idx] = str(idx)
                idx+=1



    lines_point_pair =[]
    lines_id_map = []
    Qplates_point_pair = []
    Qplates_id_map =[]
    Tplates_point_pair = []
    Tplates_id_map = []


    for elm in Element.elements:
        if elm.TYPE in ['BEAM','TRUSS']:
            n1 = point_ids.index(elm.NODE[0])
            n2 = point_ids.index(elm.NODE[1])
            lines_point_pair.append([2,n1,n2])
            lines_id_map.append(elm.ID)

        elif elm.TYPE == 'PLATE':
            n1 = point_ids.index(elm.NODE[0])
            n2 = point_ids.index(elm.NODE[1])
            n3 = point_ids.index(elm.NODE[2])
            if elm._NPOINT == 3 :
                Tplates_point_pair.append([3,n1,n2,n3])
                Tplates_id_map.append(elm.ID)
            elif elm._NPOINT == 4 :
                # print("4 noded element")
                n4 = point_ids.index(elm.NODE[3])
                Qplates_point_pair.append([4,n1,n2,n3,n4])
                Qplates_id_map.append(elm.ID)

    Visual.visual_info[str(Visual.n_snap)] = {
        "POINTS" : points,
        "POINT_IDS" : point_ids,
        "POINT_GROUP_IDS" : point_Group_ids,
        "LINE_POINTS" : lines_point_pair,
        "LINE_IDS" : lines_id_map,
        "TRI_POINTS" : Tplates_point_pair,
        "TRI_IDS" : Tplates_id_map,
        "QUAD_POINTS" : Qplates_point_pair,
        "QUAD_IDS" : Qplates_id_map
    }

    # print("TAKING SNAP SHOT ................")
    # print(Visual.n_snap)
    # print(len(points))
    # print(len(Qplates_id_map))
    # print("---------- D O N E -------------")

def changeDataBack(checked):
        # print("DATA Change....")
        Visual.cur_snap = max(Visual.cur_snap-1,1)
        # print(Visual.cur_snap)
        displayWindow()

def changeDataForw(checked):
        # print("DATA Change....")
        Visual.cur_snap = min(Visual.cur_snap+1,Visual.n_snap)
        # print(Visual.cur_snap)
        displayWindow()

def displayWindow():
    if Visual.first_launch == True:
        take_snapshot()
        dPlotter = showVisual(Visual.plotter)
        Visual.first_launch = False
        
        dPlotter.view_xy()
        dPlotter.show()
    else:
        Visual.plotter.clear_actors()
        dPlotter = showVisual(Visual.plotter)
        dPlotter.render()


def showVisual(plotter):

    if Visual.first_launch:
        min_z = 0
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for nd in Node.nodes:
            min_z = min(min_z,nd.Z)
            min_x = min(min_x,nd.X)
            max_x = max(max_x,nd.X)
            min_y = min(min_y,nd.Y)
            max_y = max(max_y,nd.Y)
        min_z = int(min_z)
        min_x = int(min_x)
        max_x = int(max_x)
        min_y = int(min_y)
        max_y = int(max_y)

        Visual.min_x = min_x
        Visual.max_x = max_x
        Visual.min_y = min_y
        Visual.max_y = max_y
        Visual.min_z = min_z
    else :
        min_x = Visual.min_x
        max_x = Visual.max_x
        min_y = Visual.min_y
        max_y = Visual.max_y
        min_z = Visual.min_z


    points = Visual.visual_info[str(Visual.cur_snap)]["POINTS"]
    point_ids = Visual.visual_info[str(Visual.cur_snap)]["POINT_IDS"]
    point_Group_ids = Visual.visual_info[str(Visual.cur_snap)]["POINT_GROUP_IDS"]

    lines_point_pair =Visual.visual_info[str(Visual.cur_snap)]["LINE_POINTS"]
    lines_id_map = Visual.visual_info[str(Visual.cur_snap)]["LINE_IDS"]

    Tplates_point_pair = Visual.visual_info[str(Visual.cur_snap)]["TRI_POINTS"]
    Tplates_id_map = Visual.visual_info[str(Visual.cur_snap)]["TRI_IDS"]

    Qplates_point_pair = Visual.visual_info[str(Visual.cur_snap)]["QUAD_POINTS"]
    Qplates_id_map =Visual.visual_info[str(Visual.cur_snap)]["QUAD_IDS"]



    if lines_point_pair!=[] and Visual.toggle_Beam:
        msh = pv.PolyData(points , lines=lines_point_pair)
        msh.cell_data["ids"] = lines_id_map
        plotter.add_mesh(msh, scalars="ids", cmap="plasma", line_width=4,show_edges=False,opacity=0.95,show_scalar_bar=False,name="Lines")

    if Qplates_point_pair!=[] and Visual.toggle_Plate:
        Qmesh = pv.PolyData(points, Qplates_point_pair)
        Qmesh.cell_data["ids"] = Qplates_id_map
        plotter.add_mesh(Qmesh, scalars="ids", cmap="rainbow", show_edges=True,opacity=0.8,edge_opacity=0.3,show_scalar_bar=False,name="QPlates")

    if Tplates_point_pair!=[] and Visual.toggle_Plate:
        Tmesh = pv.PolyData(points, Tplates_point_pair)
        Tmesh.cell_data["ids"] = Tplates_id_map
        plotter.add_mesh(Tmesh, scalars="ids", cmap="rainbow", show_edges=True,opacity=0.8,edge_opacity=0.3,show_scalar_bar=False,name="TPlates")






    # SHOW NODE ID ---------------------------------------------------------------------------------------
    if Visual.toggle_NodeIDs and points!=[]:
        plotter.add_point_labels(points, point_ids, 
                                    always_visible=True,shape=None,show_points=True,
                                    fill_shape=False,
                                    point_size=10,point_color="red",
                                    font_size=15, name="LABEL_ID"
                                    )

    
    #----------------------------------------------------------------------------------------------------
    
    #GROUP NODE ID ------------------------------------------------------------------------------------
    if Visual.toggle_GroupNodeIDs and points!=[]:
        plotter.add_point_labels(points, point_Group_ids, 
                                    always_visible=True,shape=None,show_points=True,
                                    fill_shape=False,
                                    point_size=10,point_color="orange",
                                    font_size=17, name="GLABEL_ID"
                                    )

    

   # -----------------------------------------------------------------------------------------------------



    # GRID ----------------------------------------------------------------------------------------------
    x_offset = 0.2*(max_x-min_x)+1
    y_offset = 0.2*(max_y-min_y)+1
    x = np.linspace(min_x-x_offset, max_x+x_offset, 21)
    y = np.linspace(min_y-y_offset, max_y+y_offset, 21)


    lines = []
    z_off = 1

    for xi in x:
        lines.append([[xi, y[0], min_z-z_off], [xi, y[-1], min_z-z_off]])  # vertical lines

    for yi in y:
        lines.append([[x[0], yi, min_z-z_off], [x[-1], yi, min_z-z_off]])  # horizontal lines


    grid_lines = pv.PolyData()
    for line in lines:
        grid_lines += pv.Line(line[0], line[1])

    
    if Visual.toggle_Grid:
        plotter.add_mesh(grid_lines, color='gray', line_width=1,name="Grid",opacity=0.3)


#--------------------------------------------------------------------------------------------------------------


    def toggle_GridLines(checked):
        if checked:
            Visual.toggle_Grid = True
            plotter.add_mesh(grid_lines, color='gray', line_width=1,name="Grid",opacity=0.3)
        else:
            Visual.toggle_Grid = False
            plotter.remove_actor("Grid")
        plotter.render()


    def toggle_GroupNodeID(checked):
        if checked:
            Visual.toggle_GroupNodeIDs = True
            plotter.add_point_labels(points, point_Group_ids, 
                                always_visible=True,shape=None,show_points=True,
                                fill_shape=False,
                                point_size=10,point_color="orange",
                                font_size=17, name="GLABEL_ID"
                                )
        else:
            Visual.toggle_GroupNodeIDs = False
            plotter.remove_actor("GLABEL_ID")        
        
        plotter.render()



    def toggle_Beams(checked):
        if checked:
            Visual.toggle_Beam = True
            if lines_point_pair!=[]: plotter.add_mesh(msh, scalars="ids", cmap="plasma", line_width=4,show_edges=False,opacity=0.95,show_scalar_bar=False,name="Lines")
        else:
            Visual.toggle_Beam = False
            plotter.remove_actor("Lines")
        plotter.render()

    def toggle_Plates(checked):
        if checked:
            Visual.toggle_Plate = True
            if Qplates_point_pair!=[]:plotter.add_mesh(Qmesh, scalars="ids", cmap="rainbow", show_edges=True,opacity=0.8,edge_opacity=0.3,show_scalar_bar=False,name="QPlates")
            if Tplates_point_pair!=[]:plotter.add_mesh(Tmesh, scalars="ids", cmap="rainbow", show_edges=True,opacity=0.8,edge_opacity=0.3,show_scalar_bar=False,name="TPlates")
        else:
            Visual.toggle_Plate = False
            plotter.remove_actor("QPlates")
            plotter.remove_actor("TPlates")
        plotter.render()

    def toggle_nodeID(checked):
        if checked:
            Visual.toggle_NodeIDs = True
            plotter.add_point_labels(points, point_ids, 
                                always_visible=True,shape=None,show_points=True,
                                fill_shape=False,
                                point_size=10,point_color="red",
                                font_size=15, name="LABEL_ID"
                                )
        else:
            Visual.toggle_NodeIDs = False
            plotter.remove_actor("LABEL_ID")

        plotter.render()

    
    cbox_NodeID_pos = (50,10)
    plotter.add_checkbox_button_widget(toggle_nodeID, value=Visual.toggle_NodeIDs, position=cbox_NodeID_pos, size=20)
    plotter.add_text("Node ID", font_size=6, color='black',position=(cbox_NodeID_pos[0]+25,cbox_NodeID_pos[1]+3))

    cbox_GrupNodeID_pos = (150,10)
    plotter.add_checkbox_button_widget(toggle_GroupNodeID, value=Visual.toggle_GroupNodeIDs, position=cbox_GrupNodeID_pos, size=20)
    plotter.add_text("Group Node ID", font_size=6, color='black',position=(cbox_GrupNodeID_pos[0]+25,cbox_GrupNodeID_pos[1]+3))

    cbox_DispBeam_pos = (280,10)
    plotter.add_checkbox_button_widget(toggle_Beams, value=Visual.toggle_Beam, position=cbox_DispBeam_pos, size=20)
    plotter.add_text("Beams", font_size=6, color='black',position=(cbox_DispBeam_pos[0]+25,cbox_DispBeam_pos[1]+3))

    cbox_DispPlate_pos = (370,10)
    plotter.add_checkbox_button_widget(toggle_Plates, value=Visual.toggle_Plate, position=cbox_DispPlate_pos, size=20)
    plotter.add_text("Plates", font_size=6, color='black',position=(cbox_DispPlate_pos[0]+25,cbox_DispPlate_pos[1]+3))

    cbox_GridDispl_pos = (450,10)
    plotter.add_checkbox_button_widget(toggle_GridLines, value=Visual.toggle_Grid, position=cbox_GridDispl_pos, size=20)
    plotter.add_text("Grid", font_size=6, color='black',position=(cbox_GridDispl_pos[0]+25,cbox_GridDispl_pos[1]+3))

    cbox_Animate_pos = (580,10)
    plotter.add_checkbox_button_widget(changeDataBack, value=True, position=cbox_Animate_pos, size=20)
    plotter.add_text("<<", font_size=6, color='red',position=(cbox_Animate_pos[0]+25,cbox_Animate_pos[1]+3))

    cbox_Animate_pos = (640,10)
    plotter.add_checkbox_button_widget(changeDataForw, value=True, position=cbox_Animate_pos, size=20)
    plotter.add_text(">>", font_size=6, color='green',position=(cbox_Animate_pos[0]+25,cbox_Animate_pos[1]+3))

    
    #--------------------------------------------------------------------------------------------------------------


    return plotter
