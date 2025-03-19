import tkinter as tk
from tkinter import Menu
import os
import sys
from pathlib import Path
from tkinter import filedialog, messagebox
import cv2 
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
import numpy as np 
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image
import math

#  CTRL SHIFT P indent  

PETRI_DIAMETER=int(90)
PETRI_RADIUS=int(PETRI_DIAMETER/2)

canvas=None
class UiApp:

    def __init__(self:tk.Widget, root:tk):
        self.canvas=None
        self.root:tk = root
        self.root.title("ImageToOutlineDotsConverter")
        screen_width = root.winfo_screenwidth()-20
        screen_height = int(root.winfo_screenheight()/2)
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        # self.createCanvasWithScrollbar()  
        # self.root.grid_columnconfigure(0, weight=0)    
        # self.root.grid_columnconfigure(1, weight=1)    # make the main canvas take all the horizontal space
        self.createMenu(root)
        # Configure grid to allow resizing  
        # self.root.grid_rowconfigure(0, weight=1)
        # self.root.grid_columnconfigure(1, weight=1)
        # Create max
        label = tk.Label(root, text="Sampling Block Size:")
        label.grid(row=0, column=0, sticky="e")     
        self.textbox = tk.Entry(root, width=10)
        self.textbox.insert(0, "6") 
        self.textbox.grid(row=0, column=1, sticky="e")   
        label2 = tk.Label(root, text="Max points")
        label2.grid(row=0, column=2, sticky="e")             
        self.textboxPointsNumber = tk.Entry(root, width=10, state="readonly") 
        self.textboxPointsNumber.insert(0, "calculated after loading the file") 
        self.textboxPointsNumber.grid(row=0, column=3, sticky="e")   
        self.checkboxVar = tk.BooleanVar(value=True)
        # Create a Checkbutton widget, linked to the BooleanVar
        checkbox = tk.Checkbutton(root, text="Outline Only", variable=self.checkboxVar)  
        checkbox.grid(row=0, column=4, sticky="e")


    def createCanvasWithScrollbar(self):
        self.canvas = tk.Canvas(canvas, bg="lightgray", height=350, bd=0)        
        self.canvas.grid(row=1, column=0, columnspan=3, sticky="sew")  # Span across both columns        
        self.canvas.grid_rowconfigure(1, weight=1)
        self.canvas.grid_columnconfigure(0, weight=3)        

    def exitApplication(self):
        self.root.quit()      

    def createMenu(self, root):
        self.menuBar = Menu(root)
        # Left menu: File Load
        fileMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Load File", command=lambda:self.readFileHandler())
        fileMenu.add_command(label="Save File", command=lambda:self.saveFileHandler())
        root.config(menu=self.menuBar)   
          
    filePath = None 
    points=None

    def saveFileHandler(self):
        fileName: str = os.path.splitext(os.path.basename(self.filePath))[0]
        dotArrayPath=rootPath=getInitialPath()+"/"+fileName+"Edited.npy"            
        np.save(dotArrayPath,arr=self.points)
        messagebox.showinfo("Info", f"File saved as {dotArrayPath}")    

    def readFileHandler(self):
        self.textboxPointsNumber.config(state="normal")
        self.textboxPointsNumber.delete(0, tk.END)
        self.textboxPointsNumber.config(state="readonly")         
        filePath = filedialog.askopenfilename(title="Open array", initialdir=getInitialPath(), filetypes=[("Python array file", "*.npy"), ("All Files", "*.*")])  	
        rootPath=os.path.dirname(filePath)
        if filePath:
            try:
                print("loading",filePath)
                self.points=np.load(filePath)
                self.filePath=filePath
                self.createPlot( filePath)                  
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while reading the file: {e}")

    def createPlot(self, path):    
            plt.figure(figsize=(6, 6))# Plot the points using plt.scatter
            plt.xlim(-PETRI_RADIUS, PETRI_RADIUS) # for Petri dish that is  
            plt.ylim(-PETRI_RADIUS,PETRI_RADIUS)
            plt.title(f"There are {len(self.points)} points")
            plt.gca().set_aspect("equal", adjustable="box")#     Set the aspect of the plot to be equal
            fig = plt.gcf()
            fig.canvas.mpl_connect('button_press_event', self.onclick) 
            fig.canvas.manager.window.title(f"{path} self.points {len(self.points)} points")# Set the title of the window to the path of the image)       
            centerWindowHorizontally(fig)   
            self.redrawPlot(path)  

    def redrawPlot(self, path):  
            xCoords = [point[0] for point in self.points]# Extract the x and y coordinates from the list of centers
            yCoords = [point[1] for point in self.points]        
            self.scatter=plt.scatter(xCoords, yCoords, s=4, c="black")       
            plt.show()# Display the plot    

    # Function to remove points on click
    def onclick(self, event):
        print("in onclick self.points[0]",self.points[0])         
        if event.inaxes:  # Check if the click is inside the axes
            x_click, y_click = event.xdata, event.ydata
            distances = ((self.scatter.get_offsets()[:, 0] - x_click) ** 2 + 
                        (self.scatter.get_offsets()[:, 1] - y_click) ** 2)
            closest_index = distances.argmin()            
            if distances[closest_index] < 0.7:  # Adjust the threshold as needed
                print("removing",self.points[closest_index])
                self.points=np.delete(self.points, closest_index,axis=0)
                print("new points len",len(self.points))
                plt.cla()
                self.redrawPlot( self.filePath)   

def getInitialPath():
    base=None
    if getattr(sys, 'frozen', False):  # If running from a bundled executable
        print("running from a bundled Exec")
        base= str(Path(sys._MEIPASS))
    else:  # If running from a script
        base=os.getcwd()
    print("basePath",base)
    return base


def centerWindowHorizontally(fig):
    # Get the Tkinter canvas associated with the plot
    canvas = fig.canvas.manager.window
    # Get the screen width and height
    screenWidth = canvas.winfo_screenwidth()
    screenHeight = canvas.winfo_screenheight()
    # Get the window width and height
    windowWidth = canvas.winfo_width()
    windowHeight = canvas.winfo_height()
    # Calculate the position to center the window
    positionTop = 10#int((screenHeight - windowHeight) / 2)
    positionLeft = int((screenWidth - windowWidth) / 2)
    # Set the window position using geometry (x, y)
    canvas.geometry(f"+{positionLeft}+{positionTop}")


root = tk.Tk()
app = UiApp(root)
root.mainloop()
	