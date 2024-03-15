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
from pylabrobot.resources.plate import Plate
from pylabrobot.resources.resource import Resource
from pylabrobot.resources.liquid import Liquid
from pylabrobot.resources.well import Well
from pylabrobot.resources.tip_rack import TipSpot, TipRack
from pylabrobot.resources.petri_dish import PetriDish, PetriDishHolder

class UiWindow:

    def ym(self, y)->int:
         return self.liquidHandler.deck._size_y-y

    def paint(self, event):
        self.sequenceLabel.config(text = "x="+str(event.x)+" y="+str(event.y)+" Ty="+str(self.ym(event.y)))
        self.draw()

    def draw(self):
        print(self.liquidHandler.deck.children)
        for i in range(len(self.liquidHandler.deck.slot_locations)):
            slot=self.liquidHandler.deck.slot_locations[i]
            self.createRectangle(slot.x, slot.y, self.slotSizeX, self.slotSizeY, fillCol="slate grey", outlineCol="black", widthLine=1)
            self.createRectangle(slot.x, slot.y, self.slotPocketSizeX, self.slotPocketSizeY, fillCol="light grey", outlineCol="light grey", widthLine=1)
            self.canvas.create_text(slot.x+8, self.ym(slot.y)-8, text=str(i+1), fill="black", font=('Helvetica 10'))
        for c in self.liquidHandler.deck.children:
            self.resource(c)

    # this takes a resource and visualize it on the screen  
    def resource(self, r:Resource):
        self.createRectangle(r.get_absolute_location().x, r.get_absolute_location().y, r.get_size_x(), r.get_size_y(), fillCol="peach puff", outlineCol="peach puff", widthLine=1)
        self.canvas.create_text(r.get_absolute_location().x+r.get_size_x()/2, self.ym( r.get_absolute_location().y+8), text=r.name, fill="red", font=('Helvetica 10'))
        
    def createRectangle(self, x0,y0,xSize,ySize, fillCol, outlineCol, widthLine=1):
        print("create rectangle at",x0, self.ym(y0), x0+xSize, self.ym(y0)-ySize,"of sizes:",xSize,ySize)
        self.canvas.create_rectangle(x0, self.ym(y0), x0+xSize, self.ym(y0)-ySize, fill=fillCol, outline=outlineCol, width=widthLine)

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
        tips = opentrons_96_tiprack_1000ul(name="test") 
        self.slotPocketSizeX=tips.get_size_x()
        self.slotPocketSizeY=tips.get_size_y()
        # UI elements
        self.sequenceLabel:Label = Label(self.mainFrame, text = "Coordinates")
        self.sequenceLabel.pack(padx = 5, pady = 5)
         # Add a Scrollbar(horizontal)
        scrollbar=Scrollbar(self.mainFrame, orient='horizontal')
        self.menu = Menu(self.mainFrame)
        self.menu.add_command(label = "Debug", command = self.debug)
        #self.mainFrame.config(menu = self.menu)

        # Making a Canvas
        self.canvas = Canvas(self.master, width= liquidHandler.deck._size_x, height= liquidHandler.deck._size_y, bg="white")
        self.canvas.grid(row=0, column=0)
        self.canvas.grid(row=0, column=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.canvas.config(cursor="pencil")

        # Event Binding
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)        
        self.mainFrame.pack(padx = 5, pady = 5, fill= BOTH)
        self.draw()
 
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