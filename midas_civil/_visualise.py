# import pyvista as pv
import plotly.graph_objects as go
from ._model import Node,Element,Group,Model,Boundary
from ._node import nodeByID

import numpy as np


def _snapshot():
    MODEL_DATA = {
        "GRID":{},
        "BOUNDING_MARKERS":{},
        "NODE":{},
        "ELEM_LINE":{},
        "ELEM_PLATE":{},
        "ELEM_ID":{},
        "ELINK":{},
        "RIGID_LINK":{},
        "SUPPORT":{},
        "POINT_SPRING":{},   
        "ELEM_NUM" : 0
        }

    Model.getBounds()
    y1 = Model.bounds['Y_min']-1
    y2 = Model.bounds['Y_max']+1
    z1 = Model.bounds['Z_min']-0.001
    z2 = Model.bounds['Z_max']
    x1 = Model.bounds['X_min']-1
    x2 = Model.bounds['X_max']+1



    minDim = min(x2-x1,y2-y1)
    nLineX = int(((x2-x1)/minDim)*10)
    nLineY = int(((y2-y1)/minDim)*10)

    xs = np.linspace(x1, x2, nLineX)
    ys = np.linspace(y1, y2, nLineY)


    x_coords = []
    y_coords = []
    z_coords = []

    # Vertical grid lines
    for x in xs:
        x_coords.extend([x, x, None])
        y_coords.extend([y1, y2, None])
        z_coords.extend([z1, z1, None])

    # Horizontal grid lines
    for y in ys:
        x_coords.extend([x1, x2, None])
        y_coords.extend([y, y, None])
        z_coords.extend([z1, z1, None])

    MODEL_DATA['GRID']["X_COORDS"] = x_coords
    MODEL_DATA['GRID']["Y_COORDS"] = y_coords
    MODEL_DATA['GRID']["Z_COORDS"] = z_coords

#-------------------   MODEL BOUNDING POINTS -----------------------------

    x = [x1,x1,x1,x1,x2,x2,x2,x2]
    y = [y1,y2,y1,y2,y1,y2,y1,y2]
    z = [z1,z1,z2,z2,z1,z1,z2,z2]

    MODEL_DATA['BOUNDING_MARKERS']["X_COORDS"] = x
    MODEL_DATA['BOUNDING_MARKERS']["Y_COORDS"] = y
    MODEL_DATA['BOUNDING_MARKERS']["Z_COORDS"] = z


#-------------------   MODEL LINE ELEMS -----------------------------

    SECT_WISE_LINE_ELEM = {}

    PLATE_ELEM = []

    x_coords = []
    y_coords = []
    z_coords = []

    for elem in Element.elements:
        if elem.TYPE in ('BEAM','TRUSS'):
            x1,y1,z1 = nodeByID(elem.NODE[0]).LOC
            x2,y2,z2 = nodeByID(elem.NODE[1]).LOC
            x_coords = (x1, x2, None)
            y_coords = (y1, y2, None)
            z_coords = (z1, z2, None)
            if elem.SECT not in SECT_WISE_LINE_ELEM: 
                SECT_WISE_LINE_ELEM[elem.SECT] = {"X":[],"Y":[],"Z":[]}
                SECT_WISE_LINE_ELEM[elem.SECT]["COL"] = 'red'
            SECT_WISE_LINE_ELEM[elem.SECT]["X"].extend(x_coords)
            SECT_WISE_LINE_ELEM[elem.SECT]["Y"].extend(y_coords)
            SECT_WISE_LINE_ELEM[elem.SECT]["Z"].extend(z_coords)
        elif elem.TYPE in ('PLATE','WALL'):
            l1 = nodeByID(elem.NODE[0]).LOC
            l2 = nodeByID(elem.NODE[1]).LOC
            l3 = nodeByID(elem.NODE[2]).LOC
            if len(elem.NODE) > 3:
                l4 = nodeByID(elem.NODE[3]).LOC
                PLATE_ELEM.append([l3,l4,l1])
            PLATE_ELEM.append([l1,l2,l3])


    MODEL_DATA['ELEM_LINE'] = SECT_WISE_LINE_ELEM
    MODEL_DATA['ELEM_PLATE'] = PLATE_ELEM
    MODEL_DATA['ELEM_NUM'] = len(Element.elements)


