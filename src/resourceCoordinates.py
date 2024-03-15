from pylabrobot.resources.resource import Resource
class ResourceCoordinates: 

    x0: float = 0
    y0: float = 0
    xSize: float = 0
    ySize: float = 0
    resource:Resource=""
    def __init__(self, x0,y0,xS,yS, resource:Resource):
            self.xo = x0
            self.y0 = y0
            self.xSize = xS
            self.ySize= yS
            self.resource=resource

    def contains(self, x:float, y:float)->bool:
        print("checking point ",y, "and my stored dims self.y0:",self.y0)
        if  x>=self.x0 and x<=self.x0+self.xSize and y<=self.y0 and y>=self.y0-self.ySize:
             return self.resource