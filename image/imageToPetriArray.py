import cv2 
import numpy as np 

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


# main image to array converter
def main():
    path="C:/a/diy/pythonProjects/labRobot/image/"
    image_path =path +"leaf.png"
    #image_path =path +"tinyobs.png"
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageInfo(gray, "gray")
    cv2.waitKey(0) 
    edged = cv2.Canny(gray, 30, 200) # Find Canny edges
    cnts,h = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    outline = np.full(gray.shape,255, dtype=np.uint8)
    cv2.drawContours(outline, cnts, -1, (0, 0, 255), 1)
    cv2.imwrite(path+"outline.png", outline)
    (thresh, blackAndWhiteImage) = cv2.threshold(outline, 254, 255, cv2.THRESH_BINARY)
    imageInfo(blackAndWhiteImage,"blackAndWhiteImage")
    # resize does not seem to get great results
    h,w=outline.shape[:2]
    r=80/h if h>w else 80/w
    resizedImage = cv2.resize(blackAndWhiteImage, (int(w*r), int(h*r))) #width/height
    imageInfo(resizedImage,"resizedImage")
    cv2.imwrite(path+"resizedImage.png", outline)
    cv2.imshow('resized_image', resizedImage)
    cv2.waitKey(0)

    # final part
    centeredDotArray=createPetriStyleArray(resizedImage)
    print("Limits:",findLimits(centeredDotArray), "points", len(centeredDotArray))
    np.save("C:/a/diy/pythonProjects/labRobot/image/dotarray",centeredDotArray)
    #recover the image from the centeredArray
    petriStyleImageArray=np.load("C:/a/diy/pythonProjects/labRobot/image/dotarray.npy")
    height,width=resizedImage.shape[:2]
    showImageFromPetriStyleArray(petriStyleImageArray, height, width)

main()