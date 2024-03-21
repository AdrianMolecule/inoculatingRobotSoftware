from tkinter import *

from tkinter import filedialog
from collections import deque
from tkinter import messagebox
import sys
import os

from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.visualizer.visualizer import Visualizer
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.resources.opentrons.deck import OTDeck
from pylabrobot.resources import set_tip_tracking, set_volume_tracking
from pylabrobot.resources.opentrons import opentrons_96_tiprack_20ul, opentrons_96_tiprack_1000ul
from pylabrobot.resources import ( PLT_CAR_L5AC_A00, Cos_96_DW_1mL, HTF_L)
from pylabrobot.resources.opentrons import corning_96_wellplate_360ul_flat
from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.resource import Resource
from pylabrobot.resources.deck import Deck
from pylabrobot.resources.trash import Trash
from pylabrobot.resources.liquid import Liquid
from pylabrobot.resources.plate import Plate
from pylabrobot.resources.well import Well
from pylabrobot.resources.tip_rack import TipRack, TipSpot
from pylabrobot.resources.petri_dish import PetriDish, PetriDishHolder
from pylabrobot.resources.tube_rack import Tube
from pylabrobot.resources.tube_rack import TubeRack

from resourceCoordinates import ResourceCoordinates
uiDebug=True; frameLabelHolderBackgroundCol="red";frameCanvasAndScrollBarsHolderBackgroundCol="yellow"; canvasBackgroundCol="red"
deckCol="peach puff" if uiDebug else "gray10"