#-------------------   NODE POINTS -----------------------------

    x = []
    y = []
    z = []
    id = []

    for cons in Node.nodes:
        x.append(cons.X)
        y.append(cons.Y)
        z.append(cons.Z)
        id.append(cons.ID)
    

    MODEL_DATA['NODE']['X'] = x
    MODEL_DATA['NODE']['Y'] = y
    MODEL_DATA['NODE']['Z'] = z
    MODEL_DATA['NODE']['ID'] = id




#-------------------   ELEMENT ID LABELS -----------------------------

    elem_x = []
    elem_y = []
    elem_z = []
    elem_ids = []

    for elem in Element.elements:
        if elem.TYPE in ['BEAM', 'TRUSS', 'PLATE', 'WALL']:
            x, y, z = elem.CENTER
            elem_x.append(x)
            elem_y.append(y)
            elem_z.append(z)
            elem_ids.append(str(elem.ID))

    MODEL_DATA['ELEM_ID']['X'] = elem_x
    MODEL_DATA['ELEM_ID']['Y'] = elem_y
    MODEL_DATA['ELEM_ID']['Z'] = elem_z
    MODEL_DATA['ELEM_ID']['ID'] = elem_ids

#-------------------   POINT SUPPORTS ELEMS -----------------------------

    x = []
    y = []
    z = []

    for cons in Boundary.Support.sups:
        loc = nodeByID(cons.NODE).LOC
        x.append(loc[0])
        y.append(loc[1])
        z.append(loc[2])

    MODEL_DATA['SUPPORT']['X'] = x
    MODEL_DATA['SUPPORT']['Y'] = y
    MODEL_DATA['SUPPORT']['Z'] = z




    x = []
    y = []
    z = []

    for cons in Boundary.PointSpring.springs:
        loc = nodeByID(cons.NODE).LOC
        x.append(loc[0])
        y.append(loc[1])
        z.append(loc[2])

    MODEL_DATA['POINT_SPRING']['X'] = x
    MODEL_DATA['POINT_SPRING']['Y'] = y
    MODEL_DATA['POINT_SPRING']['Z'] = z



#-------------------   LINKS LINE -----------------------------

    x = []
    y = []
    z = []

    for link in Boundary.ElasticLink.links:
        loc1 = nodeByID(link.I_NODE).LOC
        loc2 = nodeByID(link.J_NODE).LOC

        x.extend((loc1[0],loc2[0],None))
        y.extend((loc1[1],loc2[1],None))
        z.extend((loc1[2],loc2[2],None))

    MODEL_DATA['ELINK']['X'] = x
    MODEL_DATA['ELINK']['Y'] = y
    MODEL_DATA['ELINK']['Z'] = z



    x = []
    y = []
    z = []

    for link in Boundary.RigidLink.links:

        loc1 = nodeByID(link.M_NODE).LOC
        for nID in link.S_NODE:
            loc2 = nodeByID(nID).LOC
            x.extend((loc1[0],loc2[0],None))
            y.extend((loc1[1],loc2[1],None))
            z.extend((loc1[2],loc2[2],None))

    MODEL_DATA['RIGID_LINK']['X'] = x
    MODEL_DATA['RIGID_LINK']['Y'] = y
    MODEL_DATA['RIGID_LINK']['Z'] = z


    return MODEL_DATA

