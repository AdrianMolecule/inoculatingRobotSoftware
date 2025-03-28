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
from lxml import etree
from collections import OrderedDict
from svgpathtools import parse_path

#  CTRL SHIFT P indent  
canvas=None
PETRI_DIAMETER=int(90)
HOP=2
PETRI_RADIUS=int(PETRI_DIAMETER/2)
REMOVE_SHORT_LINES=True
JUST_FILE_NAME="students/m1.svg" #"students/path.svg"
fast=False#True will bypass file selection and go witht eh hardcoded on

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
        fileMenu.add_command(label="Load File", command=lambda:self.loadSourceImage())
        root.config(menu=self.menuBar)   
    
    def loadSourceImage(self):
        self.textboxPointsNumber.config(state="normal")
        self.textboxPointsNumber.delete(0, tk.END)
        self.textboxPointsNumber.config(state="readonly")  
        rootPath=getInitialPath()
        print("rootPath",rootPath)
        svg=True
        if fast:
            filePath="C:\\a\\diy\\pythonProjects\\labRobot\\image/"+JUST_FILE_NAME
        else:
            filePath = filedialog.askopenfilename(title="Open Image", initialdir=rootPath, filetypes=[("Png file", "*.png"), ("All Files", "*.*")])  	
            if filePath:
                try:
                    print("loading",filePath)
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while reading the file: {e}")        
                    return None, None  
        if svg:              
            polygonPointsList:list=createPoints(filePath)            
            scaledPolygonPointsList=scaleAndCenter(polygonPointsList)
            print("scaledAndCenter: ", scaledPolygonPointsList)
            allPoints =list()
            for poly in scaledPolygonPointsList:
                polygon(poly,HOP,allPoints)
            # circle(0, 0, 3, hop, centerLocation, points)
            fileName: str = os.path.splitext(os.path.basename(filePath))[0]
            dotArrayPath=rootPath+"/"+fileName+"DotArray.npy"            
            np.save(dotArrayPath,arr=allPoints)
        else:#image
            blockDim=int(self.textbox.get()) #change here for higher/lower number of points
            image = cv2.imread(filePath) ;   
            #image = cv2.imread("C:/a/diy/pythonProjects/labRobot/src/image/leaf.png") ;    blockDim=6#12
            adrian_block_size=(blockDim,blockDim) #6 and 6 is the best but image is 2 pixel too large
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Grayscale Maybe ConvertColor?
            threshold = 30 #127 
            _, blackAndWhiteImage=cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)  # Threshold the image              
            if self.checkboxVar.get():
                edged = cv2.Canny(blackAndWhiteImage, 30, 200) # Find Canny edges
                # Finding Contours # Use a copy of the image e.g. edged.copy() # since findContours alters the image 
                contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) ##cv2.imshow('Canny Edges After Contouring', edged) 
                print("Number of Contours found = " + str(len(contours))) # Draw all contours # -1 signifies drawing all contours # cv2.drawContours(image, contours, -1, (0, 255, 0), 3) 
                # cv2.imshow('Contours', image) # cv2.waitKey(0) 
                h, w = image.shape[:2]
                contourArray = np.full((h,w),255, dtype=np.uint8) #255 is white empty image just an array of numbers
                cv2.drawContours(contourArray, contours, -1, (0, 255, 0), 3)    
                dotArray = createDotImageOpencv(contourArray, adrian_block_size)# Call the function to create and save the dot image
            else:
                dotArray = createDotImageOpencv(blackAndWhiteImage, adrian_block_size)# Call the function to create and save the dot image
            allPoints = find_centers_of_black_sections(dotArray)# Call the function to find centers of black sections
            self.textboxPointsNumber.config(state="normal")
            self.textboxPointsNumber.delete(0, tk.END)
            self.textboxPointsNumber.insert(tk.END, str(len(allPoints)))    
            self.textboxPointsNumber.config(state="readonly")  
        createPlot(allPoints, rootPath, dotArrayPath)                            
        messagebox.showinfo("dotArrany.npy saved", f"The dotArrany.npy file containing all the coordinates of the points relative to the center of the image was saved   as {dotArrayPath}")            
        # Call the center window function after plotting
        return None,None