class UiWindow:

    def ym(self, y:float)->float:
         return self.liquidHandler.deck._size_y-y
    
    def yGcode(self, y:float)->float:
         return -y+self.liquidHandler.deck._size_y

    def drawAll(self):
        # self.screenElements.clear()
        self.drawResourceAndChildrenImages(self.liquidHandler.deck)

    # this takes the deck which is the top resource and visualize it and children on the screen  
    def drawResourceAndChildrenImages(self, r:Resource):
        self.createResourceImage(r)
        if len(r.children)>0:
            for child in r.children:
                if not isinstance(child,Resource):
                     print("!!!!!!!!!!!!!!!!WARNING child is not a resource", child.name)
                else:
                    self.drawResourceAndChildrenImages(child)

    def createResourceImage(self, r:Resource):
        z=self.zoom
        if isinstance(r,Deck):
            self.createResourceShapes(r, theFillCol=deckCol)            
            # draw deck and slots
            for i in range(len(self.liquidHandler.deck.slot_locations)):
                slot=self.liquidHandler.deck.slot_locations[i]
                self.createRectangle(slot.x*z, slot.y*z, z*self.slotSizeX, z*self.slotSizeY, fillCol="slate grey", outlineCol="black")
                self.createRectangle(slot.x*z, slot.y*z, z*self.slotPocketSizeX, z*self.slotPocketSizeY, fillCol="light grey", outlineCol="light grey")
                self.canvas.create_text(slot.x*z+8, z*self.ym(slot.y)-8, text=str(i+1), fill="black", font=('Helvetica 10'))            
        elif isinstance(r,Trash):
            self.createResourceShapes(r, theFillCol="gray40")                      
        elif isinstance(r,TipRack):
            self.createResourceShapes(r, theFillCol="aquamarine")            
        elif isinstance(r,TipSpot):
            self.createResourceShapes(r, addCircle=True,theFillCol="white")            
        elif isinstance(r,Plate):
            self.createResourceShapes(r, theFillCol="cyan4")            
        elif isinstance(r,Well):
            self.createResourceShapes(r, addCircle=True,theFillCol="blue")          
        elif isinstance(r,TubeRack):
            self.createResourceShapes(r, theFillCol="red")    
        elif isinstance(r,Tube):
            self.createResourceShapes(r, addCircle=True,theFillCol="blue")    
        elif isinstance(r,PetriDishHolder):
            self.createResourceShapes(r, theFillCol="red")    
        elif isinstance(r,PetriDish):
            self.createResourceShapes(r, addCircle=True,theFillCol="blue") 
        elif isinstance(r,Resource) and r.name=="trash_container":
                self.createResourceShapes(r, theFillCol="black")     
        else:
            messagebox.showinfo("Found unknown type", type(r), r)

    def createResourceShapes(self,r:Resource, addCircle=False, theFillCol="peach puff",theOutlineCol="peach puff"):
        absX=r.get_absolute_location().x*self.zoom
        absY=r.get_absolute_location().y*self.zoom
        sx=r.get_size_x()*self.zoom
        sy=r.get_size_y()*self.zoom
        typeName=type(r).__name__
        if addCircle:
            self.canvas.create_oval(absX, self.ym(absY), absX+sx, self.ym(absY)-sy, fill="white", outline=theOutlineCol)
        else:
            self.createRectangle(absX, absY, sx, sy, fillCol=theFillCol, outlineCol=theOutlineCol)
        if(self.firstDraw):
            self.screenElements.insert(0,ResourceCoordinates(absX,absY, sx, sy,r))
        if  isinstance(r,Plate) or isinstance(r,TipRack) or isinstance(r,Trash):
            self.canvas.create_text(absX+sx/2, self.ym( absY+6), text=r.name, fill="black", font=('Arial 8'))
            #self.canvas.create_text(r.get_absolute_location().x+r.get_size_x()/2, self.ym( r.get_absolute_location().y+8), text=r.name+str(type(r)), fill="red", font=('Helvetica 8'))
        if isinstance(r,PetriDish):
            self.canvas.create_text(absX+2, self.ym( absY+6), text=r.name, fill="black", font=('Arial 8'))
            #self.canvas.create_text(r.get_absolute_location().x+r.get_size_x()/2, self.ym( r.get_absolute_location().y+8), text=r.name+str(type(r)), fill="red", font=('Helvetica 8'))                
            if hasattr(r,"drops"):
                for drop in r.drops: #todo adrian check if the +1 etc are needed
                    self.canvas.create_oval((drop[0]*self.zoom-1), self.ym(drop[1]*self.zoom-1), drop[0]*self.zoom+1, self.ym(drop[1]*self.zoom+1), fill="green", outline=theOutlineCol)
    
    # the zoom adjusted coordinates should be calculater in advance and fed here           
    def createRectangle(self, x0,y0,xSize,ySize, fillCol, outlineCol, widthBorder=0):
        self.canvas.create_rectangle(x0, self.ym(y0), x0+xSize, self.ym(y0)-ySize, fill=fillCol, outline=outlineCol, width=widthBorder)

    def getRectangleName(self, x, y):# y is tk style and so are the elements
        for screenElement in self.screenElements:
            if self.zoom==1 and screenElement.contains(x,self.ym(y), self.zoom):
                return screenElement.resource.name  #todo can also add type(resource).__name__
            elif self.zoom==2 and screenElement.contains(x,self.ym(y-self.liquidHandler.deck._size_y/2), self.zoom):
                return screenElement.resource.name
        return "empty"
         
    @staticmethod
    def getSlotPocketDimensions(): 
        justTempVariableToDetermineSlotSize = opentrons_96_tiprack_1000ul(name="testIgnore") # needed for calculation slot sizes
        return justTempVariableToDetermineSlotSize.get_size_x(), justTempVariableToDetermineSlotSize.get_size_y()

    def __init__(self, rootWindow, liquidHandler):
        self.stack = deque(maxlen = 10)
        self.stackcursor = 0
        self.zoom = 1
        self.liquidHandler:LiquidHandler=liquidHandler
        # some calculations
        for col in range(1,len(self.liquidHandler.deck.slot_locations)):
            if self.liquidHandler.deck.slot_locations[col].x==0:
                 break
        self.slotSizeX=self.liquidHandler.deck.slot_locations[1].x # assume slots go firstly right and then up
        self.slotSizeY=self.liquidHandler.deck.slot_locations[col+1].y
        self.slotPocketSizeX, self.slotPocketSizeY=UiWindow.getSlotPocketDimensions()
        print("pocketSizes:",self.slotPocketSizeX, self.slotPocketSizeY)
        self.firstDraw:bool=True
        self.screenElements:list[ResourceCoordinates]=list()
        # UI starts
        frameLabelHolderBackground=frameLabelHolderBackgroundCol if uiDebug else "gray"
        frameLabelHolder = Frame(rootWindow, bg=frameLabelHolderBackground)
        frameLabelHolder.place_configure(relwidth=0.5, relheight=1, relx=.5, bordermode =OUTSIDE)   
        frameCanvasAndScrollBarsHolderBackground=frameCanvasAndScrollBarsHolderBackgroundCol if uiDebug else "gray"     
        frameCanvasAndScrollBarsHolder = Frame(rootWindow, bg= frameCanvasAndScrollBarsHolderBackground)
        frameCanvasAndScrollBarsHolder.place_configure(relwidth=0.5, relheight=1, relx=0, bordermode =OUTSIDE)       
        self.xyLabel = Label(frameLabelHolder, text = "Coordinates")
        self.xyLabel.place_configure(relwidth=0.5, relheight=.05, rely=0,  relx=0, bordermode =OUTSIDE)   
        # xyLabel.grid(row=0, column=0)             
        self.elementNameLabel:Label = Label(frameLabelHolder, text = "Element Name")
        self.elementNameLabel.place_configure(relwidth=0.5, relheight=.05, relx=0, rely=.05, bordermode =OUTSIDE)
        canvasBackground=canvasBackgroundCol if uiDebug else "gray"
        self.canvas = Canvas(frameCanvasAndScrollBarsHolder,yscrollcommand=Scrollbar.set, width=self.liquidHandler.deck._size_x, height= self.liquidHandler.deck._size_y, bd=0,bg=canvasBackground, cursor="crosshair",highlightthickness=0, highlightbackground="white")
        #xscrollcommand will be set to Scrollbar.set
        sbHorizontalScrollBar = Scrollbar(frameCanvasAndScrollBarsHolder)
        sbVerticalScrollBar = Scrollbar(frameCanvasAndScrollBarsHolder)
        # Sets up the Canvas, Frame, and scrollbars for scrolling based on https://www.joehutch.com/posts/tkinter-dynamic-scroll-area/
        self.canvas.config(xscrollcommand=sbHorizontalScrollBar.set,yscrollcommand=sbVerticalScrollBar.set, highlightthickness=0)
        sbHorizontalScrollBar.config(orient=HORIZONTAL, command=self.canvas.xview)
        sbVerticalScrollBar.config(orient=VERTICAL, command=self.canvas.yview)
        sbHorizontalScrollBar.pack(fill=X, side=BOTTOM, expand=FALSE)
        sbVerticalScrollBar.pack(fill=Y, side=RIGHT, expand=FALSE)

        self.canvas.pack_configure(fill=NONE, anchor="s", side=BOTTOM, expand=TRUE)
        # scrollbarWidth=sbVerticalScrollBar.winfo_depth()
        self.canvas.update_idletasks()
        # canvas.config(scrollregion=(0,0,canvasW+scrollbarWidth,canvasD+scrollbarWidth))
        # END UI
        # Event Binding
        self.canvas.bind("<Motion>", self.showCursorCoordinates)
        self.canvas.bind("<Button-1>", self.zoomButtonAction)        
        self.drawAll()
        self.firstDraw=False # so we don't over collect screenElements

    def showCursorCoordinates(self, event):
        self.xyLabel.config(text = "x="+str(round((event.x),2))+" y="+str(round(self.yGcode(event.y),2))+" Ty="+str(round((event.y),2)))
        self.elementNameLabel.config(text=self.getRectangleName(event.x,event.y))

    def zoomButtonAction(self, event):
        if self.zoom==1:
            self.zoom=2
            self.canvas.config(width=self.liquidHandler.deck._size_x*self.zoom, height=self.liquidHandler.deck._size_y*self.zoom)
            halfYDeckSize=self.liquidHandler.deck._size_y
            self.canvas.config(scrollregion=(0,-halfYDeckSize,self.liquidHandler.deck._size_x*self.zoom, halfYDeckSize))
        else:
            self.zoom=1
            self.canvas.config(width=self.liquidHandler.deck._size_x, height=self.liquidHandler.deck._size_y,
                               scrollregion=(0,0,self.liquidHandler.deck._size_x,self.liquidHandler.deck._size_y))
        self.drawAll()

    def stackify(self):
        None,

    def debug(self):
        print("LiquidHandler", self.liquidHandler)
        # messagebox.showinfo("Model", Controller.model.dump())

