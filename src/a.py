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
from uiBootUp import UiBootUp
#
#from opentrons import robot, labware, instruments
from pylabrobot.liquid_handling.backends import ChatterBoxBackend
from cncLabBackend import CncLabBackend
import inspect
import adUtil, cncLabBackend
import asyncio
import os
from pprint import pprint

backend=CncLabBackend()
#backend=ChatterBoxBackend()
deck:OTDeck=OTDeck()
liquidHandler = LiquidHandler(backend, deck)

tube_z_offset = -50
dish_z_offset = -6
tip_z_offset = -5

def ot_petri_dish_petriHolder(name: str) -> PetriDishHolder:
  plate_width = 127.0
  petriHolder = PetriDishHolder(name=name, size_x=plate_width, size_y=86.0, size_z=14.5)
  diameter = 86.0
  dish = PetriDish(name=f"{name}_dish", diameter=diameter, height=14.5)
  petriHolder.assign_child_resource(dish, location=Coordinate( x=plate_width/2 - diameter/2,  y=0, z=0))
  return petriHolder

async def main():
    print("current execution directory",os.getcwd())   # Create a new file path new_file_path = os.path.join(current_directory, 'new_file.txt')
    await liquidHandler.setup()
    await asyncio.sleep(1)
    # vis = Visualizer(resource=liquidHandler)
    # await asyncio.sleep(1)
    # await vis.setup()
    # await asyncio.sleep(1)    

    set_tip_tracking(True), set_volume_tracking(True)
    tipsSlot=4
    petriSlot=1
    tips = opentrons_96_tiprack_1000ul(name="tip_rack_20") #opentrons_96_tiprack_20ul
    #tips.fill()
    deck.assign_child_at_slot(tips, tipsSlot)
    await liquidHandler.pick_up_tips(tips["A1"])
    return
    sourceSlot=3 # label not the 0 indexed
    sourceWells:Resource = corning_96_wellplate_360ul_flat(name='source_plate') #https://labware.opentrons.com/corning_96_wellplate_360ul_flat?category=wellPlate
    deck.assign_child_at_slot(sourceWells, slot=sourceSlot)
    #liquids:list=[(Liquid.WATER, 10)] #GLYCERIN
    sourceWells.set_well_liquids((Liquid.WATER, 200))
    adUtil.printl(liquidHandler.deck.slots[sourceSlot-1])
    await liquidHandler.aspirate(sourceWells["A1"][0], vols=[100.0])
    #adUtil.printl(sourceWells)

    print("loading petriHolder")
    petriHolder = ot_petri_dish_petriHolder("petri_holder")
    dish = petriHolder.dish
    liquidHandler.deck.assign_child_at_slot(petriHolder, petriSlot)
    for i in range(5):
        await liquidHandler.dispense(dish, vols=[1], offsets=[Coordinate(x=0, y=-5+i*2, z=dish_z_offset)])


    #source 96wells     #destination 96 wells
    sourceSlot=2 # label not the 0 indexed
    sourceWells:Resource = corning_96_wellplate_360ul_flat(name='source_plate') #https://labware.opentrons.com/corning_96_wellplate_360ul_flat?category=wellPlate
    deck.assign_child_at_slot(sourceWells, slot=sourceSlot)
    #liquids:list=[(Liquid.WATER, 10)] #GLYCERIN
    sourceWells.set_well_liquids((Liquid.WATER, 200))
    adUtil.printl(liquidHandler.deck.slots[sourceSlot-1])
    adUtil.printl(sourceWells)
    
    # plate = liquidHandler.deck.get_resource("source_plate")
    sourceA1:Well = sourceWells["A1"][0]
    adUtil.printl(sourceA1)

    destinationSlot=1
    destinationWells = corning_96_wellplate_360ul_flat(name='destination_plate') #https://labware.opentrons.com/corning_96_wellplate_360ul_flat?category=wellPlate
    deck.assign_child_at_slot(destinationWells, slot=destinationSlot)
    #movement starts
    await liquidHandler.pick_up_tips(tips["A1"])

    await liquidHandler.aspirate(sourceA1, vols=[100.0])
    await liquidHandler.dispense(sourceWells["C1"][0], vols=[100.0])   
    await  liquidHandler.discard_tips()
    #await liquidHandler.drop_tips(tips["A1"]) will put them back
    await liquidHandler.pick_up_tips(tips["A3"])  

    await liquidHandler.aspirate(sourceA1, vols=[100.0])
    await liquidHandler.dispense(sourceWells["B3"][0], vols=[10.0])    
    await liquidHandler.aspirate(sourceWells["H3"][0], vols=[10.0])
    await liquidHandler.dispense(sourceWells["H12"][0], vols=[10.0])    
    await asyncio.sleep(3)

    # destinationA5 = destinationWells["A5"][0]
    # adUtil.printl(destinationA5)
    # await liquidHandler.dispense(destinationA5, vols=[100.0])    # await liquidHandler.return_tips()
    liquidHandler.summary()
    adUtil.saveGCode()
    # I can get pylabrobot.machine.Machine and then get all children
    await liquidHandler.stop()
    await asyncio.sleep(50)

asyncio.run(main())
UiBootUp(liquidHandler)

    # https://docs.pylabrobot.org/installation.html change pip install -e ".[dev]"
    # https://docs.pylabrobot.org/basic.html
    # https://docs.pylabrobot.org/using-the-visualizer.html
    # https://colab.research.google.com/drive/1ljiMtb2jrh7-a-ZpjeO7i92d1sQY8KIP?usp=sharing#scrollTo=0gmcxpe-5Qu9
    # https://github.com/Opentrons/opentrons/blob/8fd8a190467708e5b98fc9a0f85163c757fe8272/api/docs/v1/labware.rst
    # for JIM use the workout https://opentrons.com/resource/using-your-multi-channel-e-pipette/
    # https://docs.opentrons.com/v1/hardware_control.html from Jupiter


#https://colab.research.google.com/drive/1PoEZYIjggdnXQNGiKdnMmrJGTUg9xrPY#scrollTo=1cp3Mp8C4tQt HTGAA Ricks big code

    #my cnc max y160 x=285
# SCRIPT_DIR = os.path.dirname(os.path.abspath("C:/a/diy/pythonProjects/pylabrobot/pylabrobot/gui"))
# print("SCRIPT_DIR:",SCRIPT_DIR,sys.path)
# sys.path.append(os.path.dirname(SCRIPT_DIR))