def _visualise(MODEL_DATA,bGrid=True,bNode=False,bNodeID=False,bElementID=False,bSupport=True,bPointSpring=False,bElink=False, bRigidLink=False,):

    #---------  GRID ------------------
    fig = go.Figure()


    if bGrid:
        x_coords = MODEL_DATA['GRID']["X_COORDS"]
        y_coords = MODEL_DATA['GRID']["Y_COORDS"]
        z_coords = MODEL_DATA['GRID']["Z_COORDS"]

        fig.add_trace(
            go.Scatter3d(
                x=x_coords,
                y=y_coords,
                z=z_coords,
                mode="lines",
                line=dict(color="lightgray", width=2),
                hoverinfo="skip",
                showlegend=False,
            )
        )

#---------------------------------------------------------

#-------------------   MODEL BOUNDING POINTS -----------------------------

    x = MODEL_DATA['BOUNDING_MARKERS']["X_COORDS"]
    y = MODEL_DATA['BOUNDING_MARKERS']["Y_COORDS"]
    z = MODEL_DATA['BOUNDING_MARKERS']["Z_COORDS"]


    fig.add_trace(go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers",
        hoverinfo="skip",
        marker=dict(
            size=0,
            opacity = 0,
            color="blue",
        )
    ))

#-------------------   MODEL LINE ELEMS -----------------------------
    _COL_ID = {
        1: "#0BAEEE",
        2: "#3D5AFF",
        3: "#8344F8",
        4: "#D858FF",
        5: "#3FBE50",
        6: "#CC4848",
    }

    SECT_WISE_LINE_ELEM = MODEL_DATA['ELEM_LINE']

    PLATE_ELEM = MODEL_DATA['ELEM_PLATE']




    for secID in SECT_WISE_LINE_ELEM:
        col = _COL_ID.get(int(secID%7),'red')
        fig.add_trace(
            go.Scatter3d(
                x=SECT_WISE_LINE_ELEM[secID]["X"],
                y=SECT_WISE_LINE_ELEM[secID]["Y"],
                z=SECT_WISE_LINE_ELEM[secID]["Z"],
                mode="lines",
                line=dict(color=col, width=4),
                hoverinfo="skip",
                showlegend=False,
            )
        )

#-------------------   MODEL PLATE ELEMS -----------------------------

    
    x, y, z = [], [], []
    i, j, k = [], [], []

    offset = 0
    for plate in PLATE_ELEM:
        # Add vertices
        for p in plate:
            x.append(p[0])
            y.append(p[1])
            z.append(p[2])

            i.append(offset)
            j.append(offset + 1)
            k.append(offset + 2)

        offset += 3

    fig.add_trace(
        go.Mesh3d(
            x=x,
            y=y,
            z=z,
            i=i,
            j=j,
            k=k,
            color="#A7DEF0",
            opacity=1,
            flatshading=True,
            hoverinfo="skip",
            showlegend=False,
            showscale=False,
        )
    )

    # Triangle edges
    edge_x, edge_y, edge_z = [], [], []

    for n in range(0, len(x), 3):
        # vertices: n, n+1, n+2
        verts = [n, n + 1, n+2]

        for a, b in zip(verts[:-1], verts[1:]):
            edge_x.extend([x[a], x[b], None])
            edge_y.extend([y[a], y[b], None])
            edge_z.extend([z[a], z[b], None])

    fig.add_trace(
        go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode="lines",
            line=dict(
                color="#403685",
                width=1,
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

#-------------------   NODE POINTS -----------------------------
    if bNode:
        x = MODEL_DATA['NODE']['X']
        y = MODEL_DATA['NODE']['Y']
        z = MODEL_DATA['NODE']['Z']


        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="markers",
            hoverinfo="skip",
            marker=dict(
                size=4,
                opacity = 1,
                color="#1296e2",
                symbol="circle"
            )
        ))

#-------------------   NODE ID LABELS -----------------------------
    if bNodeID:
        x_ids = MODEL_DATA['NODE']['X']
        y_ids = MODEL_DATA['NODE']['Y']
        z_ids = MODEL_DATA['NODE']['Z']
        text_ids = MODEL_DATA['NODE']['ID']


        fig.add_trace(go.Scatter3d(
            x=x_ids,
            y=y_ids,
            z=z_ids,
            mode="text",
            text=text_ids,
            textposition="top center", 
            hoverinfo="skip",
            textfont=dict(
                size=12,
                color="#000000"
            ),
            showlegend=False
        ))

