from pylabrobot.pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.pylabrobot.liquid_handling.backends import ChatterBoxBackend
from pylabrobot.pylabrobot.visualizer.visualizer import Visualizer
from pylabrobot.pylabrobot.resources.opentrons.deck import OTDeck
from pylabrobot.pylabrobot.resources import set_tip_tracking, set_volume_tracking
from pylabrobot.pylabrobot.resources.opentrons import opentrons_96_tiprack_20ul
from pylabrobot.pylabrobot.resources import ( PLT_CAR_L5AC_A00, Cos_96_DW_1mL, HTF_L)
from pylabrobot.pylabrobot.resources.opentrons import corning_96_wellplate_360ul_flat
import asyncio
import os

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
    # https://docs.pylabrobot.org/installation.html
    #  pip install -e ".[dev]"
    # https://docs.pylabrobot.org/basic.html
    # https://docs.pylabrobot.org/using-the-visualizer.html
    # https://colab.research.google.com/drive/1ljiMtb2jrh7-a-ZpjeO7i92d1sQY8KIP?usp=sharing#scrollTo=0gmcxpe-5Qu9
    #backend = AgarSimulatingBackend()
    set_tip_tracking(True), set_volume_tracking(True)

    tips20 = opentrons_96_tiprack_20ul(name="tip_rack_20")
    lh.deck.assign_child_resource(tips20,2) # adrian changed
    tips20.fill()
    await lh.pick_up_tips(tips20["A5"])

    #source 96wells
    #destination 96 wells
    sourceWells = corning_96_wellplate_360ul_flat(name='source_plate')
    lh.deck.assign_child_at_slot(sourceWells, slot=2)
    destinationWells = corning_96_wellplate_360ul_flat(name='destination_plate')
    lh.deck.assign_child_at_slot(destinationWells, slot=5)
    
    # plate = lh.deck.get_resource("source_plate")
    await lh.aspirate(sourceWells["A1"], vols=[100.0])
    await lh.dispense(destinationWells["D1"], vols=[100.0])

    # await lh.return_tips()
    lh.summary()
    await lh.stop()
    #await asyncio.sleep(60)

asyncio.run(main())


