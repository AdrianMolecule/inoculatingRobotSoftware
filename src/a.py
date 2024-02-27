from pylabrobot.pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.pylabrobot.liquid_handling.backends import ChatterBoxBackend
from pylabrobot.pylabrobot.visualizer.visualizer import Visualizer
from pylabrobot.pylabrobot.resources.opentrons.deck import OTDeck
from pylabrobot.pylabrobot.resources import set_tip_tracking, set_volume_tracking
from pylabrobot.pylabrobot.resources.opentrons import opentrons_96_tiprack_20ul
from pylabrobot.pylabrobot.resources import ( PLT_CAR_L5AC_A00, Cos_96_DW_1mL, HTF_L)
from pylabrobot.pylabrobot.resources.opentrons import corning_96_wellplate_360ul_flat
from pylabrobot.pylabrobot.resources.coordinate import Coordinate
from pylabrobot.pylabrobot.resources.plate import Plate
from pylabrobot.pylabrobot.resources.resource import Resource
from pylabrobot.pylabrobot.resources.well import Well
import inspect
import adUtil
import asyncio
import os
from pprint import pprint

backend=ChatterBoxBackend()
lh = LiquidHandler(backend, deck=OTDeck())

async def main():
    print("current execution directory",os.getcwd())   # Create a new file path new_file_path = os.path.join(current_directory, 'new_file.txt')

    await lh.setup()
    await asyncio.sleep(1)
    vis = Visualizer(resource=lh)
    await asyncio.sleep(1)
    await vis.setup()
    await asyncio.sleep(1)

    # inspired from 
    # https://docs.pylabrobot.org/installation.html change pip install -e ".[dev]"
    # https://docs.pylabrobot.org/basic.html
    # https://docs.pylabrobot.org/using-the-visualizer.html
    # https://colab.research.google.com/drive/1ljiMtb2jrh7-a-ZpjeO7i92d1sQY8KIP?usp=sharing#scrollTo=0gmcxpe-5Qu9
    # backend = AgarSimulatingBackend()
    set_tip_tracking(True), set_volume_tracking(True)

    tips20 = opentrons_96_tiprack_20ul(name="tip_rack_20")
    lh.deck.assign_child_resource(tips20,5) 
    #adUtil.printl(lh.deck)
    # #pprint(inspect.getmembers(lh.deck))
    tips20.fill()

    sourceSlot=2 # label not the 0 indexed
    destinationSlot=5
    await lh.pick_up_tips(tips20["A5"])

    #source 96wells     #destination 96 wells
    sourceWells:Resource = corning_96_wellplate_360ul_flat(name='source_plate') #https://labware.opentrons.com/corning_96_wellplate_360ul_flat?category=wellPlate
    lh.deck.assign_child_at_slot(sourceWells, slot=sourceSlot)
    adUtil.printl(lh.deck.slots[sourceSlot-1])
    adUtil.printl(sourceWells)
    
    # plate = lh.deck.get_resource("source_plate")
    sourceA1:Well = sourceWells["A1"][0]
    adUtil.printl(sourceA1)
    sourceA2:Well = sourceWells["A2"][0]
    adUtil.printl(sourceA2)

    destinationWells = corning_96_wellplate_360ul_flat(name='destination_plate')
    lh.deck.assign_child_at_slot(destinationWells, slot=destinationSlot)

    await lh.aspirate(sourceA1, vols=[100.0])
    await lh.dispense(destinationWells["D1"], vols=[100.0])

    # await lh.return_tips()
    lh.summary()
    adUtil.printGCode()
    await lh.stop()
    #await asyncio.sleep(60)

asyncio.run(main())


