from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.resource import Resource
from pprint import pprint
from pylabrobot.resources.petri_dish import PetriDish, PetriDishHolder
from pylabrobot.liquid_handling.standard import (  Pickup,  PickupTipRack,  Drop,  DropTipRack,  Aspiration,  AspirationPlate,  Dispense,  DispensePlate,  Move)
#
from uiBootup import UiBootup, UiWindow
from tkinter import filedialog, messagebox
import inspect, os
import asyncio


Z_MAX=42 # good for 18x40 CNC change here for other machines
Z_CLEAR=Z_MAX
Z_LABWARE_MAX=30

def configureZ(zClear):
    global Z_MAX
    global Z_CLEAR
    if zClear!=None:
        Z_CLEAR=zClear

gCode=list()
gCode.append("G90 G21; G90 means absolute")
gCode.append("Z"+str(Z_CLEAR)+"; initial lift to safelevel")
gCode.append("X0 Y0; go to X Y origin")

def appendGCodeAndDropLocations(operation):
    operationType=str(type(operation).__name__)
    resource:Resource=operation.resource
    #gCode.append("Z"+str(resource.get_size_z()+Z_PROTECTION)+"; "+"Z Protection lift for move to "+resource.name)
    gCode.append("Z"+str(Z_CLEAR)+"; "+"Z Z_CLEAR lift for move to "+resource.name)
    absLocation=resource.get_absolute_location()
    resourceRoundedAbsoluteCoords:Coordinate=roundedCoords(absLocation)
    operationRoundedOffsetCoords:Coordinate=roundedCoords(operation.offset)
    roundedFinalCoords:Coordinate=roundedCoords(Coordinate(absLocation.x+operation.offset.x, absLocation.y+operation.offset.y, absLocation.z+operation.offset.z))
    # .offset is a relative offset to the center to an absolute value from the left corner of the object so we need to add resource.
    if isinstance(operation, Dispense) and isinstance(resource,PetriDish) : #offset is changed to middle +sent offset TODO check forjust one offfsets
            if( operation.offset==None or operation.offset.z==0):
                raise "PetriDish operations have to have an offset and the z should be >0"
            else: #todo add the size of drops
                gCode.append("X"+str(roundedFinalCoords.x)+" Y"+str(roundedFinalCoords.y)+"; "+operationType+"; go to "+resource.name+" labware abs coords:"+roundedCoordsAsString(operation.offset)+
                            " and an offset:"+roundedCoordsAsString(operation.offset))
                if not hasattr(resource,"drops"):
                    resource.drops=list()
                tou=operationRoundedOffsetCoords.x,operationRoundedOffsetCoords.y
                resource.drops.append(tou)
                gCode.append("Z"+str(operation.offset.z)+"; "+operationType+", plunge to Agar")
    else:
        gCode.append("X"+str(resourceRoundedAbsoluteCoords.x)+ " Y"+str(resourceRoundedAbsoluteCoords.y)+"; "+operationType+"; go to "+resource.name)
        clearanceFromWellBottom=1
        gCode.append("Z"+str(resourceRoundedAbsoluteCoords.z+clearanceFromWellBottom)+"; "+operationType+", plunge to "+resource.name+" at "+str(clearanceFromWellBottom)+" mm above bottom")


def roundedCoords(rawCoordinate:Coordinate)->Coordinate:
    return Coordinate(round(rawCoordinate.x,2),round(rawCoordinate.y,2), round(rawCoordinate.z,2))

def roundedCoordsAsString(rawCoordinate:Coordinate)->str:
    return str(round(rawCoordinate.x,2))+", "+str(round(rawCoordinate.y,2))+", "+str(round(rawCoordinate.z,2))

def printGCode():
    for i in range(len(gCode)):
        print(gCode[i])

SAVE_FILE_NAME="gcode.txt" #change here if you don't like the file name for the gcode 
def saveGCode(rootPath):
    gCode.append("Z"+str(Z_CLEAR)+"; final lift to safe level")
    print("\n******** GCode********")
    file =open(os.path.join(rootPath, SAVE_FILE_NAME), 'w+')
    for i in range(len(gCode)):
        file.write(gCode[i]+"\n")
    file.close()
    #printGCode()
    messagebox.showinfo(" gcode file saved", f"the gcode was saved as {os.path.abspath(file.name)}")            


def printl(resource:Resource):
    #pprint(vars(resource))
    coordinate:Coordinate=resource.get_absolute_location()
    print("Resource name:", resource.name,", absolute location:",resource.get_absolute_location()," , location:",resource.location, "_size_x:",resource._size_x,"_size_y:",resource._size_y)


def createOtPetriDishPetriHolder(name: str) -> PetriDishHolder: # see maybe better way using Opentron's way commented below 
  # warning all z coordiantes are ignored and replaced with the Calibration Z passed in the main program
  slotSizeX=127.76; slotSizeY=85.48
  # opentrons  xOffset, 21.48, yOffset=.34, slotMidPoint=63.88, 42.4
  petriHolder = PetriDishHolder(name=f"{name}_holder", size_x=slotSizeX, size_y=slotSizeY, size_z=11)
  diameter = 84.8 #change here for a different diam PetriDish
  heightOfBottomFromResourceBase=2.99+petriHolder._size_z # should probably be resource.height-resourceWellDepth but it's overwritten based on calibration z for the plate
  dish = PetriDish(name=f"{name}_dish", diameter=diameter, height=13)
  #lower left corner
  petriHolder.assign_child_resource(dish, location=Coordinate( x=slotSizeX/2 - diameter/2,  y=slotSizeY/2 - diameter/2, z=4))
  return petriHolder

def findLimits(array):
    maxX=0;maxY=0;minX=0;minY=0
    for p in array:
        if p[0]>maxX: maxX= p[0]
        if p[1]>maxY: maxY= p[1]
        if p[0]<minX: minX= p[0]
        if p[1]<minY: minY= p[1]
    return maxX, maxY, minX, minY

async def drawBigPlusSign(liquidHandler,dish, calibrationMediaHeight=0):
    off=38
    await liquidHandler.dispense(dish, vols=[1], offsets=[Coordinate(x=0, y=0, z=calibrationMediaHeight)])
    await liquidHandler.dispense(dish, vols=[1], offsets=[Coordinate(x=-off, y=0, z=calibrationMediaHeight)])
    await liquidHandler.dispense(dish, vols=[1], offsets=[Coordinate(x=off, y=0, z=calibrationMediaHeight)])
    await liquidHandler.dispense(dish, vols=[1], offsets=[Coordinate(x=0, y=-off, z=calibrationMediaHeight)])
    await liquidHandler.dispense(dish, vols=[1], offsets=[Coordinate(x=0, y=off, z=calibrationMediaHeight)])


    
# if plate_name not in labware.list():
#     labware.create(
#         custom_plate_name,  # name of you labware
#         grid=(3, 6),        # number of (columns, rows)
#         spacing=(12, 12),   # distances (mm) between each (column, row)
#         diameter=5,         # diameter (mm) of each well
#         depth=10,           # depth (mm) of each well
#         volume=200)         # volume (µL) of each well

# if plate_name not in labware.list():
#     labware.create(
#         PetriDish,  # name of you labware
#         grid=(1, 1),        # number of (columns, rows)
#         spacing=(100, 100),   # distances (mm) between each (column, row)
#         diameter=84.8,         # diameter (mm) of each well
#         depth=10,           # depth (mm) of each well
#         volume=1000)         # volume (µL) of each well