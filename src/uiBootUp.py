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

class UiWindow:

    def ym(self, y:float)->float:
         return self.liquidHandler.deck._size_y-y
    
    def yGcode(self, y:float)->float:
         return -y+self.liquidHandler.deck._size_y

    def paint(self, event):
        self.xyLabel.config(text = "x="+str(event.x)+" y="+str(self.yGcode(event.y))+" Ty="+str(event.y))
        self.elementNameLabel.config(text=self.getRectangleName(event.x,event.y))
        self.drawAll()

    def drawAll(self):
        self.drawResourceAndChildrenImages(self.liquidHandler.deck)
        print("dump stored screen elements")
        for screenElement in self.screenElements:
            print("Stored screen element",screenElement.resource.name, " with x0=", screenElement.x0)

    # this takes the deck which is the top resource and visualize it and children on the screen  
    def drawResourceAndChildrenImages(self, r:Resource):
        self.createResourceImage(r)
        if len(r.children)>0:
            for child in r.children:
                if not isinstance(child,Resource):
                     print("!!!!!!!!!!!!!!!!WARNING child is not a resource", child.name)
            self.drawResourceAndChildrenImages(child)

    def createResourceImage(self, r:Resource):
        #print(r.category)
        if isinstance(r,Deck):
            # draw deck and slots
            for i in range(len(self.liquidHandler.deck.slot_locations)):
                slot=self.liquidHandler.deck.slot_locations[i]
                self.createRectangle(slot.x, slot.y, self.slotSizeX, self.slotSizeY, fillCol="slate grey", outlineCol="black", widthLine=1)
                self.createRectangle(slot.x, slot.y, self.slotPocketSizeX, self.slotPocketSizeY, fillCol="light grey", outlineCol="light grey", widthLine=1)
                self.canvas.create_text(slot.x+8, self.ym(slot.y)-8, text=str(i+1), fill="black", font=('Helvetica 10'))            
        elif isinstance(r,Trash):
            self.createResourceRectangle(r, theFillCol="brown")                      
        elif isinstance(r,TipRack):
            self.createResourceRectangle(r, theFillCol="red")            
        elif isinstance(r,TipSpot):
            self.createResourceRectangle(r, theFillCol="blue")            
        elif isinstance(r,Plate):
            self.createResourceRectangle(r, theFillCol="blue")            
        elif isinstance(r,Well):
            self.createResourceRectangle(r, theFillCol="blue")            
        elif isinstance(r,TubeRack):
            self.createResourceRectangle(r, theFillCol="blue")    
        elif isinstance(r,Tube):
            self.createResourceRectangle(r, theFillCol="blue")    
        elif isinstance(r,PetriDishHolder):
            self.createResourceRectangle(r, theFillCol="blue")    
        elif isinstance(r,PetriDish):
            self.createResourceRectangle(r, theFillCol="blue")    
        elif isinstance(r,Resource) and r.name=="trash_container":
                self.createResourceRectangle(r, theFillCol="black")     
        else:
            print("!!!!!!!!!!!!!!!!!!! found unknown type", type(r), r)


    def createResourceRectangle(self,r:Resource,theFillCol="peach puff",theOutlineCol="peach puff"):
        self.createRectangle(r.get_absolute_location().x, r.get_absolute_location().y, r.get_size_x(), r.get_size_y(), fillCol=theFillCol, outlineCol=theOutlineCol, widthLine=1)
        if(self.firstDraw):
            print("ADDING screen element ",r.name, r.get_absolute_location().x,r.get_absolute_location().y, r.get_size_x(), r.get_size_y())
            self.screenElements.insert(0,ResourceCoordinates(r.get_absolute_location().x,r.get_absolute_location().y, r.get_size_x(), r.get_size_y(),r))
        #self.canvas.create_text(r.get_absolute_location().x+r.get_size_x()/2, self.ym( r.get_absolute_location().y+8), text=r.name, fill="red", font=('Helvetica 10'))
        #self.canvas.create_text(r.get_absolute_location().x+r.get_size_x()/2, self.ym( r.get_absolute_location().y+8), text=r.name+str(type(r)), fill="red", font=('Helvetica 10'))
                
    def createRectangle(self, x0,y0,xSize,ySize, fillCol, outlineCol, widthLine=1):
        #print("create rectangle at",x0, self.ym(y0), x0+xSize, self.ym(y0)-ySize,"of sizes:",xSize,ySize)
        self.canvas.create_rectangle(x0, self.ym(y0), x0+xSize, self.ym(y0)-ySize, fill=fillCol, outline=outlineCol, width=widthLine)

    def getRectangleName(self, x, y):# y is tk style and so are the elements
        for screenElement in self.screenElements:
            if screenElement.contains(x,self.ym(y)):
                return screenElement.resource
        return "empty"
         

    def __init__(self, master, liquidHandler):
        self.master = master
        self.mainFrame = Frame(self.master)
        self.mainFrame.grid(row=0, column=0)
        self.stack = deque(maxlen = 10)
        self.stackcursor = 0
        self.liquidHandler:LiquidHandler=liquidHandler
        # some calculations
        for col in range(1,len(self.liquidHandler.deck.slot_locations)):
            if self.liquidHandler.deck.slot_locations[col].x==0:
                 break
        self.slotSizeX=self.liquidHandler.deck.slot_locations[1].x # assume slots go  right first and then up
        self.slotSizeY=self.liquidHandler.deck.slot_locations[col+1].y
        justTempVariableToDetermineSlotSize = opentrons_96_tiprack_1000ul(name="testIgnore") # needed for calculation slot sizes
        self.slotPocketSizeX=justTempVariableToDetermineSlotSize.get_size_x()
        self.slotPocketSizeY=justTempVariableToDetermineSlotSize.get_size_y()
        self.firstDraw:bool=True
        self.screenElements:list[ResourceCoordinates]=list()
        # UI
        self.xyLabel:Label = Label(self.mainFrame, text = "Coordinates")
        self.elementNameLabel:Label = Label(self.mainFrame, text = "Element Name")
        self.xyLabel.pack(padx = 5, pady = 5)
        self.elementNameLabel.pack(padx = 5, pady = 5)
         # Add a Scrollbar (horizontal)
        scrollbar=Scrollbar(self.mainFrame, orient='horizontal')
        self.menu = Menu(self.mainFrame)
        self.menu.add_command(label = "Debug", command = self.debug)
        #self.mainFrame.config(menu = self.menu)

        # Making a Canvas https://www.tutorialspoint.com/python/tk_place.htm
        self.canvas = Canvas(self.master, width= liquidHandler.deck._size_x,
                              height= liquidHandler.deck._size_y, bd=0,bg="white", cursor="crosshair",
                              highlightthickness=0, highlightbackground="blue")
        self.canvas.grid(row=0, column=0)
        self.canvas.grid(row=0, column=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER, bordermode =OUTSIDE)
        self.canvas.config()#cursor="pencil")

        # Event Binding
        self.canvas.bind("<Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)        
        self.mainFrame.pack(padx = 5, pady = 5, fill= BOTH)
        self.drawAll()
        self.firstDraw=False # so we don't over collect screenElements
 
    def display(self):
        print(self.sequenceTextBox.get("1.0", "end"))     

    def clear(self):
        self.sequenceTextBox.delete("1.0", "end")
 
    def stackify(self):
        None
 
    def undo(self):
        if self.stackcursor != 0:
            self.clear()
            if self.stackcursor > 0: self.stackcursor -= 1
            self.sequenceTextBox.insert("0.0", self.stack[self.stackcursor])
 
    def redo(self):
        if len(self.stack) > self.stackcursor + 1:
            self.clear()
            if self.stackcursor < 9: self.stackcursor += 1
            self.sequenceTextBox.insert("0.0", self.stack[self.stackcursor])
 
    def debug(self):
        # print("Model")
        # print(Controller.model.dump())
        # messagebox.showinfo("Model", Controller.model.dump())
        messagebox.showinfo("Model", "TADA ADRIAN")

    def printStack(self):
        i = 0
        for stack in self.stack:
            print(str(i) + " " + stack)
            i += 1

    def update(self):
        print("update called")
        line = self.canvas.create_line(100, 20, 50, 100, fill="red", width=2) 

    
# Clear Screen
    def clearScreen(self):
        self.canvas.delete("all")

    # def showForbiddenListFromFile(self):
    #     listString=""
    #     for line in Controller.model.forbiddenList:
    #         listString+=line
    #     messagebox.showinfo("Forbidden list", listString+"                    ")

    # def debug(self):
    #     print("Model")
    #     print(Controller.model.dump())
    #     messagebox.showinfo("Model", Controller.model.dump())
        
    # end class    

def onExit():
     #messagebox.showinfo("bye", "bye")
    #  UtilFileIO.saveModelToFile()
     #os.path.dirname(os.path.abspath(__file__))+"\\..\\default.fa"
     quit()

class UiBootUp:
     def __init__(self, liquidHandler):
        rootWindow = Tk()
        rootWindow.title('text')
        rootWindow.geometry(str(rootWindow.winfo_screenwidth())+"x"+str( int(rootWindow.winfo_screenheight()*.7)))
        rootWindow.state('zoomed')
        window = UiWindow(rootWindow, liquidHandler)
        #rootWindow.attributes('-fullscreen', True)
        #screen_width = win.winfo_screenwidth()
        rootWindow.bind("<Key>", lambda event: window.stackify())
        rootWindow.protocol( "WM_DELETE_WINDOW", onExit )
        rootWindow.mainloop()

  




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
# mainFrameloop()