#-------------------   ELEMENT ID LABELS -----------------------------
    if bElementID:
        elem_x = MODEL_DATA['ELEM_ID']['X']
        elem_y = MODEL_DATA['ELEM_ID']['Y']
        elem_z = MODEL_DATA['ELEM_ID']['Z']
        elem_ids = MODEL_DATA['ELEM_ID']['ID']

        fig.add_trace(go.Scatter3d(
            x=elem_x,
            y=elem_y,
            z=elem_z,
            mode='text',
            text=elem_ids,
            textposition='middle center',
            name='Element IDs',
            textfont=dict(
                color="#5A7DD7",
                size=12
            ),
            hoverinfo='text'
        ))

#-------------------   POINT SUPPORTS ELEMS -----------------------------
    if bSupport:
        x = MODEL_DATA['SUPPORT']['X']
        y = MODEL_DATA['SUPPORT']['Y']
        z = MODEL_DATA['SUPPORT']['Z']


        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="markers",
            hoverinfo="skip",
            marker=dict(
                size=5,
                opacity = 1,
                color="#87ce03",
                symbol="diamond"
            )
        ))

    if bPointSpring:
        x = MODEL_DATA['POINT_SPRING']['X']
        y = MODEL_DATA['POINT_SPRING']['Y']
        z = MODEL_DATA['POINT_SPRING']['Z']

        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="markers",
            hoverinfo="skip",
            marker=dict(
                size=5,
                opacity = 1,
                color="#e21284",
                symbol="circle"
            )
        ))

#-------------------   LINKS LINE -----------------------------
    if bElink:
        x = MODEL_DATA['ELINK']['X']
        y = MODEL_DATA['ELINK']['Y']
        z = MODEL_DATA['ELINK']['Z']

        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="lines",
            hoverinfo="skip",
            line=dict(color="#ff7272", width=4, dash="longdash"),
            showlegend=False,
        ))

    if bRigidLink:
        x = MODEL_DATA['RIGID_LINK']['X']
        y = MODEL_DATA['RIGID_LINK']['Y']
        z = MODEL_DATA['RIGID_LINK']['Z']

        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="lines",
            hoverinfo="skip",
            line=dict(color="#03e428", width=4, dash="dot"),
            showlegend=False,
        ))
                
    view_height = MODEL_DATA['BOUNDING_MARKERS']["Z_COORDS"][-1]

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        scene=dict(
            aspectmode="data",
            yaxis=dict(visible=False),
            xaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(
                projection=dict(type="orthographic"),   # no perspective foreshortening
                eye=dict(x=-1.5, y=-1.5),
            ),
        ),
    )

    return fig

# def stVisual(bGrid=True,bSupport=True,bPointSpring=False,bElink=False, bRigidLink=False,bNode=False,bNodeID=False,bElementID=False):

#     #---------  GRID ------------------
#     fig = go.Figure()

#     Model.getBounds()
#     y1 = Model.bounds['Y_min']-1
#     y2 = Model.bounds['Y_max']+1
#     z1 = Model.bounds['Z_min']-0.001
#     z2 = Model.bounds['Z_max']
#     x1 = Model.bounds['X_min']-1
#     x2 = Model.bounds['X_max']+1

#     if bGrid:
#         minDim = min(x2-x1,y2-y1)
#         nLineX = int(((x2-x1)/minDim)*10)
#         nLineY = int(((y2-y1)/minDim)*10)

#         xs = np.linspace(x1, x2, nLineX)
#         ys = np.linspace(y1, y2, nLineY)


#         x_coords = []
#         y_coords = []
#         z_coords = []

#         # Vertical grid lines
#         for x in xs:
#             x_coords.extend([x, x, None])
#             y_coords.extend([y1, y2, None])
#             z_coords.extend([z1, z1, None])

