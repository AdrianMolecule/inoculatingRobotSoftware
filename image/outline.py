import cv2 
import numpy as np 
import matplotlib.pyplot as plt

def imageInfo(image, imageName=""):
    h,w=image.shape[:2]
    print("image "+imageName+ " dimensions",h,w, " black pixels",h*w-cv2.countNonZero(image)) # Get the dimensions of the image

path="C:/a/diy/pythonProjects/labRobot/src/image/"
imageName="obs.png.png"
image_path =path +imageName
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
imageInfo(gray, "gray")
edged = cv2.Canny(gray, 30, 200) # Find Canny edges
cnts,h = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
outline = np.full(gray.shape,255, dtype=np.uint8)
cv2.drawContours(outline, cnts, -1, (0, 0, 255), 1)
cv2.imwrite(path+imageName+".png", outline)
imageInfo(outline,imageName)
cv2.imshow('outline', outline)
cv2.waitKey(0) 