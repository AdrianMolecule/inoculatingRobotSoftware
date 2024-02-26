from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import ChatterBoxBackend
from pylabrobot.visualizer.visualizer import Visualizer
from pylabrobot.resources.opentrons.deck import OTDeck
from pylabrobot.resources import set_tip_tracking, set_volume_tracking
from pylabrobot.resources import ( PLT_CAR_L5AC_A00, Cos_96_DW_1mL, HTF_L)
import asyncio

lh = LiquidHandler(backend=ChatterBoxBackend(), deck=OTDeck())

async def main():
    await lh.setup()
    await asyncio.sleep(1)
    vis = Visualizer(resource=lh)
    await asyncio.sleep(1)
    await vis.setup()
    await asyncio.sleep(2)
    #see https://docs.python.org/3/library/asyncio-task.html

    set_tip_tracking(True), set_volume_tracking(True)
    tip_rack1 = HTF_L(name='tips_01', with_tips=False)
    tip_rack1.fill()

    lh.deck.assign_child_resource(tip_rack1,1) # adrian changed
    await lh.pick_up_tips(tip_rack1["A1", "B2", "C3", "D4"])
    #await lh.drop_tips(tip_rack1["A1", "B2", "C3", "D4"])

asyncio.run(main())