#         # Horizontal grid lines
#         for y in ys:
#             x_coords.extend([x1, x2, None])
#             y_coords.extend([y, y, None])
#             z_coords.extend([z1, z1, None])

#         fig.add_trace(
#             go.Scatter3d(
#                 x=x_coords,
#                 y=y_coords,
#                 z=z_coords,
#                 mode="lines",
#                 line=dict(color="lightgray", width=2),
#                 hoverinfo="skip",
#                 showlegend=False,
#             )
#         )

# #---------------------------------------------------------

# #-------------------   MODEL BOUNDING POINTS -----------------------------

#     x = [x1,x1,x1,x1,x2,x2,x2,x2]
#     y = [y1,y2,y1,y2,y1,y2,y1,y2]
#     z = [z1,z1,z2,z2,z1,z1,z2,z2]

#     fig.add_trace(go.Scatter3d(
#         x=x,
#         y=y,
#         z=z,
#         mode="markers",
#         hoverinfo="skip",
#         marker=dict(
#             size=0,
#             opacity = 0,
#             color="blue",
#         )
#     ))

# #-------------------   MODEL LINE ELEMS -----------------------------
#     _COL_ID = {
#         1: "#0BAEEE",
#         2: "#3D5AFF",
#         3: "#8344F8",
#         4: "#D858FF",
#         5: "#3FBE50",
#         6: "#CC4848",
#     }

#     SECT_WISE_LINE_ELEM = {}

#     PLATE_ELEM = []

#     x_coords = []
#     y_coords = []
#     z_coords = []

#     for elem in Element.elements:
#         if elem.TYPE in ('BEAM','TRUSS'):
#             x1,y1,z1 = nodeByID(elem.NODE[0]).LOC
#             x2,y2,z2 = nodeByID(elem.NODE[1]).LOC
#             x_coords = (x1, x2, None)
#             y_coords = (y1, y2, None)
#             z_coords = (z1, z2, None)
#             if elem.SECT not in SECT_WISE_LINE_ELEM: 
#                 SECT_WISE_LINE_ELEM[elem.SECT] = {"X":[],"Y":[],"Z":[]}
#                 SECT_WISE_LINE_ELEM[elem.SECT]["COL"] = 'red'
#             SECT_WISE_LINE_ELEM[elem.SECT]["X"].extend(x_coords)
#             SECT_WISE_LINE_ELEM[elem.SECT]["Y"].extend(y_coords)
#             SECT_WISE_LINE_ELEM[elem.SECT]["Z"].extend(z_coords)
#         elif elem.TYPE in ('PLATE','WALL'):
#             l1 = nodeByID(elem.NODE[0]).LOC
#             l2 = nodeByID(elem.NODE[1]).LOC
#             l3 = nodeByID(elem.NODE[2]).LOC
#             if len(elem.NODE) > 3:
#                 l4 = nodeByID(elem.NODE[3]).LOC
#                 PLATE_ELEM.append([l1,l3,l4])
#             PLATE_ELEM.append([l1,l2,l3])



#     for secID in SECT_WISE_LINE_ELEM:
#         col = _COL_ID.get(int(secID%7),'red')
#         fig.add_trace(
#             go.Scatter3d(
#                 x=SECT_WISE_LINE_ELEM[secID]["X"],
#                 y=SECT_WISE_LINE_ELEM[secID]["Y"],
#                 z=SECT_WISE_LINE_ELEM[secID]["Z"],
#                 mode="lines",
#                 line=dict(color=col, width=4),
#                 hoverinfo="skip",
#                 showlegend=False,
#             )
#         )

# #-------------------   MODEL PLATE ELEMS -----------------------------

    
#     x, y, z = [], [], []
#     i, j, k = [], [], []

#     offset = 0
#     for plate in PLATE_ELEM:
#         # Add vertices
#         for p in plate:
#             x.append(p[0])
#             y.append(p[1])
#             z.append(p[2])

