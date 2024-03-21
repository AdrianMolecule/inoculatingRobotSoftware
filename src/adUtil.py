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
gCode.append("Z20; go to 20")
gCode.append("X0 Y0; go to X Y origin")

def appendGCode(operation):
    operationType=str(type(operation).__name__)
    resource:Resource=operation.resource
    gCode.append("Z"+str(resource.get_size_z()+Z_PROTECTION)+"; "+"lift for move to go to "+resource.name)
    resourceStartCoords:Coordinate=resource.get_absolute_location()
    # .offset is changed fromthe relative offset to the center to an absolute value from the left corner of the object so we need to add resource.
    if isinstance(operation, Dispense) and operation.offset!=None: #offset is changed to middle +sent offset TODO check forjust one offfsets
        if(operation.offset.z!=0):
            raise "!!!!!!!!!!!!!!!! offset with Z!=0 is not supported"   
        else:           #todo add the size of drops
            gCode.append("X"+str(round(resourceStartCoords.x+operation.offset.x,2))+ " "+"Y"+str(round(resourceStartCoords.y+operation.offset.y,2))+"; using "+operationType+" in "+resource.name+
                          " and an offset:"+str(operation.offset)+" so real coords inside labware:"+str(round(resourceStartCoords.x+operation.offset.x,2)))
            if not hasattr(resource,"drops"):
                resource.drops=list()
            tou=(round(resourceStartCoords.x+operation.offset.x,2)), round(resourceStartCoords.y+operation.offset.y,2)
            resource.drops.append(tou)
    else:
        gCode.append("X"+str(round(resourceStartCoords.x,2))+ " "+"Y"+str(round(resourceStartCoords.y,2))+"; using "+operationType+", "+resource.name)
    gCode.append("Z"+str(resourceStartCoords.z-1)+"; "+operationType+", plunge to tube")
    
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
  slotSizeX=127.76; slotSizeY=85.48
  petriHolder = PetriDishHolder(name=f"{name}_holder", size_x=slotSizeX, size_y=slotSizeY, size_z=4)
  diameter = 84.8
  dish = PetriDish(name=f"{name}_dish", diameter=diameter, height=3)
  #lower left corner
  petriHolder.assign_child_resource(dish, location=Coordinate( x=slotSizeX/2 - diameter/2,  y=slotSizeY/2 - diameter/2, z=3))
  return petriHolder
