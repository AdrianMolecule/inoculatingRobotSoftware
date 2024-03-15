from pylabrobot.resources.resource import Resource
class ResourceCoordinates: 

    x0: float = -1
    y0: float = -1
    xSize: float = -1
    ySize: float = -1
    resource:Resource=None
    def __init__(self, x0,y0,xS,yS, resource:Resource):
            self.x0 = x0
            self.y0 = y0
            self.xSize = xS
            self.ySize= yS
            self.resource=resource

    def contains(self, x:float, y:float)->bool: #uses Gcode coordinates not tk coords
        if  x>=self.x0 and x<=self.x0+self.xSize and y>=self.y0 and y<=self.y0+self.ySize:
             return self.resource