#             i.append(offset)
#             j.append(offset + 1)
#             k.append(offset + 2)

#         offset += 3

#     fig.add_trace(
#         go.Mesh3d(
#             x=x,
#             y=y,
#             z=z,
#             i=i,
#             j=j,
#             k=k,
#             colorscale=[[0, "#7758FF"],
#                     [1, "#AF2EFA"]],
#             intensity = np.linspace(0, 1, len(x), endpoint=True),
#             opacity=1,
#             flatshading=True,
#             hoverinfo="skip",
#             showlegend=False,
#             showscale=False,
#         )
#     )

# #-------------------   NODE POINTS -----------------------------
#     if bNode:
#         x = []
#         y = []
#         z = []

#         for cons in Node.nodes:
#             loc = cons.LOC
#             x.append(loc[0])
#             y.append(loc[1])
#             z.append(loc[2])

#         fig.add_trace(go.Scatter3d(
#             x=x,
#             y=y,
#             z=z,
#             mode="markers",
#             hoverinfo="skip",
#             marker=dict(
#                 size=5,
#                 opacity = 1,
#                 color="#1296e2",
#                 symbol="circle"
#             )
#         ))

# #-------------------   NODE ID LABELS -----------------------------
#     if bNodeID:
#         x_ids = []
#         y_ids = []
#         z_ids = []
#         text_ids = []

#         for cons in Node.nodes:
#             loc = cons.LOC
#             x_ids.append(loc[0])
#             y_ids.append(loc[1])
#             z_ids.append(loc[2])
#             text_ids.append(str(cons.ID))

#         fig.add_trace(go.Scatter3d(
#             x=x_ids,
#             y=y_ids,
#             z=z_ids,
#             mode="text",
#             text=text_ids,
#             textposition="top center", 
#             hoverinfo="skip",
#             textfont=dict(
#                 size=12,
#                 color="#000000"
#             ),
#             showlegend=False
#         ))

# #-------------------   ELEMENT ID LABELS -----------------------------
#     if bElementID:
#         elem_x = []
#         elem_y = []
#         elem_z = []
#         elem_ids = []

#         for elem in Element.elements:
#             if elem.TYPE in ['BEAM', 'TRUSS', 'PLATE', 'WALL']:
#                 x, y, z = elem.CENTER
#                 elem_x.append(x)
#                 elem_y.append(y)
#                 elem_z.append(z)
#                 elem_ids.append(str(elem.ID))

#         fig.add_trace(go.Scatter3d(
#             x=elem_x,
#             y=elem_y,
#             z=elem_z,
#             mode='text',
#             text=elem_ids,
#             textposition='middle center',
#             name='Element IDs',
#             textfont=dict(
#                 color="#5A7DD7",
#                 size=12
#             ),
#             hoverinfo='text'
#         ))

# #-------------------   POINT SUPPORTS ELEMS -----------------------------
#     if bSupport:
#         x = []
#         y = []
#         z = []

#         for cons in Boundary.Support.sups:
#             loc = nodeByID(cons.NODE).LOC
#             x.append(loc[0])
#             y.append(loc[1])
#             z.append(loc[2])

#         fig.add_trace(go.Scatter3d(
#             x=x,
#             y=y,
#             z=z,
#             mode="markers",
#             hoverinfo="skip",
#             marker=dict(
#                 size=5,
#                 opacity = 1,
#                 color="#1296e2",
#                 symbol="diamond"
#             )
#         ))

#     if bPointSpring:
#         x = []
#         y = []
#         z = []

#         for cons in Boundary.PointSpring.springs:
#             loc = nodeByID(cons.NODE).LOC
#             x.append(loc[0])
#             y.append(loc[1])
#             z.append(loc[2])

#         fig.add_trace(go.Scatter3d(
#             x=x,
#             y=y,
#             z=z,
#             mode="markers",
#             hoverinfo="skip",
#             marker=dict(
#                 size=5,
#                 opacity = 1,
#                 color="#1296e2",
#                 symbol="circle"
#             )
#         ))