def scaleAndCenter(po):
        BORDER=5 # 5 mm border
        allPointsArray = list()
        for i, points in enumerate(po):
            # print(f"Raw Polygon {i+1}: {points}")   
            allPointsArray.extend(points) 
        maxX,maxY,minX,minY=findLimits(allPointsArray)        
        print ("Raw maxX:",maxX, " maxY:",maxY," minX:",minX, " minY:",minY, " rangeX:",maxX-(minX), " rangeY:",maxY-(minY))
        scale=(PETRI_DIAMETER-BORDER)/max(maxX-minX,maxY-minY)
        allScaledPointsArray = list()     
        maxX=None
        maxY=None
        minX=None
        minY=None
        for points in po:  
            newScaledPoly=[]                
            for p in points:
                newX=p[0]*scale
                newY=p[1]*scale
                newScaledPoly.append((newX,newY))
                if maxX==None or newX>maxX: maxX=newX
                if maxY==None or newY>maxY: maxY=newY
                if minX==None or newX<minX: minX=newX
                if minY==None or newY<minY: minY=newY
            allScaledPointsArray.append(newScaledPoly)
        print ("Scaled maxX:",maxX, " maxY:",maxY," minX:",minX, " minY:",minY, " rangeX:",maxX+abs(minX), " rangeY:",maxY+abs(minY))
        translateX=(maxX-minX)/2+minX
        translateY=(maxY-minY)/2+minY
        allTranslatedPointsArray = list()            
        for points in allScaledPointsArray:           
            newTranslatedPoly=[]
            for p in points:
                newX=p[0]-translateX
                newY=-(p[1]-translateY)# adrian in here I switch y with -y to have the y axis go up
                newTranslatedPoly.append((round(newX,1),round(newY,1)))
            allTranslatedPointsArray.append(newTranslatedPoly)
        return allTranslatedPointsArray     

