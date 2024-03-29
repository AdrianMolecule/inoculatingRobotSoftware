import cv2 
import numpy as np 
  
# Let's load a simple image with 3 black squares 
path="C:/a/diy/pythonProjects/labRobot/src/image/"
image_path =path +"leaf.png"
image = cv2.imread(image_path) 
cv2.waitKey(0) 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
# Find Canny edges 
edged = cv2.Canny(gray, 30, 200) #can change here
cv2.waitKey(0) 
contours, hierarchy = cv2.findContours(edged,     cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
##cv2.imshow('Canny Edges After Contouring', edged) 
cv2.waitKey(0) 
print("Number of Contours found = " + str(len(contours))) 

contourImagePath = path+"contour.png"
h, w = image.shape[:2]
contour = np.full((h,w),255, dtype=np.uint8) #255 is white empty image just anarray of numbers
cv2.drawContours(contour, contours, -1, (0, 255, 0), 1) # -1 signifies drawing all contours, 1 is the thickness of the line
cv2.imshow('Just Cont', contour)
cv2.imwrite(contourImagePath, contour)
cv2.waitKey(0) 
cv2.destroyAllWindows() 