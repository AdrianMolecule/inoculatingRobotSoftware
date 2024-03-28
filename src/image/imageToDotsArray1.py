import cv2 
import numpy as np 
import matplotlib.pyplot as plt



def create_dot_image_opencv(image, block_size, threshold=128):
    h, w = image.shape[:2] # Get the dimensions of the image
    # Calculate the number of blocks
    w_blocks = w / block_size[0]
    h_blocks = h / block_size[1]
    # Create a new image for the dots, initializing to white
    dot_image = np.full((int(h_blocks)+1, int(w_blocks)+1), int(255), np.uint8)  # '255' for white in a 1-channel image
    # Process each block
    for y in range(0, h, block_size[1]):
        for x in range(0, w, block_size[0]):
            # Extract the block from the image
            block = image[y : y + block_size[1], x : x + block_size[0]]
            # Calculate the average brightness of the block
            block_brightness = np.mean(block)
            # If the average brightness is lower than the threshold, set the corresponding dot to black
            if block_brightness < threshold:
                 dot_image[int(y / block_size[1]), int(x / block_size[0])] = 0 # Set to '0' for black )
    return dot_image

def createCenteredDotArray(image):
    h, w = image.shape[:2]
    black_dots = []
    # Process each block
    for y in range(0, h):
        for x in range(0, w):
            if image[y,x]==0:
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

path="C:/a/diy/pythonProjects/labRobot/src/image/"
image_path =path +"leaf.png"
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray', gray)
imageInfo(gray, "gray")
cv2.waitKey(0) 
edged = cv2.Canny(gray, 30, 200) # Find Canny edges
cnts,h = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#cnts = cnts[0] if len(cnts) == 1 else cnts[1]
#outline= np.ones(gray.shape, dtype=np.uint8) * 255
outline = np.full(gray.shape,255, dtype=np.uint8)

# for c in cnts:
# cv2.drawContours(outline, [c], -1, (0, 0, 0), thickness=1)
cv2.drawContours(outline, cnts, -1, (0, 0, 255), 1)
cv2.imwrite(path+"outline.png", outline)
imageInfo(outline,"outline")
# cv2.imshow('outline', outline)
# cv2.waitKey(0) 

contourImage = cv2.imread(path +"outline.png") # Load the image using OpenCV 
# cv2.imshow('outline', contourImage)
dot_image = create_dot_image_opencv(contourImage, (1,1))# Call the function to create the dot image
# Save the dot image using OpenCV
dot_image_path = path+"dot_image.png"
cv2.imwrite(dot_image_path, dot_image)
imageInfo(dot_image,"dot_image")
# cv2.imshow('dot_image', dot_image)
# cv2.waitKey(0) 
image = cv2.imread(dot_image_path, cv2.COLOR_BGR2GRAY)
#black_centers = find_centers_of_black_sections(image, block_size=(1,1))# Call the function to find centers of black sections
centeredDotArray=createCenteredDotArray(image)

# r=80/h if h>w else 80/w
# resizedImage = cv2.resize(image, (int(w*r), int(h*r))) #width/height
# imageInfo(resizedImage,"resizedImage")
# cv2.imshow('resized_image', resizedImage)
# cv2.waitKey(0)

print("Limits:",findLimits(centeredDotArray), "points", len(centeredDotArray))
np.save("C:/a/diy/pythonProjects/labRobot/src/image/dotarray",centeredDotArray)
#recover the image from the centeredArray
petriStyleImageArray=np.load("C:/a/diy/pythonProjects/labRobot/src/image/dotarray.npy")
height,width=image.shape[:2]
showImageFromPetriStyleArray(petriStyleImageArray, height, width)
