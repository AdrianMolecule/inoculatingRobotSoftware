from pylabrobot.pylabrobot.resources.coordinate import Coordinate
from pylabrobot.pylabrobot.resources.resource import Resource
from pprint import pprint
import inspect


gCode=list()
gCode.append("G90 G21; G90 means absolute")
gCode.append("G00 X0 Y0; go to origin")

def appendGCode(message, resource:Resource):
    coordinate:Coordinate=resource.get_absolute_location()
    gCode.append("G00 X"+str(coordinate.x)+ " "+"Y"+str(coordinate.y)+";"+message)
    

def printGCode():
    for i in range(len(gCode)):
        print(gCode[i])


def printl(resource:Resource):
    #pprint(vars(resource))
    coordinate:Coordinate=resource.get_absolute_location()
    print("Resource name:",resource.name,", absolute location:",resource.get_absolute_location()," , location:",resource.location, "_size_x:",resource._size_x,"_size_y:",resource._size_y)
    print("Add Gcode to absolute move G90 G21;G00 X0 Y0 ; ",resource.get_absolute_location())