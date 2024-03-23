# pylint: disable=unused-argument

from typing import List

from pylabrobot.liquid_handling.backends.backend import LiquidHandlerBackend
from pylabrobot.resources import Resource
from pylabrobot.liquid_handling.standard import (  Pickup,  PickupTipRack,  Drop,  DropTipRack,  Aspiration,  AspirationPlate,  Dispense,  DispensePlate,  Move)
from pylabrobot.resources.petri_dish import PetriDish, PetriDishHolder

import adUtil

class CncLabBackend(LiquidHandlerBackend):

  def __init__(self, num_channels: int = 8):
    """ Initialize a chatter box backend. """
    super().__init__()
    self._num_channels = num_channels

  async def setup(self):
    await super().setup()
    print("Setting up the robot.", self)


  async def stop(self):
    await super().stop()
    print("Stopping the robot.")

  @property
  def num_channels(self) -> int:
    
    return self._num_channels

  async def assigned_resource_callback(self, resource: Resource):
    print(f"Resource {resource.name} was assigned to the robot.")

  async def unassigned_resource_callback(self, name: str):
    print(f"Resource {name} was unassigned from the robot.")

  async def pick_up_tips(self, ops: List[Pickup], use_channels: List[int], **backend_kwargs):
    print(f"Picking up tips {ops}.")

  async def drop_tips(self, ops: List[Drop], use_channels: List[int], **backend_kwargs):
    print(f"Dropping tips {ops}.")

  async def aspirate(self, ops: List[Aspiration], use_channels: List[int], **backend_kwargs):
    #print(f"Aspirating {ops}.")
    adUtil.printl(ops[0].resource)
    # todo add the volume
    adUtil.appendGCodeAndDropLocations(ops[0])

  async def dispense(self, ops: List[Dispense], use_channels: List[int], **backend_kwargs):
    #print(f"Dispensing {ops}.")
    # if isinstance(ops[0].resource, PetriDish):
    #   print("Found Petri dish in holder")
    #   adUtil.printl(ops[0].resource.parent)
    #   offset_from_center = ops[0].offset - ops[0].resource.center()
    #   print("operation offset op[0].offset",ops[0].offset)
    #   print("offset_from_center.x, offset_from_center.y, self.color",offset_from_center.x, offset_from_center.y)
    #   #self.drops.append((offset_from_center.x, offset_from_center.y, self.color))
    # offset_from_center = ops[0].offset - ops[0].resource.center()
    # self.drops.append((offset_from_center.x, offset_from_center.y, self.color))
    # print(ops[0].offsets[0])
    # print("appended", offset_from_center.x, offset_from_center.y, self.color)
    # resource:Resource=ops[0].resource
    # if(resource.drops==None
    #    resource.drops=list()
    #    drops.append()
    adUtil.appendGCodeAndDropLocations(ops[0])

  async def pick_up_tips96(self, pickup: PickupTipRack, **backend_kwargs):
    print(f"Picking up tips from {pickup.resource.name}.")

  async def drop_tips96(self, drop: DropTipRack, **backend_kwargs):
    print(f"Dropping tips to {drop.resource.name}.")

  async def aspirate96(self, aspiration: AspirationPlate):
    print(f"Aspirating {aspiration.volume} from {aspiration.resource}.")

  async def dispense96(self, dispense: DispensePlate):
    print(f"Dispensing {dispense.volume} to {dispense.resource}.")

  async def move_resource(self, move: Move, **backend_kwargs):
    print(f"Moving {move}.")
