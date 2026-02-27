from midas_civil import *

#--------------- C O N N E C T I O N ------------------

MAPI_KEY('xxxxxxxxxxxxxx')
MAPI_BASEURL.autoURL()

#--------------- P A R A M E T E R S ------------------
bay_width = 6
bay_height = 3
bay_length = 4

no_bays = 2

bay_len_div = 2

#--------------- M A T E R I A L ------------------
Material.STEEL('A36','ASTM(S)','A36')

#--------------- S E C T I O N ------------------
Section.DB('W8x35','H','AISC','W8x35',id=1)
Section.DB('W16x67','H','AISC','W16x67',id=2)

#--------------- G E O M E T R Y ------------------
for i in range(no_bays+1):
    Element.Beam.SDL([i*bay_length,0,0],[0,0,1],bay_height,sect=1,angle=90)
    Element.Beam.SDL([i*bay_length,bay_width,0],[0,0,1],bay_height,sect=1,angle=90)
    Element.Beam.SDL([i*bay_length,0,bay_height],[0,1,0],bay_width,sect=2)

for i in range(no_bays):
    Element.Beam.SDL([i*bay_length,0,bay_height],[1,0,0],bay_length,bay_len_div,sect=2)
    Element.Beam.SDL([i*bay_length,bay_width,bay_height],[1,0,0],bay_length,bay_len_div,sect=2)

    for j in range(bay_len_div-1):
        Element.Beam.SDL([i*bay_length+(j+1)*bay_length/bay_len_div,0,bay_height],[0,1,0],bay_width,sect=2)


#--------------- S U P P O R T ------------------

bottomNodeIDs = Model.Select.Box([0,0,0],[no_bays*bay_length,bay_width,0])
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