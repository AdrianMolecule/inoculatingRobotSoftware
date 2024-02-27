from pylabrobot.pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.pylabrobot.liquid_handling.backends import ChatterBoxBackend
from pylabrobot.pylabrobot.visualizer.visualizer import Visualizer
from pylabrobot.pylabrobot.resources.opentrons.deck import OTDeck
from pylabrobot.pylabrobot.resources import set_tip_tracking, set_volume_tracking
from pylabrobot.pylabrobot.resources.opentrons import opentrons_96_tiprack_20ul
from pylabrobot.pylabrobot.resources import ( PLT_CAR_L5AC_A00, Cos_96_DW_1mL, HTF_L)
from pylabrobot.pylabrobot.resources.opentrons import opentrons_96_tiprack_300ul
import asyncio


lh = LiquidHandler(backend=ChatterBoxBackend(), deck=OTDeck())

async def main():
    await lh.setup()
    await asyncio.sleep(1)
    vis = Visualizer(resource=lh)
    await asyncio.sleep(1)
    await vis.setup()
    await asyncio.sleep(1)

    # no visual

    # https://docs.pylabrobot.org/installation.html for bringing the pylabrobot code
    #see https://docs.python.org/3/library/asyncio-task.html
    #see https://colab.research.google.com/drive/1PoEZYIjggdnXQNGiKdnMmrJGTUg9xrPY#scrollTo=xTuAYvAb5O76

    # Here, we use an 300ul opentrons tips tip rack in slot 11.

    #backend = AgarSimulatingBackend()
    await lh.setup()
    vis = Visualizer(resource=lh)
    await vis.setup()
    set_tip_tracking(True), set_volume_tracking(True)
    tips20 = opentrons_96_tiprack_20ul(name="tip_rack_20")
    lh.deck.assign_child_at_slot(tips20, slot=2)
    await lh.pick_up_tips(tips20["A1"])
    set_tip_tracking(True), set_volume_tracking(True)


    # tip_car = TIP_CAR_480_A00(name='tip carrier')
    # tip_car[0] = tip_rack1 = HTF_L(name='tips_01', with_tips=False)
    # tip_car[1] = tip_rack2 = HTF_L(name='tips_02', with_tips=False)

    # lh.deck.assign_child_resource(tip_car,1) # adrian changed

    # plt_car = PLT_CAR_L5AC_A00(name='plate carrier')
    # plt_car[0] = plate_1 = Cos_96_DW_1mL(name='plate_01')
    # plt_car[1] = plate_2 = Cos_96_DW_1mL(name='plate_02')
    # plt_car[2] = plate_3 = Cos_96_DW_1mL(name='plate_03')

    # lh.deck.assign_child_resource(plt_car, 6)
    # tip_rack1.fill()

    # tip_rack2.set_tip_state([[True, True, False, False]*3]*8)
    # plate_1_liquids = [[(None, 500)]]*96
    # plate_1.set_well_liquids(plate_1_liquids)
    # set_tip_tracking(True), set_volume_tracking(True)

    # await lh.pick_up_tips(tip_rack1["A1", "B2", "C3", "D4"])
    # await lh.drop_tips(tip_rack1["A1", "B2", "C3", "D4"])

    # await lh.pick_up_tips(tip_rack1["A1"])
    # await lh.aspirate(plate_1["A2"], vols=[300])
    # await lh.dispense(plate_2["A1"], vols=[300])
    # await lh.return_tips()

asyncio.run(main())


