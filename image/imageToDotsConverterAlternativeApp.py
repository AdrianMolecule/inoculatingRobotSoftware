import tkinter as tk
from tkinter import Menu
import os
import sys
from pathlib import Path
from tkinter import filedialog, messagebox
import cv2 
import numpy as np 
#  CTRL SHIFT P indent  
canvas=None
class UiApp:

    def __init__(self:tk.Widget, root:tk):
        self.canvas=None
        self.root:tk = root
        self.root.title("ImageToDotConverter")
        screen_width = root.winfo_screenwidth()-20
        screen_height = int(root.winfo_screenheight()/2)
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.createCanvasWithScrollbar()  
        # self.root.grid_columnconfigure(0, weight=0)    
        self.root.grid_columnconfigure(1, weight=1)    # make the main canvas take all the horizontal space
        self.createMenu(root)
        # Configure grid to allow resizing  
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        # Create max
        label = tk.Label(root, text="Max points")
        label.grid(row=0, column=0, sticky="e")     
        self.textbox = tk.Entry(root, width=10)
        self.textbox.insert(0, "40") 
        self.textbox.grid(row=0, column=1, sticky="e")     

    def createCanvasWithScrollbar(self):
        self.canvas = tk.Canvas(canvas, bg="lightgray", height=350, bd=0)        
        self.canvas.grid(row=1, column=0, columnspan=2, sticky="sew")  # Span across both columns        
        self.canvas.grid_rowconfigure(1, weight=1)
        self.canvas.grid_columnconfigure(0, weight=2)        

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
        filePath = filedialog.askopenfilename(title="Open Image", initialdir=getInitialPath(), filetypes=[("Png file", "*.png"), ("All Files", "*.*")])  	
        rootPath=os.path.dirname(filePath)
        if filePath:
            try:
                print("loading",filePath)
                image = cv2.imread(filePath)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                imageInfo(gray, "gray")
                cv2.waitKey(0) 
                edged = cv2.Canny(gray, 30, 200) # Find Canny edges
                cnts,h = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                outline = np.full(gray.shape,255, dtype=np.uint8)
                cv2.drawContours(outline, cnts, -1, (0, 0, 255), 1)
                cv2.imwrite(rootPath+"outline.png", outline)
                (thresh, blackAndWhiteImage) = cv2.threshold(outline, 254, 255, cv2.THRESH_BINARY)
                imageInfo(blackAndWhiteImage,"blackAndWhiteImage")
                # resize does not seem to get great results
                h,w=outline.shape[:2]
                maxDim=int(self.textbox.get())  
                r=maxDim/h if h>w else maxDim/w
                resizedImage = cv2.resize(blackAndWhiteImage, (int(w*r), int(h*r))) #width/height
                imageInfo(resizedImage,"resizedImage")
                cv2.imwrite(rootPath+"resizedImage.png", outline)
                # cv2.imshow('resized_image', resizedImage)
                # cv2.waitKey(0)
                # final part
                centeredDotArray=createPetriStyleArray(resizedImage)
                print("Limits:",findLimits(centeredDotArray), "points", len(centeredDotArray))
                np.save(rootPath+"/dotarray.npy",centeredDotArray)
                #recover the image from the centeredArray
                petriStyleImageArray=np.load(rootPath+"/dotarray.npy")
                height,width=resizedImage.shape[:2]
                showImageFromPetriStyleArray(petriStyleImageArray, height, width)                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while reading the file: {e}")
        return None,None

def getInitialPath():
    base=None
    if getattr(sys, 'frozen', False):  # If running from a bundled executable
        print("running from a bundled Exec")
        base= str(Path(sys._MEIPASS))
    else:  # If running from a script
        base=os.getcwd()
    print("basePath",base)
    return base


def createPetriStyleArray(image):
    h, w = image.shape[:2]
    black_dots = []
    # Process each block
    for y in range(0, h):
        for x in range(0, w):
            if image[y,x]<255:
                center_x = x + 1 / 2 - w / 2
                center_y = h / 2 - (y +1 / 2)
                black_dots.append((center_x, center_y))    
    return black_dots

def showImageFromPetriStyleArray(petriArray, height, width):
    print("h, w=",height, width)
    recoveredImageArray = np.full((height, width), int(255), np.uint8)  # '255' for white in a 1-channel image
    # petriArray
    for p in petriArray:
        #recoveredImageArray[int(h/2),int(w/2)] = 0 # Set to '0' for black and should be in the centere of the screen
        recoveredImageArray[int(height/2-p[1]), int(p[0]-width/2)] = 0 # Set to '0' for black @ y from top down x from left to right
    print("After Loading np.load Limits:",findLimits(petriArray), "points", len(petriArray))
    cv2.imshow("image", recoveredImageArray)
    cv2.waitKey()

def imageInfo(image, imageName=""):
    h,w=image.shape[:2]
    print("image "+imageName+ " dimensions",h,w, " black pixels",h*w-cv2.countNonZero(image)) # Get the dimensions of the image

def findLimits(array):
    maxX=0;maxY=0;minX=0;minY=0
    for p in array:
        if p[0]>maxX: maxX= p[0]
        if p[1]>maxY: maxY= p[1]
        if p[0]<minX: minX= p[0]
        if p[1]<minY: minY= p[1]
    return maxX, maxY, minX, minY



root = tk.Tk()
app = UiApp(root)
root.mainloop()
