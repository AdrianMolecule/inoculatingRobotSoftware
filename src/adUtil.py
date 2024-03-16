from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.resource import Resource
from pprint import pprint
from pylabrobot.resources.petri_dish import PetriDish, PetriDishHolder
from pylabrobot.liquid_handling.standard import (  Pickup,  PickupTipRack,  Drop,  DropTipRack,  Aspiration,  AspirationPlate,  Dispense,  DispensePlate,  Move)
#
from uiBootUp import UiBootUp, UiWindow
import inspect, os

Z_PROTECTION=10

gCode=list()
gCode.append("G90 G21; G90 means absolute")
gCode.append("Z10; go higher")
gCode.append("X0 Y0; go to X Y origin")

def appendGCode(operation):
    print("Operation resource", operation.resource, "operation.offset",operation.offset,
          "operation.offset - operation.resource.center()",operation.offset - operation.resource.center(),"resource center", operation.resource.center())
    operationType=str(type(operation).__name__)
    resource:Resource=operation.resource
    gCode.append("Z"+str(resource.get_size_z()+Z_PROTECTION)+"; "+"lift for move to go to "+resource.name)
    coordinate:Coordinate=resource.get_absolute_location()
    if operation.offset!=None: #offset is changed to middle +sent offset
        if(operation.offset.z!=0):
            raise "!!!!!!!!!!!!!!!! offset with Z!=0 is not supported" # NOTE: this is almost equivalent to bare `raise`   
        else:           
             gCode.append("X"+str(round(coordinate.x+operation.offset.x,2))+ " "+"Y"+str(round(coordinate.y+operation.offset.y,2))+"; using "+operationType+", "+resource.name)
    elif operation.offsets!=None: 
        raise "!!!!!!!!!!!!!!!! offsets are not supported"
    else:
        gCode.append("X"+str(round(coordinate.x,2))+ " "+"Y"+str(round(coordinate.y,2))+"; using "+operationType+", "+resource.name)
    gCode.append("Z"+str(coordinate.z)+"; "+operationType+", plunge to tube")
    
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


def createOtPetriDishPetriHolder(name: str) -> PetriDishHolder:
  slotSizeX, slotSizeY=UiWindow.getSlotPocketDimensions()
  petriHolder = PetriDishHolder(name=name, size_x=slotSizeX, size_y=slotSizeY, size_z=14.5)
  diameter = 85.6
  dish = PetriDish(name=f"{name}_dish", diameter=diameter, height=14.5)
  #lower left corner
  petriHolder.assign_child_resource(dish, location=Coordinate( x=slotSizeX/2 - diameter/2,  y=slotSizeY/2 - diameter/2, z=0))
  return petriHolder
