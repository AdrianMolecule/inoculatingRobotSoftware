import sys
import os

from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.visualizer.visualizer import Visualizer
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.resources.opentrons.deck import OTDeck
from pylabrobot.resources import set_tip_tracking, set_volume_tracking
from pylabrobot.resources.opentrons import opentrons_96_tiprack_20ul, opentrons_96_tiprack_1000ul
from pylabrobot.resources import ( PLT_CAR_L5AC_A00, Cos_96_DW_1mL, HTF_L)
from pylabrobot.resources.opentrons import corning_96_wellplate_360ul_flat
from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.plate import Plate
from pylabrobot.resources.resource import Resource
from pylabrobot.resources.liquid import Liquid
from pylabrobot.resources.well import Well
from pylabrobot.resources.tip_rack import TipSpot, TipRack
from pylabrobot.resources.petri_dish import PetriDish, PetriDishHolder
#
from uiBootUp import UiBootUp, UiWindow
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

backend=CncLabBackend()
#backend=ChatterBoxBackend()
deck:OTDeck=OTDeck()
liquidHandler = LiquidHandler(backend, deck)

async def main():
    print("current execution directory",os.getcwd())   # Create a new file path new_file_path = os.path.join(current_directory, 'new_file.txt')
    await liquidHandler.setup()
    await asyncio.sleep(1)
    # vis = Visualizer(resource=liquidHandler)
    # await asyncio.sleep(1)
    # await vis.setup()
    # await asyncio.sleep(1)    

    set_tip_tracking(True)
    #set_volume_tracking(True)
    tipsSlot=4
    petriSlot=1
    sourceSlot=3 # label not the 0 indexed
    destinationSlot=2    
    
    tips = opentrons_96_tiprack_1000ul(name="tip_rack_20") #opentrons_96_tiprack_20ul
    #tips.fill()
    deck.assign_child_at_slot(tips, tipsSlot)
    await liquidHandler.pick_up_tips(tips["A1"])
    sourceWells:Resource = corning_96_wellplate_360ul_flat(name='source_plate') #https://labware.opentrons.com/corning_96_wellplate_360ul_flat?category=wellPlate
    deck.assign_child_at_slot(sourceWells, slot=sourceSlot)
    #liquids:list=[(Liquid.WATER, 10)] #GLYCERIN
    sourceWells.set_well_liquids((Liquid.WATER, 200))
    await liquidHandler.aspirate(sourceWells["A1"][0], vols=[100.0])
    print("loading petriHolder")
    petriHolder = createOtPetriDishPetriHolder("petri_holder")
    dish = petriHolder.dish
    liquidHandler.deck.assign_child_at_slot(petriHolder, petriSlot)
    # for x in range(-40, 41, 40): # 3 dots from -40 to 40 incrementing by 10
    #     print("x",x)
    #    await liquidHandler.dispense(dish, vols=[1], offset=Coordinate(x=x, y=0, z=0))
    await liquidHandler.dispense(dish, vols=[1], offset=Coordinate(x=0, y=0, z=0))
    await liquidHandler.dispense(dish, vols=[1], offset=Coordinate(x=-33, y=0, z=0))
    # for y in range(-40, 40, 10): # 8 dots
    #     await liquidHandler.dispense(dish, vols=[1], offset=Coordinate(x=0, y=y, z=0))
    #liquids:list=[(Liquid.WATER, 10)] #GLYCERIN

    # # plate = liquidHandler.deck.get_resource("source_plate")
    # sourceA1:Well = sourceWells["A1"][0]
    # adUtil.printl(sourceA1)

    # destinationWells = corning_96_wellplate_360ul_flat(name='destination_plate') #https://labware.opentrons.com/corning_96_wellplate_360ul_flat?category=wellPlate
    # deck.assign_child_at_slot(destinationWells, slot=destinationSlot)
    # #movement starts

    # await liquidHandler.aspirate(sourceA1, vols=[100.0])
    # await liquidHandler.dispense(sourceWells["C1"][0], vols=[100.0])   
    # await  liquidHandler.discard_tips()
    # #await liquidHandler.drop_tips(tips["A1"]) will put them back
    # await liquidHandler.pick_up_tips(tips["A3"])  

    # await liquidHandler.aspirate(sourceA1, vols=[100.0])
    # await liquidHandler.dispense(sourceWells["B3"][0], vols=[10.0])    
    # await liquidHandler.aspirate(sourceWells["H3"][0], vols=[10.0])
    # await liquidHandler.dispense(sourceWells["H12"][0], vols=[10.0])    
    # #await asyncio.sleep(3)

    # # destinationA5 = destinationWells["A5"][0]
    # # adUtil.printl(destinationA5)
    # # await liquidHandler.dispense(destinationA5, vols=[100.0])    # await liquidHandler.return_tips()
    # #liquidHandler.summary()
    adUtil.saveGCode()
    # I can get pylabrobot.machine.Machine and then get all children
    await liquidHandler.stop()
    #await asyncio.sleep(3)

asyncio.run(main())
UiBootUp(liquidHandler)


    # https://docs.pylabrobot.org/installation.html change pip install -e ".[dev]"
    # https://docs.pylabrobot.org/basic.html
    # https://docs.pylabrobot.org/using-the-visualizer.html
    # https://colab.research.google.com/drive/1ljiMtb2jrh7-a-ZpjeO7i92d1sQY8KIP?usp=sharing#scrollTo=0gmcxpe-5Qu9
    # https://github.com/Opentrons/opentrons/blob/8fd8a190467708e5b98fc9a0f85163c757fe8272/api/docs/v1/labware.rst
    # for JIM use the workout https://opentrons.com/resource/using-your-multi-channel-e-pipette/
    # https://docs.opentrons.com/v1/hardware_control.html from Jupiter#monkey https://stackoverflow.com/questions/17985216/simpler-way-to-draw-a-circle-with-tkinter


#https://colab.research.google.com/drive/1PoEZYIjggdnXQNGiKdnMmrJGTUg9xrPY#scrollTo=1cp3Mp8C4tQt HTGAA Ricks big code

    #my cnc max y160 x=285
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

# custom_plate = labware.load(custom_plate_name, slot="3")