class UiBootUp:

    def __init__(self, liquidHandler):
        # really here is where the UI starts being built
        rootWindow = Tk()
        spreadOnX=.95;spreadOnY=.8
        rootWindow.title('LabRobot')
        rootWindow.geometry(str(int(rootWindow.winfo_screenwidth()*spreadOnX))+"x"+str( int(rootWindow.winfo_screenheight()*spreadOnY))+"+"+str( int(rootWindow.winfo_screenwidth()*(1-spreadOnX)/2))+"+"+str( int(rootWindow.winfo_screenheight()*(1-spreadOnY)/2)))
        rootWindow.configure(background='blue') 
        rootWindow.state('zoomed')
        window = UiWindow(rootWindow, liquidHandler)
        rootWindow.bind("<Key>", lambda event: window.stackify())
        rootWindow.protocol( "WM_DELETE_WINDOW", onExit )
        rootWindow.mainloop()


def onExit():
    #messagebox.showinfo("bye", "bye")
    #  UtilFileIO.saveModelToFile()
    #os.path.dirname(os.path.abspath(__file__))+"\\..\\default.fa"
    quit()




# from tkinter import * 
# from tkinter.ttk import *
 
# # creating tkinter window
# root = Tk()
# # getting screen's height in pixels
# height = root.winfo_screenheight()
# width = root.winfo_screenwidth()

# my_var = StringVar()
 
# # defining the callback function (observer)
# def my_callback(var, index, mode):
#     print (("Traced variable ".format(my_var.get())))
 
# # registering the observer
# my_var.trace_add('write', my_callback)
 
# Label(root, textvariable = my_var).pack(padx = 5, pady = 5)
 
# Entry(root, textvariable = my_var).pack(padx = 5, pady = 5)

# print("\n width x height = %d x %d (in pixels)\n" %(width, height))
# # infinite loop
# frameLabelHolderloop()