from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.visualizer.visualizer import Visualizer
from pylabrobot.resources.opentrons.deck import OTDeck
from pylabrobot.resources import set_tip_tracking, set_volume_tracking
from pylabrobot.resources.opentrons import opentrons_96_tiprack_20ul
from pylabrobot.resources import ( PLT_CAR_L5AC_A00, Cos_96_DW_1mL, HTF_L)
from pylabrobot.resources.opentrons import corning_96_wellplate_360ul_flat
from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.plate import Plate
from pylabrobot.resources.resource import Resource
from pylabrobot.resources.well import Well

#from opentrons import robot, labware, instruments
from cncLabBackend import CncLabBackend
import inspect
import adUtil, cncLabBackend
import asyncio
import os
from pprint import pprint

backend=CncLabBackend()
lh = LiquidHandler(backend, deck=OTDeck())

async def main():
    print("current execution directory",os.getcwd())   # Create a new file path new_file_path = os.path.join(current_directory, 'new_file.txt')

    await lh.setup()
    await asyncio.sleep(1)
    vis = Visualizer(resource=lh)
    await asyncio.sleep(1)
    await vis.setup()
    await asyncio.sleep(1)

    # backend = AgarSimulatingBackend()
    set_tip_tracking(True), set_volume_tracking(True)
    tipsSlot=4
    tips20 = opentrons_96_tiprack_20ul(name="tip_rack_20")
    lh.deck.assign_child_resource(tips20,tipsSlot) 
    adUtil.printl(lh.deck)
    # #pprint(inspect.getmembers(lh.deck))
    tips20.fill()
    await lh.pick_up_tips(tips20["A5"])

    #source 96wells     #destination 96 wells
    sourceSlot=2 # label not the 0 indexed
    sourceWells:Resource = corning_96_wellplate_360ul_flat(name='source_plate') #https://labware.opentrons.com/corning_96_wellplate_360ul_flat?category=wellPlate
    lh.deck.assign_child_at_slot(sourceWells, slot=sourceSlot)
    adUtil.printl(lh.deck.slots[sourceSlot-1])
    adUtil.printl(sourceWells)

    await lh.aspirate(sourceWells["G7"][0], vols=[100.0])
    await asyncio.sleep(30)

  
    lh.summary()
    adUtil.printGCode()
    await lh.stop()
    await asyncio.sleep(5)

asyncio.run(main())

    # https://docs.pylabrobot.org/installation.html change pip install -e ".[dev]"
    # https://docs.pylabrobot.org/basic.html
    # https://docs.pylabrobot.org/using-the-visualizer.html
    # https://colab.research.google.com/drive/1ljiMtb2jrh7-a-ZpjeO7i92d1sQY8KIP?usp=sharing#scrollTo=0gmcxpe-5Qu9
    # https://github.com/Opentrons/opentrons/blob/8fd8a190467708e5b98fc9a0f85163c757fe8272/api/docs/v1/labware.rst
    # for JIM use the workout https://opentrons.com/resource/using-your-multi-channel-e-pipette/
    # https://docs.opentrons.com/v1/hardware_control.html from Jupiter


#https://colab.research.google.com/drive/1PoEZYIjggdnXQNGiKdnMmrJGTUg9xrPY#scrollTo=1cp3Mp8C4tQt HTGAA Ricks big code

    #my cnc max y160 x=285
