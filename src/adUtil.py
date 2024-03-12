from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.resource import Resource
from pprint import pprint
import inspect

Z_PROTECTION=10

gCode=list()
gCode.append("G90 G21; G90 means absolute")
gCode.append("Z20; go higher")
gCode.append("X0 Y0; go to X Y origin")

def appendGCode(operationName, resource:Resource):
    gCode.append("Z"+str(resource.get_size_z()+Z_PROTECTION)+"; "+"lift for move to go to "+resource.name)
    coordinate:Coordinate=resource.get_absolute_location()
    gCode.append("X"+str(coordinate.x)+ " "+"Y"+str(coordinate.y)+" using "+operationName+", "+resource.name)
    gCode.append("Z"+str(coordinate.z)+"; "+operationName+" plunge to tube")
    
def printGCode():
    for i in range(len(gCode)):
        print(gCode[i])

def printl(resource:Resource):
    #pprint(vars(resource))
    coordinate:Coordinate=resource.get_absolute_location()
    print("Resource name:", resource.name,", absolute location:",resource.get_absolute_location()," , location:",resource.location, "_size_x:",resource._size_x,"_size_y:",resource._size_y)
    print("Add Gcode to absolute move G90 G21;G00 X0 Y0 ; ",resource.get_absolute_location())