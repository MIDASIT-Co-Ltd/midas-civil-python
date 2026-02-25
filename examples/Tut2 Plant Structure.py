from midas_civil import *

bay_width = 4
bay_height = 6
bay_length = 4

no_bays = 10

bay_len_div = 3
bay_height_div = 3

gap_truss = 0.75
truss_div = 5
truss_centre_height = 1
#--------------- M A T E R I A L ------------------
Material.STEEL('Frame','ASTM(S)','A36')

#--------------- S E C T I O N ------------------
Section.DB('W16x67','H','AISC','W16x67',id=1)
Section.DB('W14x90','H','AISC','W14x90',id=2)
Section.DB('W18x65','H','AISC','W18x65',id=3)
Section.DB('W4x13','H','AISC','W4x13',id=4)
Section.DB('WT7x24','T','AISC','WT7x24',id=5)
Section.DB('WT4x9','T','AISC','WT4x9',id=6)
Section.DB('L4x4x5/16','L','AISC','L4x4x5/16',id=7)


#--------------- G E O M E T R Y ------------------
for i in range(no_bays+1):
    Element.Beam.SDL([i*bay_length,0,0],[0,0,1],bay_height-gap_truss,sect=1,angle=90)
    Element.Beam.SDL([i*bay_length,0,bay_height-gap_truss],[0,0,1],gap_truss,sect=1,angle=90)

    Element.Beam.SDL([i*bay_length,2*bay_width,0],[0,0,1],bay_height,bay_height_div,sect=1,angle=90)
    Element.Beam.SDL([i*bay_length,0,bay_height],[0,1,0],bay_width,truss_div,sect=5,group='HorzPTrussL')
    Element.Beam.SDL([i*bay_length,2*bay_width,bay_height],[0,-1,0],bay_width,truss_div,sect=5,group='HorzPTrussR')
    Element.Beam.SE([i*bay_length,0,bay_height],[i*bay_length,bay_width,bay_height+truss_centre_height],truss_div,group='InclinePTrussL',sect=5)
    Element.Beam.SE([i*bay_length,2*bay_width,bay_height],[i*bay_length,bay_width,bay_height+truss_centre_height],truss_div,group='InclinePTrussR',sect=5)
    Element.Truss.SE([i*bay_length,bay_width,bay_height],[i*bay_length,bay_width,bay_height+truss_centre_height],sect=6)


for i in range(no_bays+1):
    if i in [0,no_bays]:
        Element.Beam.SDL([i*bay_length,bay_width,0],[0,0,1],bay_height,bay_height_div,sect=2,angle=90)

        Element.Truss.SE([i*bay_length,0,bay_height],[i*bay_length,bay_width,0],sect=7)
        Element.Truss.SE([i*bay_length,0,0],[i*bay_length,bay_width,bay_height],sect=7)
    else:
        Element.Beam.SDL([i*bay_length,bay_width,0],[0,0,1],(bay_height_div-1)*bay_height/bay_height_div,bay_height_div-1,sect=2,angle=90)

HorzPTrussLNodeIDs = nodesInGroup('HorzPTrussL')
HorzPTrussRNodeIDs = nodesInGroup('HorzPTrussR')

InclinePTrussLNodeIDs = nodesInGroup('InclinePTrussL')
InclinePTrussRNodeIDs = nodesInGroup('InclinePTrussR')

for i in range(no_bays+1):
    for j in range(truss_div-1):
        Element.Truss(InclinePTrussLNodeIDs[1+j+i*(truss_div+1)],HorzPTrussLNodeIDs[1+j+i*(truss_div+1)],sect=6)
        Element.Truss(InclinePTrussRNodeIDs[1+j+i*(truss_div+1)],HorzPTrussRNodeIDs[1+j+i*(truss_div+1)],sect=6)
        Element.Truss(InclinePTrussLNodeIDs[1+j+i*(truss_div+1)],HorzPTrussLNodeIDs[2+j+i*(truss_div+1)],sect=6)
        Element.Truss(InclinePTrussRNodeIDs[1+j+i*(truss_div+1)],HorzPTrussRNodeIDs[2+j+i*(truss_div+1)],sect=6)

