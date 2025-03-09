import tkinter as tk
from tkinter import Menu
import os
import sys
from pathlib import Path
from tkinter import filedialog, messagebox
import cv2 
import numpy as np 
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image
import math

#  CTRL SHIFT P indent  
canvas=None
class UiApp:

    def __init__(self:tk.Widget, root:tk):
        self.canvas=None
        self.root:tk = root
        self.root.title("ImageToOutlineDotsConverter")
        screen_width = root.winfo_screenwidth()-20
        screen_height = int(root.winfo_screenheight()/2)
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.createMenu(root)
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
        fileMenu.add_command(label="Load File", command=lambda:self.loadSequencesHandler())
        root.config(menu=self.menuBar)   
          
    def loadSequencesHandler(self):
        self.textboxPointsNumber.config(state="normal")
        self.textboxPointsNumber.delete(0, tk.END)
        self.textboxPointsNumber.config(state="readonly")     
        rootPath=getInitialPath()
        black_centers = createPoints()
        self.textboxPointsNumber.config(state="normal")
        self.textboxPointsNumber.delete(0, tk.END)
        self.textboxPointsNumber.insert(tk.END, str(len(black_centers)))    
        self.textboxPointsNumber.config(state="readonly")                  
        x_coords = [point[0] for point in black_centers]# Extract the x and y coordinates from the list of centers
        y_coords = [point[1] for point in black_centers]
        plt.figure(figsize=(8, 8))# Plot the points using plt.scatter
        plt.scatter(x_coords, y_coords, c="black")
        maxX,maxY,minX,minY=findLimits(black_centers)
        h, w = (maxY,maxX) # Set the axis limits to the size of the image
        plt.xlim(-43, 43)
        plt.ylim(-43, 43)
        plt.title(f"There are {len(black_centers)} points")
        plt.gca().set_aspect("equal", adjustable="box")# Set the aspect of the plot to be equal
        print (findLimits(black_centers))
        dotArrayPath=rootPath+"/dotarray.npy"
        np.save(dotArrayPath,black_centers)
        arr=np.load(dotArrayPath)
        print (findLimits(arr))
        fig = plt.gcf()
        fig.canvas.manager.window.title(dotArrayPath)            
        centerWindowHorizontally(fig)    
        plt.show()# Display the plot 
        messagebox.showinfo("dotArrany.npy saved", f"The dotArrany.npy file containing all the coordinates of the points relative to the center of the image was saved   as {dotArrayPath}")            
        # Call the center window function after plotting
        return None,None

def findLimits(array):
    maxX=0;maxY=0;minX=0;minY=0
    for p in array:
        if p[0]>maxX: maxX= p[0]
        if p[1]>maxY: maxY= p[1]
        if p[0]<minX: minX= p[0]
        if p[1]<minY: minY= p[1]
    return maxX, maxY, minX, minY


def getInitialPath():
    base=None
    if getattr(sys, 'frozen', False):  # If running from a bundled executable
        print("running from a bundled Exec")
        base= str(Path(sys._MEIPASS))
    else:  # If running from a script
        base=os.getcwd()
    print("basePath",base)
    return base


def createPoints():
    centerLocation=(0,0)
    points =list()
    steps=10
    circle(-15, 15, 3, steps, centerLocation, points)
    circle(15, 15, 3, steps, centerLocation, points)
    line(-10, -10, 8, 8, steps, centerLocation, points)
    line(-10, -10, 10, -10, steps, centerLocation, points)
    line(-15, -23, 20, -23, steps, centerLocation, points)
    line(-15, -23, 0, -30, 5, centerLocation, points)
    line(0, -30, 20, -23, 5, centerLocation, points)    
    return points

def findLimits(array):
    maxX=0;maxY=0;minX=0;minY=0
    for p in array:
        if p[0]>maxX: maxX= p[0]
        if p[1]>maxY: maxY= p[1]
        if p[0]<minX: minX= p[0]
        if p[1]<minY: minY= p[1]
    return maxX, maxY, minX, minY

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

def line(x1, y1, x2, y2, steps, center_location, points:list):
  x_distance = x2 - x1
  y_distance = y2 - y1
  x_separation = x_distance / steps
  y_separation = y_distance / steps
  for i in range(steps):
    # points.append(center_location.move(x=x1+i*x_separation, y=y1+i*y_separation))
    points.append((x1+i*x_separation, y1+i*y_separation))

def circle(center_x, center_y, radius, steps, center_location,points:list):
  for i in range(steps):
    angle = 2 * math.pi * i / steps
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    points.append((x, y))


root = tk.Tk()
app = UiApp(root)
root.mainloop()