def createPoints(filePath):
    tree = etree.parse(filePath)
    polygons = tree.findall(".//{http://www.w3.org/2000/svg}polygon")
    # Extract points for each polygon
    polygonPointsList = []
    for polygon in polygons:
        points_string = polygon.get("points")
        points: list[tuple[float, ...]] = [tuple(map(float, point.split(","))) for point in points_string.split()]
        polygonPointsList.append(points)

    #PATHS
    pathPointsList = []
    paths = tree.findall(".//{http://www.w3.org/2000/svg}path")
    if(len(paths)>0):
        for path in paths:
            pathString = path.get("d")
            path = parse_path(pathString)
            # Extract points
            for segment in path:
                pathPointsList.append((segment.start.real, segment.start.imag))
                pathPointsList.append((segment.end.real, segment.end.imag))

        print("Extracted Points:", pathPointsList)
        # Convert to a list of x and y coordinates
        x, y = zip(*pathPointsList)
        plt.figure(figsize=(8, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='b')  # 'o' for points, '-' for lines
        plt.title('SVG Path Points')
        plt.xlabel('X Coordinates')
        plt.ylabel('Y Coordinates')
        plt.grid()
        plt.axis('equal')  # Keep the aspect ratio square
        plt.show()

    # Print the points for each polygon
    for i, points in enumerate(polygonPointsList):
        print(f"Raw Polygon {i+1}: {points}")       
    return polygonPointsList

def createPlot(blackCenters, rootPath, blackCentersPath):
        x_coords = [point[0] for point in blackCenters]# Extract the x and y coordinates from the list of centers
        y_coords = [point[1] for point in blackCenters]
        plt.figure(figsize=(6, 6))# Plot the points using plt.scatter
        plt.scatter(x_coords, y_coords, s=4, c="black")        
        plt.xlim(-PETRI_RADIUS, PETRI_RADIUS) # for Petri dish that is 
        plt.ylim(-PETRI_RADIUS,PETRI_RADIUS)
        plt.title(f"There are {len(blackCenters)} points. Adjust the blocksize up if you want less points.")
        plt.gca().set_aspect("equal", adjustable="box")# Set the aspect of the plot to be equal
        fig = plt.gcf()
        fig.canvas.manager.window.title(blackCentersPath)            
        centerWindowHorizontally(fig)    
        plt.show()# Display the plot     


def polygon(  poWithDuplicates:list,hop, points:list):
    po=list(OrderedDict.fromkeys(poWithDuplicates))
    previous=po[0]
    for p in po[1:]:
        line(previous[0], previous[1], p[0],p[1], hop, points)
        previous=p
    line(previous[0], previous[1], po[0][0],po[0][1], hop, points)

def createPointsSmiley():
    centerLocation=(0,0)
    points =list()
    steps=10
    circle(-15, 15, 3, steps,  points)
    circle(15, 15, 3, steps,  points)
    line(-10, -10, 8, 8, steps,  points)
    line(-10, -10, 10, -10, steps,  points)
    line(-15, -23, 20, -23, steps,  points)
    line(-15, -23, 0, -30, 5,  points)
    line(0, -30, 20, -23, 5,  points)    
    return points


def line(x1, y1, x2, y2, hop, points:list):
    x_distance = x2 - x1
    y_distance = y2 - y1
    lineLen=math.sqrt(x_distance**2 + y_distance**2)
    steps=int(lineLen/hop)
    if steps==0: 
        if REMOVE_SHORT_LINES: return
        steps=1
    x_separation = x_distance / steps
    y_separation = y_distance / steps
    for i in range(steps+1):
        points.append((round(x1+i*x_separation,1),round(y1+i*y_separation,1)))
    print("\nline points",points)

def circle(center_x, center_y, radius, steps,points:list):
  for i in range(steps):
    angle = 2 * math.pi * i / steps
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    points.append((x, y))


# Now we define a function to create a ?x? dot pattern image using OpenCV
def createDotImageOpencv(image:Image, block_size, threshold=128)->Image:
#def create_dot_image_opencv(image, block_size=(26, 26), threshold=128):
    # Get the dimensions of the image
    h, w = image.shape[:2]
    # Calculate the number of blocks
    w_blocks = w / block_size[0]
    h_blocks = h / block_size[1]
    # Create a new image for the dots, initializing to white
    dot_imageArray = np.full((int(h_blocks)+1, int(w_blocks)+1), int(255), np.uint8)  # '255' for white in a 1-channel image
    # Process each block
    for y in range(0, h, block_size[1]):
        for x in range(0, w, block_size[0]):
            # Extract the block from the image
            block = image[y : y + block_size[1], x : x + block_size[0]]
            # Calculate the average brightness of the block
            block_brightness = np.mean(block)
            # If the average brightness is lower than the threshold, set the corresponding dot to black
            if block_brightness < threshold:
                 dot_imageArray[int(y / block_size[1]), int(x / block_size[0])] = 0 # Set to '0' for black )
    return  dot_imageArray

def findLimits(array):
    maxX=None;maxY=None;minX=None;minY=None
    for p in array:
        if maxX==None or p[0]>maxX: maxX= p[0]
        if maxY==None or p[1]>maxY: maxY= p[1]
        if minX==None or p[0]<minX: minX= p[0]
        if minY==None or p[1]<minY: minY= p[1]
    return maxX, maxY, minX, minY

def find_centers_of_black_sections(image, block_size=(1, 1), threshold=128):
    # Get the dimensions of the image
    h, w = image.shape[:2]
    # List to store the centers of black sections
    black_centers = []
    # Process each block
    for y in range(0, h, block_size[1]):
        for x in range(0, w, block_size[0]):
            # Extract the block from the image
            block = image[y : y + block_size[1], x : x + block_size[0]]
            # Calculate the average brightness of the block
            block_brightness = np.mean(block)
            # If the average brightness is lower than the threshold, consider it a black section
            if block_brightness < threshold:
                # Calculate the center of the block
                center_x = x + block_size[0] / 2 - w / 2
                center_y = h / 2 - (y + block_size[1] / 2)
                center_x *= 2
                center_y *= 2
                black_centers.append((center_x, center_y))
    maxX,maxY,minX,minY=findLimits(black_centers)

    print(" number of points:",len(black_centers))
    print(" maxX:",maxX, " maxY:",maxY," minX:",minX, " minY:",minY, " rangeX:",maxX+abs(minX), " rangeY:",maxY+abs(minY))
    return black_centers


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
