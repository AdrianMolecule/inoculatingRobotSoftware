import asyncio
import math

from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import OpentronsBackend

from pylabrobot.resources import OTDeck
from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.petri_dish import PetriDish, PetriDishHolder, ot_petri_dish_holder
from pylabrobot.resources.opentrons import (
    opentrons_96_filtertiprack_20ul,
    opentrons_6_tuberack_falcon_50ml_conical
)

def ot_petri_dish_holder(name: str) -> PetriDishHolder:
  plate_width = 127.0
  holder = PetriDishHolder(name=name, size_x=plate_width, size_y=86.0, size_z=14.5)

  diameter = 86.0
  dish = PetriDish(name=f"{name}_dish", diameter=diameter, height=14.5)
  holder.assign_child_resource(dish, location=Coordinate(
    x=plate_width/2 - diameter/2,
    y=0, z=0))

  return holder

async def opentronsTest():

    tube_z_offset = -50
    dish_z_offset = -6
    tip_z_offset = -5
    otBackend = OpentronsBackend(host="192.168.1.134")
    lh = LiquidHandler(backend=otBackend, deck=OTDeck())
    await lh.setup()

    print("loading filtertip rack")
    tips20= opentrons_96_filtertiprack_20ul(name="tip_rack")
    lh.deck.assign_child_at_slot(tips20, slot=8)

    print("loading tuber rack")
    tube_rack = opentrons_6_tuberack_falcon_50ml_conical(name="tube_rack")
    lh.deck.assign_child_at_slot(tube_rack, slot=6)

    print("loading petriholder")
    holder = ot_petri_dish_holder("petri_holder")
    dish = holder.dish
    lh.deck.assign_child_at_slot(holder, slot=2)

    # Add to the code below or delete and start fresh!
    import math

    await lh.pick_up_tips(tips20["A1"], offsets=[Coordinate(z=tip_z_offset)])

    # Vertical line / "nose"
    await lh.aspirate(tube_rack["A1"], vols=[5], use_channels=[0], offsets=[Coordinate(z=tube_z_offset)])
    for i in range(5):
        await lh.dispense(dish, vols=[1], offsets=[Coordinate(x=0, y=-5+i*2, z=dish_z_offset)])

    # left eye
    await lh.aspirate(tube_rack["A1"], vols=[13], use_channels=[0], offsets=[Coordinate(z=tube_z_offset)])
    # center of eye
    await lh.dispense(dish, vols=[1], offsets=[Coordinate(x=-15, y=8, z=dish_z_offset)])
    # circle of eye
    for i in range(12):
        # radius * cos(360/12 * i)
        x = 5 * math.cos(2*math.pi/12 * i)
        y = 5 * math.sin(2*math.pi/12 * i)
        await lh.dispense(dish, vols=[1], offsets=[Coordinate(x=-15+x, y=8+y, z=dish_z_offset)])

    # left eye
    await lh.aspirate(tube_rack["A1"], vols=[13], use_channels=[0], offsets=[Coordinate(z=tube_z_offset)])
    # center of eye
    await lh.dispense(dish, vols=[1], offsets=[Coordinate(x=15, y=8, z=dish_z_offset)])
    # circle of eye
    for i in range(12):

        x = 5 * math.cos(2*math.pi/12 * i)
        y = 5 * math.sin(2*math.pi/12 * i)
        await lh.dispense(dish, vols=[1], offsets=[Coordinate(x=15+x, y=8+y, z=dish_z_offset)])

    # left eye
    await lh.aspirate(tube_rack["A1"], vols=[12], use_channels=[0], offsets=[Coordinate(z=tube_z_offset)])
    # circle of eye
    for i in range(12):
        # radius * cos(360/12 * i)
        x = 27 * math.cos(math.pi/14 * i +math.pi/8)
        y = -27 * math.sin(math.pi/14 * i +math.pi/8)
        await lh.dispense(dish, vols=[1], offsets=[Coordinate(x=0+x, y=y, z=dish_z_offset)])

    await lh.discard_tips()

    await otBackend.home()


    
if __name__ == "__main__":
        
    loop =  asyncio.get_event_loop()
    try:
        loop.run_until_complete(opentronsTest())
    finally:
        loop.close()