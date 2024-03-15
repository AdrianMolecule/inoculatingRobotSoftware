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
lh = LiquidHandler(backend, deck)

async def main():
    print("current execution directory",os.getcwd())   # Create a new file path new_file_path = os.path.join(current_directory, 'new_file.txt')

    await lh.setup()
    await asyncio.sleep(1)
    vis = Visualizer(resource=lh)
    #await asyncio.sleep(1)
    await vis.setup()
    await asyncio.sleep(1)      

    set_tip_tracking(True), set_volume_tracking(True)
    tipsSlot=4
    tips = opentrons_96_tiprack_1000ul(name="tip_rack_20") #opentrons_96_tiprack_20ul
    tips.fill()
    deck.assign_child_at_slot(tips, tipsSlot)
    #tips.
    adUtil.printl(lh.deck)

    #source 96wells     #destination 96 wells
    sourceSlot=2 # label not the 0 indexed
    sourceWells:Resource = corning_96_wellplate_360ul_flat(name='source_plate') #https://labware.opentrons.com/corning_96_wellplate_360ul_flat?category=wellPlate
    deck.assign_child_at_slot(sourceWells, slot=sourceSlot)
    #liquids:list=[(Liquid.WATER, 10)] #GLYCERIN
    sourceWells.set_well_liquids((Liquid.WATER, 200))
    adUtil.printl(lh.deck.slots[sourceSlot-1])
    adUtil.printl(sourceWells)
    
    # plate = lh.deck.get_resource("source_plate")
    sourceA1:Well = sourceWells["A1"][0]
    adUtil.printl(sourceA1)

    destinationSlot=1
    destinationWells = corning_96_wellplate_360ul_flat(name='destination_plate') #https://labware.opentrons.com/corning_96_wellplate_360ul_flat?category=wellPlate
    deck.assign_child_at_slot(destinationWells, slot=destinationSlot)
    #movement starts
    await lh.pick_up_tips(tips["A1"])

    await lh.aspirate(sourceA1, vols=[100.0])
    await lh.dispense(sourceWells["C1"][0], vols=[100.0])   
    await  lh.discard_tips()
    #await lh.drop_tips(tips["A1"]) will put them back
    await lh.pick_up_tips(tips["A3"])  

    await lh.aspirate(sourceA1, vols=[100.0])
    await lh.dispense(sourceWells["B3"][0], vols=[10.0])    
    await lh.aspirate(sourceWells["H3"][0], vols=[10.0])
    await lh.dispense(sourceWells["H12"][0], vols=[10.0])    
    await asyncio.sleep(3)

    # destinationA5 = destinationWells["A5"][0]
    # adUtil.printl(destinationA5)
    # await lh.dispense(destinationA5, vols=[100.0])    # await lh.return_tips()
    lh.summary()
    adUtil.saveGCode()
    # I can get pylabrobot.machine.Machine and then get all children
    await lh.stop()
    await asyncio.sleep(50)

asyncio.run(main())

    # https://docs.pylabrobot.org/installation.html change pip install -e ".[dev]"
    # https://docs.pylabrobot.org/basic.html
    # https://docs.pylabrobot.org/using-the-visualizer.html
    # https://colab.research.google.com/drive/1ljiMtb2jrh7-a-ZpjeO7i92d1sQY8KIP?usp=sharing#scrollTo=0gmcxpe-5Qu9
    # https://github.com/Opentrons/opentrons/blob/8fd8a190467708e5b98fc9a0f85163c757fe8272/api/docs/v1/labware.rst
    # for JIM use the workout https://opentrons.com/resource/using-your-multi-channel-e-pipette/
    # https://docs.opentrons.com/v1/hardware_control.html from Jupiter


#https://colab.research.google.com/drive/1PoEZYIjggdnXQNGiKdnMmrJGTUg9xrPY#scrollTo=1cp3Mp8C4tQt HTGAA Ricks big code
# London and GenSpace code https://colab.research.google.com/drive/13lk-YYfLgpdBRQvWxMNFkGmr1ZVi5OZ_?usp=sharing#scrollTo=nIXUYCL4hbdn

#https://dafarry.github.io/tkinterbook/widget.htm for registering callbacks with the tkinter UI

    #my cnc max y160 x=285
# SCRIPT_DIR = os.path.dirname(os.path.abspath("C:/a/diy/pythonProjects/pylabrobot/pylabrobot/gui"))
# print("SCRIPT_DIR:",SCRIPT_DIR,sys.path)
# sys.path.append(os.path.dirname(SCRIPT_DIR))