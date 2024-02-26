from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import ChatterBoxBackend
from pylabrobot.visualizer.visualizer import Visualizer
from pylabrobot.resources.opentrons.deck import OTDeck
import asyncio

lh = LiquidHandler(backend=ChatterBoxBackend(), deck=OTDeck())

async def main():
    await lh.setup()
    await asyncio.sleep(1)
    vis = Visualizer(resource=lh)
    await asyncio.sleep(1)
    await vis.setup()
    await asyncio.sleep(1)


asyncio.run(main())