# #-------------------   LINKS LINE -----------------------------
#     if bElink:
#         x = []
#         y = []
#         z = []

#         for link in Boundary.ElasticLink.links:
#             loc1 = nodeByID(link.I_NODE).LOC
#             loc2 = nodeByID(link.J_NODE).LOC

#             x.extend((loc1[0],loc2[0],None))
#             y.extend((loc1[1],loc2[1],None))
#             z.extend((loc1[2],loc2[2],None))

#         fig.add_trace(go.Scatter3d(
#             x=x,
#             y=y,
#             z=z,
#             mode="lines",
#             hoverinfo="skip",
#             line=dict(color="#ff7272", width=4, dash="longdash"),
#             showlegend=False,
#         ))

#     if bRigidLink:
#         x = []
#         y = []
#         z = []

#         for link in Boundary.RigidLink.links:

#             loc1 = nodeByID(link.M_NODE).LOC
#             for nID in link.S_NODE:
#                 loc2 = nodeByID(nID).LOC
#                 x.extend((loc1[0],loc2[0],None))
#                 y.extend((loc1[1],loc2[1],None))
#                 z.extend((loc1[2],loc2[2],None))

#         fig.add_trace(go.Scatter3d(
#             x=x,
#             y=y,
#             z=z,
#             mode="lines",
#             hoverinfo="skip",
#             line=dict(color="#03e428", width=4, dash="dot"),
#             showlegend=False,
#         ))
                

# #--------------   FINAL LAYOUT ----------------

#     # fig.update_layout(
#     #     margin=dict(l=0, r=0, t=0, b=0),
#     #     showlegend=False,
#     #     uirevision="scene",
#     #     scene=dict(
#     #         aspectmode="data",
#     #         yaxis=dict(visible=False),
#     #         xaxis=dict(visible=False),
#     #         zaxis=dict(visible=False),
#     #         camera=dict(
#     #             projection=dict(type="orthographic"),   # no perspective foreshortening
#     #             eye=dict(x=1.6, y=1.6, z=0.9),
#     #         ),
#     #     ),
#     # )

#     fig.update_layout(
#         margin=dict(l=0, r=0, t=0, b=0),
#         showlegend=False,
#         uirevision="constant_viewpoint_key",
#         scene=dict(
#             aspectmode="data",
#             yaxis=dict(visible=False),
#             xaxis=dict(visible=False),
#             zaxis=dict(visible=False),
#             camera=dict(
#                 projection=dict(type="orthographic"),   # no perspective foreshortening
#             ),
#         ),
#     )

#     return fig




#--------------- SNAP FEATURE FOR PLOTLY IMPLEMENTATION ------------------
class Snap:
    snapshots = {}
    n_snap = 0

    def __init__(self,name=None):
        Snap.n_snap+=1

        self.NAME = name
        self.SNAP_DATA = _snapshot()
        self.ID = Snap.n_snap
        
        Snap.snapshots[self.ID] = self

    @staticmethod
    def clear():
        Snap.snapshots = {}
        Snap.n_snap = 0

    @staticmethod
    def get(ID=None):
        maxID = 0
        minID = 0
        try:
            maxID = max(Snap.snapshots.keys())
            minID = min(Snap.snapshots.keys())
        except:
            return
        if ID is None:
            ID = max(minID, min(ID, maxID)) 
        return Snap.snapshots.get(ID,None)
    
    @staticmethod
    def minimumID():
        try:
            minID = min(Snap.snapshots.keys())
            return minID
        except:
            print("⚠️ Error: no snapshots taken")
            return

    @staticmethod
    def maximumID():
        try:
            maxID = max(Snap.snapshots.keys())
            return maxID
        except:
            print("⚠️ Error: no snapshots taken")
            return

    @staticmethod
    def ListIDs():
        return list(Snap.snapshots.keys())
        
