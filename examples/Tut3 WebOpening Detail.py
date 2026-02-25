from midas_civil import *
import math

circle_points = []
radius = 100
n=24
for i in range(n+1):
    theta = 360/n*i*math.pi/180
    circle_points.append((radius*math.cos(theta),0,radius*math.sin(theta)))


Element.Plate.fromPoints([(-500,0,-200)])
Node.create()

Load.Beam()