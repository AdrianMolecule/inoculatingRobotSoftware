
from pylabrobot.pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.pylabrobot.liquid_handling.backends import ChatterBoxBackend
from pylabrobot.pylabrobot.visualizer.visualizer import Visualizer
from pylabrobot.pylabrobot.resources.opentrons.deck import OTDeck
from pylabrobot.pylabrobot.resources import set_tip_tracking, set_volume_tracking
from pylabrobot.pylabrobot.resources import (  Cos_96_DW_1mL, HTF_L)

import asyncio

# inspired from 
# https://docs.pylabrobot.org/installation.html
#  pip install -e ".[dev]"
# https://docs.pylabrobot.org/basic.html
# https://docs.pylabrobot.org/using-the-visualizer.html
# https://colab.research.google.com/drive/1ljiMtb2jrh7-a-ZpjeO7i92d1sQY8KIP?usp=sharing#scrollTo=0gmcxpe-5Qu9
lh = LiquidHandler(backend=ChatterBoxBackend(), deck=OTDeck())

async def main():
    await lh.setup() #see https://docs.python.org/3/library/asyncio-task.html
    await asyncio.sleep(1)
    vis = Visualizer(resource=lh)
    await asyncio.sleep(1)
    await vis.setup()
    await asyncio.sleep(1)
   
    tip_rack1 = HTF_L(name='tips_01', with_tips=False)
    lh.deck.assign_child_resource(tip_rack1,1) # adrian changed
    tip_rack1.fill()
    set_tip_tracking(True), set_volume_tracking(True)
    await lh.pick_up_tips(tip_rack1["A1", "B2", "C3", "D4"])
    await lh.drop_tips(tip_rack1["A2", "B2", "C3", "D4"])

    await lh.pick_up_tips(tip_rack1["A1"])
    await lh.return_tips()

asyncio.run(main())


