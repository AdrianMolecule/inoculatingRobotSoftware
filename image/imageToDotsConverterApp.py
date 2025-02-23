import tkinter as tk
from tkinter import Menu
import os
import sys
from pathlib import Path
from tkinter import filedialog, messagebox
import cv2 
import numpy as np 
import cv2 
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image

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
        self.textbox.insert(0, "5") 
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
        filePath = filedialog.askopenfilename(title="Open Image", initialdir=getInitialPath(), filetypes=[("Png file", "*.png"), ("All Files", "*.*")])  	
        rootPath=os.path.dirname(filePath)
        if filePath:
            try:
                print("loading",filePath)
                blockDim=int(self.textbox.get()) #change here for higher/lower number of points
                image = cv2.imread(filePath) ;   
                #image = cv2.imread("C:/a/diy/pythonProjects/labRobot/src/image/leaf.png") ;    blockDim=6#12
                adrian_block_size=(blockDim,blockDim) #6 and 6 is the best but image is 2 pixel too large
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Grayscale Maybe ConvertColor?
                if self.checkboxVar.get():
                    edged = cv2.Canny(gray, 30, 200) # Find Canny edges
                    # Finding Contours # Use a copy of the image e.g. edged.copy() # since findContours alters the image 
                    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) ##cv2.imshow('Canny Edges After Contouring', edged) 
                    print("Number of Contours found = " + str(len(contours))) # Draw all contours # -1 signifies drawing all contours # cv2.drawContours(image, contours, -1, (0, 255, 0), 3) 
                    # cv2.imshow('Contours', image) # cv2.waitKey(0) 
                    h, w = image.shape[:2]
                    contourArray = np.full((h,w),255, dtype=np.uint8) #255 is white empty image just an array of numbers
                    cv2.drawContours(contourArray, contours, -1, (0, 255, 0), 3)    
                    dotArray = createDotImageOpencv(contourArray, adrian_block_size)# Call the function to create and save the dot image
                else:
                    dotArray = createDotImageOpencv(gray, adrian_block_size)# Call the function to create and save the dot image
                black_centers = find_centers_of_black_sections(dotArray)# Call the function to find centers of black sections
                self.textboxPointsNumber.config(state="normal")
                self.textboxPointsNumber.delete(0, tk.END)
                self.textboxPointsNumber.insert(tk.END, str(len(black_centers)))    
                self.textboxPointsNumber.config(state="readonly")                  
                x_coords = [point[0] for point in black_centers]# Extract the x and y coordinates from the list of centers
                y_coords = [point[1] for point in black_centers]
                plt.figure(figsize=(8, 8))# Plot the points using plt.scatter
                plt.scatter(x_coords, y_coords, c="black")
                h, w = dotArray.shape[:2] # Set the axis limits to the size of the image
                plt.xlim(-w, w)
                plt.ylim(-h, h)
                plt.title(f"There are {len(black_centers)} points. Adjust the blocksize up if you want less points.")
                plt.gca().set_aspect("equal", adjustable="box")# Set the aspect of the plot to be equal
                print (findLimits(black_centers))
                dotArrayPath=rootPath+"/dotarray.npy"
                np.save(dotArrayPath,black_centers)
                arr=np.load(dotArrayPath)
                print (findLimits(arr))
                fig = plt.gcf()
                fig.canvas.manager.window.title(dotArrayPath)            
                plt.show()# Display the plot 
                # Call the center window function after plotting
                centerWindowHorizontally(fig)    
                messagebox.showinfo("dotArrany.npy saved", f"The dotArrany.npy file containing all the coordinates of the points relative to the center of the image was saved   as {dotArrayPath}")            
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while reading the file: {e}")
        return None,None

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
    maxX=0;maxY=0;minX=0;minY=0
    for p in array:
        if p[0]>maxX: maxX= p[0]
        if p[1]>maxY: maxY= p[1]
        if p[0]<minX: minX= p[0]
        if p[1]<minY: minY= p[1]
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


root = tk.Tk()
app = UiApp(root)
root.mainloop()
