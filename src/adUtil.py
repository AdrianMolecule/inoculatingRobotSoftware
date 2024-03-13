from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.resource import Resource
from pprint import pprint
import inspect, os

Z_PROTECTION=10

gCode=list()
gCode.append("G90 G21; G90 means absolute")
gCode.append("Z10; go higher")
gCode.append("X0 Y0; go to X Y origin")

def appendGCode(operationName, resource:Resource):
    gCode.append("Z"+str(resource.get_size_z()+Z_PROTECTION)+"; "+"lift for move to go to "+resource.name)
    coordinate:Coordinate=resource.get_absolute_location()
    gCode.append("X"+str(coordinate.x)+ " "+"Y"+str(coordinate.y)+"; using "+operationName+", "+resource.name)
    gCode.append("Z"+str(coordinate.z)+"; "+operationName+" plunge to tube")
    
def printGCode():
    for i in range(len(gCode)):
        print(gCode[i])

SAVE_FILE_NAME="gcode.txt"
SAVE_FILE_PATH="../"
def saveGCode():
    #file=open(SAVE_file_NAME,"w+")
    file =open(os.path.join(SAVE_FILE_PATH, SAVE_FILE_NAME), 'w+')
    for i in range(len(gCode)):
        file.write(gCode[i]+"\n")
    file.close()
    printGCode()
    print("saved gcode as "+os.path.abspath(file.name))


def printl(resource:Resource):
    #pprint(vars(resource))
    coordinate:Coordinate=resource.get_absolute_location()
    print("Resource name:", resource.name,", absolute location:",resource.get_absolute_location()," , location:",resource.location, "_size_x:",resource._size_x,"_size_y:",resource._size_y)