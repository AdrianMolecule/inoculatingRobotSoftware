import os
import sys
import numpy
from pathlib import Path




from pylabrobot.liquid_handling import LiquidHandler
#from pylabrobot.visualizer.visualizer import Visualizer
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.resources.opentrons.deck import OTDeck
from pylabrobot.resources import set_volume_tracking
from pylabrobot.resources.opentrons import corning_96_wellplate_360ul_flat
from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.plate import Plate
from pylabrobot.resources.resource import Resource
from pylabrobot.resources.liquid import Liquid
from pylabrobot.resources.well import Well
from pylabrobot.resources.opentrons import opentrons_96_tiprack_20ul, opentrons_96_tiprack_1000ul
#
from uiBootup import UiBootup, UiWindow
#
#from opentrons import robot, labware, instruments
from pylabrobot.liquid_handling.backends import ChatterBoxBackend
from cncLabBackend import CncLabBackend
import inspect
import adUtil, cncLabBackend
import asyncio
import os
from pprint import pprint
from adUtil import createOtPetriDishPetriHolder
from adUtil import drawBigPlusSign
from adUtil import findLimits
from adUtil import configureZ
from tkinter import filedialog, messagebox

opentronsIp=None
if opentronsIp != None:
    print("using an Opentrons server")
    #backend = OpentronsBackend(host=opentronsIp, port=31950)
else:
    backend=CncLabBackend()
deck:OTDeck=OTDeck(); deck._size_x=437.86;deck._size_y=437.36 # adjusted deck dimensions
liquidHandler = LiquidHandler(backend, deck)

def getInitialPath():
    base=None
    if getattr(sys, 'frozen', False):  # If running from a bundled executable
        print("running from a bundled Exec")
        base= str(Path(sys._MEIPASS))
    else:  # If running from a script
        base=os.getcwd()
    print("basePath",base)
    return base

# all docs at https://github.com/AdrianMolecule/inoculatingRobot  # if you want to clone pylabrobot too read about extraPaths at the end of this file
async def main():
    print("current execution directory",os.getcwd())   # Create a new file path new_file_path = os.path.join(current_directory, 'new_file.txt')
    await liquidHandler.setup()
    configureZ(22)# will set clearance Z for this session.If not it will go the z_max for machine
    #set_volume_tracking(True)
    petriSlot=1
    sourceSlot=4 # labeled style starts at 1 not the 0 indexed
    sourceWell="H7"
    tipsSlot=5 # my fourth one
    tips = opentrons_96_tiprack_1000ul(name="tip_rack_20") ;    deck.assign_child_at_slot(tips, tipsSlot);    await liquidHandler.pick_up_tips(tips["A1"]) #should not be necessary   
    sourceWells:Resource = corning_96_wellplate_360ul_flat(name='source_plate') #https://labware.opentrons.com/corning_96_wellplate_360ul_flat?category=wellPlate
    sourceWells.set_well_liquids((Liquid.WATER, 200))
    deck.assign_child_at_slot(sourceWells, slot=sourceSlot)
    print("loading petriHolder")
    petriHolder = createOtPetriDishPetriHolder("Petri Canvas")
    dish = petriHolder.dish
    liquidHandler.deck.assign_child_at_slot(petriHolder, petriSlot)
    print("calling disperse with offsets")
    calibrationMediaHeight=7.9 #change here and replace with the z of the top of your agar plate calculated as distance from the bed
    #await drawBigPlusSign(liquidHandler,dish,calibrationMediaHeight) # change here if you want to t
    filePath = filedialog.askopenfilename(title="Open Image", initialdir=getInitialPath(), filetypes=[("Dot array file", "*.npy"), ("All Files", "*.*")])  	
    rootPath=os.path.dirname(filePath)
    if filePath:
        try:
            print("loading",filePath)# st with big plus sign
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the file: {e}")
    points=numpy.load(filePath)
    print ("limits for Petri disperse: ",findLimits(points))
    await liquidHandler.aspirate(sourceWells[sourceWell][0], vols=[100.0])#pre-wet, kind of redundant but better be safe
    for point in points:
        print("disperse offset:",point)
        await liquidHandler.aspirate(sourceWells[sourceWell][0], vols=[1.0])        
        await liquidHandler.dispense(dish, vols=[1.0], offsets=[Coordinate(x=point[0], y=point[1], z=calibrationMediaHeight)])
    adUtil.saveGCode(rootPath, originalFileName=os.path.splitext(os.path.basename(filePath))[0])
    await liquidHandler.stop()

asyncio.run(main())

UiBootup(liquidHandler) #all done in the constructor




    # https://docs.pylabrobot.org/installation.html change pip install -e ".[dev]"
    # https://docs.pylabrobot.org/basic.html
    # https://docs.pylabrobot.org/using-the-visualizer.html
    # https://colab.research.google.com/drive/1ljiMtb2jrh7-a-ZpjeO7i92d1sQY8KIP?usp=sharing#scrollTo=0gmcxpe-5Qu9
    # https://github.com/Opentrons/opentrons/blob/8fd8a190467708e5b98fc9a0f85163c757fe8272/api/docs/v1/labware.rst
    # for JIM use the workout https://opentrons.com/resource/using-your-multi-channel-e-pipette/
    # https://docs.opentrons.com/v1/hardware_control.html from Jupiter#monkey https://stackoverflow.com/questions/17985216/simpler-way-to-draw-a-circle-with-tkinter


#https://colab.research.google.com/drive/1PoEZYIjggdnXQNGiKdnMmrJGTUg9xrPY#scrollTo=1cp3Mp8C4tQt HTGAA Rick's big code

#C:\a\diy\pythonProjects\pylabrobot\pylabrobot\server\readme.md has interesting info for running and communication with the web server


# if you want to clone pylabrobot too one way to use it is to change the settings (change 'ad' to your name and allabsolute paths) in C:\Users\ad\AppData\Roaming\Code\User adn add teh extra paths
    # "python.autoComplete.extraPaths": ["C:/a/diy/pythonProjects/pylabrobot"],  
    # "python.analysis.extraPaths": ["C:/a/diy/pythonProjects/pylabrobot/"],
    #This one in WORKSPACE SETTINGS # "terminal.integrated.env.windows": {"PYTHONPATH": "${workspaceFolder};C:/a/diy/pythonProjects/pylabrobot" },
    # warning: for Microsoft the general User setting file is hidden under C:\Users\ad\AppData\Roaming\Code\User\settings.json


    #my cnc max y160 x=285

    # one could also add the path to piRobot programatically like below
    # SCRIPT_DIR = os.path.dirname(os.path.abspath("C:/a/diy/pythonProjects/pylabrobot/pylabrobot/gui"))
    # print("SCRIPT_DIR:",SCRIPT_DIR,sys.path)
    # sys.path.append(os.path.dirname(SCRIPT_DIR))


# custom_plate_name = "custom_18_wellplate_200ul"

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

# custom_plate = labware.load(custom_plate_name, slot="3")