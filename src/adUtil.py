from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.resource import Resource
from pprint import pprint
from pylabrobot.resources.petri_dish import PetriDish, PetriDishHolder
from pylabrobot.liquid_handling.standard import (  Pickup,  PickupTipRack,  Drop,  DropTipRack,  Aspiration,  AspirationPlate,  Dispense,  DispensePlate,  Move)
#
from uiBootUp import UiBootUp, UiWindow
import inspect, os


Z_MAX=42
Z_LABWARE_MAX=30
Z_LABWARE_MAX=30

gCode=list()
gCode.append("G90 G21; G90 means absolute")
gCode.append("Z"+str(Z_MAX)+"; go to 20")
gCode.append("X0 Y0; go to X Y origin")

def appendGCodeAndDropLocations(operation):
    operationType=str(type(operation).__name__)
    resource:Resource=operation.resource
    #gCode.append("Z"+str(resource.get_size_z()+Z_PROTECTION)+"; "+"Z Protection lift for move to "+resource.name)
    gCode.append("Z"+str(Z_MAX)+"; "+"Z Z_MAX lift for move to "+resource.name)
    absLocation=resource.get_absolute_location()
    resourceRoundedAbsoluteCoords:Coordinate=roundedCoords(absLocation)
    operationRoundedOffsetCoords:Coordinate=roundedCoords(operation.offset)
    roundedFinalCoords:Coordinate=roundedCoords(Coordinate(absLocation.x+operation.offset.x, absLocation.y+operation.offset.y, absLocation.z+operation.offset.z))
    # .offset is a relative offset to the center to an absolute value from the left corner of the object so we need to add resource.
    if isinstance(operation, Dispense) and isinstance(resource,PetriDish) : #offset is changed to middle +sent offset TODO check forjust one offfsets
            if( operation.offset==None or operation.offset.z==0):
                raise "PetriDish operations have to have an offset and the z should be >0"
            else: #todo add the size of drops
                gCode.append("X"+str(roundedFinalCoords.x)+" Y"+str(roundedFinalCoords.y)+"; "+operationType+" in "+resource.name+" labware abs coords:"+roundedCoordsAsString(operation.offset)+
                            " and an offset:"+roundedCoordsAsString(operation.offset))
                if not hasattr(resource,"drops"):
                    resource.drops=list()
                tou=operationRoundedOffsetCoords.x,operationRoundedOffsetCoords.y
                resource.drops.append(tou)
                gCode.append("Z"+str(operation.offset.z)+"; "+operationType+", plunge to Agar")
    else:
        gCode.append("X"+str(resourceRoundedAbsoluteCoords.x)+ " Y"+str(resourceRoundedAbsoluteCoords.y)+"; "+operationType+" to "+resource.name)
        gCode.append("Z"+str(resourceRoundedAbsoluteCoords.z+1)+"; "+operationType+", plunge to "+resource.name+" at 1 mm above bottom")

def roundedCoords(rawCoordinate:Coordinate)->Coordinate:
    return Coordinate(round(rawCoordinate.x,2),round(rawCoordinate.y,2), round(rawCoordinate.z,2))

def roundedCoordsAsString(rawCoordinate:Coordinate)->str:
    return str(round(rawCoordinate.x,2))+", "+str(round(rawCoordinate.y,2))+", "+str(round(rawCoordinate.z,2))

def printGCode():
    for i in range(len(gCode)):
        print(gCode[i])

SAVE_FILE_NAME="gcode.txt"
SAVE_FILE_PATH="../"
def saveGCode():
    print("\n******** GCode********")
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
  # warning all z coordiantes are ignored and replaced with the Calibration Z passed in the main program
  slotSizeX=127.76; slotSizeY=85.48
  # opentrons  xOffset, 21.48, yOffset=.34, slotMidPoint=63.88, 42.4
  petriHolder = PetriDishHolder(name=f"{name}_holder", size_x=slotSizeX, size_y=slotSizeY, size_z=11)
  diameter = 84.8
  heightOfBottomFromResourceBase=2.99+petriHolder._size_z # should probably be resource.height-resourceWellDepth
  dish = PetriDish(name=f"{name}_dish", diameter=diameter, height=13)
  #lower left corner
  petriHolder.assign_child_resource(dish, location=Coordinate( x=slotSizeX/2 - diameter/2,  y=slotSizeY/2 - diameter/2, z=4))
  return petriHolder