for i in range(no_bays):
    Element.Beam.SDL([i*bay_length,bay_width,bay_height+truss_centre_height],[1,0,0],bay_length,sect=1)
    # Side TRUSS
    Element.Beam.SDL([i*bay_length,0,bay_height],[1,0,0],bay_length,truss_div,group='TopSideTruss',sect=4)
    Element.Beam.SDL([i*bay_length,0,bay_height-gap_truss],[1,0,0],0.5*bay_length/truss_div,group='BotSideTruss',sect=4)
    Element.Beam.SDL(Element.lastLoc,[1,0,0],bay_length-bay_length/truss_div,truss_div-1,group='BotSideTruss',sect=4)
    Element.Beam.SDL(Element.lastLoc,[1,0,0],0.5*bay_length/truss_div,group='BotSideTruss',sect=4)

    #BRACING
    if i in [0,no_bays-1]:
        Element.Truss.SE([i*bay_length,2*bay_width,bay_height],[(i+1)*bay_length,2*bay_width,0],sect=7)
        Element.Truss.SE([(i+1)*bay_length,2*bay_width,bay_height],[i*bay_length,2*bay_width,0],sect=7)
        Element.Truss.SE([(i)*bay_length,0,bay_height],[(i+1)*bay_length,bay_width,bay_height+truss_centre_height],sect=7)
        Element.Truss.SE([(i+1)*bay_length,0,bay_height],[(i)*bay_length,bay_width,bay_height+truss_centre_height],sect=7)
        Element.Truss.SE([(i)*bay_length,2*bay_width,bay_height],[(i+1)*bay_length,bay_width,bay_height+truss_centre_height],sect=7)
        Element.Truss.SE([(i+1)*bay_length,2*bay_width,bay_height],[(i)*bay_length,bay_width,bay_height+truss_centre_height],sect=7)

    Element.Beam.SDL([i*bay_length,2*bay_width,bay_height],[1,0,0],bay_length,sect=1)

    for j in range(bay_height_div-1):
        Element.Beam.SDL([i*bay_length,2*bay_width,(j+1)*bay_height/bay_height_div],[1,0,0],bay_length,3,group='MezOuter',sect=3)
        Element.Beam.SDL([i*bay_length,bay_width,(j+1)*bay_height/bay_height_div],[1,0,0],bay_length,3,group='MezInner',sect=3)


TopSideTrussNodeIDs = nodesInGroup('TopSideTruss')
BotSideTrussNodeIDs = nodesInGroup('BotSideTruss')
MezOuterNodeIDs = nodesInGroup('MezOuter')
MezInnerNodeIDs = nodesInGroup('MezInner')

for i in range(len(MezOuterNodeIDs)):
    Element.Beam(MezOuterNodeIDs[i],MezInnerNodeIDs[i],sect=3)

for i in range(no_bays):
    for j in range(truss_div):
        Element.Truss(TopSideTrussNodeIDs[j+i*(truss_div)],BotSideTrussNodeIDs[1+j+i*(truss_div+1)],sect=6)
        Element.Truss(TopSideTrussNodeIDs[1+j+i*(truss_div)],BotSideTrussNodeIDs[1+j+i*(truss_div+1)],sect=6)


#--------------- S U P P O R T ------------------

bottomNodeIDs = Model.Select.Box([0,0,0],[no_bays*bay_length,2*bay_width,0])
Boundary.Support(bottomNodeIDs,'fix')

#--------------- L O A D I N G ------------------

Load.SW('Self Weight')

topElementIDs = Model.Select.Box([0,0,bay_height],[no_bays*bay_length,bay_width,bay_height],'ELEM_ID')
Load.Beam(topElementIDs,'Floor Load','',direction='GZ',D=[0,0.25,0.75,1],P=[0,-3,-3,0])

fronNodeIDs = Model.Select.Box([0,0,bay_height],[0,bay_width,bay_height])
Load.Nodal(fronNodeIDs,'Wind Load X','',FX = 60)

SideElementIDs = Model.Select.Box([0,0,bay_height],[no_bays*bay_length,0,0],'ELEM_ID')
Load.Beam(SideElementIDs,'Wind Load Y','',10,'GY')



#--------------- D A T A   T O   C I V I L   N X ------------------

Model.create()