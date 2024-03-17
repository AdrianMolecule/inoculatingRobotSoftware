from pylabrobot.resources.coordinate import Coordinate
def p(i):
    print(i.xxx)
l=Coordinate (2,2,3)
if hasattr(l,"xxx"):
    print("has Attribute first")
print(l.x)
l.xxx="AHA"
if hasattr(l,"xxx"):
    print("has Attribute after")
print(l.xxx)
p(l)
