import cv2 
import numpy as np 
import matplotlib.pyplot as plt
  
# Let's load a simple image with 3 black squares 
path="C:/a/diy/pythonProjects/labRobot/src/image/"
image_path =path +"leaf.png"
image = cv2.imread(image_path) 
adrian_block_size=(6,6)
cv2.waitKey(0) 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Grayscale 
edged = cv2.Canny(gray, 30, 200) # Find Canny edges
cv2.waitKey(0) 
# Finding Contours # Use a copy of the image e.g. edged.copy() # since findContours alters the image 
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) ##cv2.imshow('Canny Edges After Contouring', edged) 
cv2.waitKey(0) 
print("Number of Contours found = " + str(len(contours))) # Draw all contours # -1 signifies drawing all contours # cv2.drawContours(image, contours, -1, (0, 255, 0), 3) 
# cv2.imshow('Contours', image) # cv2.waitKey(0) 
contourImagePath = path+"contour.png"
h, w = image.shape[:2]
contour = np.full((h,w),255, dtype=np.uint8) #255 is white empty image just anarray of numbers
cv2.drawContours(contour, contours, -1, (0, 255, 0), 3) 
cv2.imshow('Just Cont', contour)
cv2.imwrite(contourImagePath, contour)
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Now we define a function to create a 32x32 dot pattern image using OpenCV
def create_dot_image_opencv(image, block_size, threshold=128):
#def create_dot_image_opencv(image, block_size=(26, 26), threshold=128):
    # Get the dimensions of the image
    h, w = image.shape[:2]
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
    # Save the dot image using OpenCV
    dot_image_path = path+"dot_image.png"
    cv2.imwrite(dot_image_path, dot_image)
    return  dot_image_path

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
    maxX=0;maxY=0;minX=0;minY=0
    for p in black_centers:
        if p[0]>maxX: maxX= p[0]
        if p[1]>maxY: maxY= p[1]
        if p[0]<minX: minX= p[0]
        if p[1]<minY: minY= p[1]
    print(" number of points:",len(black_centers))
    print(" maxX:",maxX, " maxY:",maxY," minX:",minX, " minY:",minY, " rangeX:",maxX+abs(minX), " rangeY:",maxY+abs(minY))
    return black_centers

# LAST PART
contourImage = cv2.imread(path +"contour.png") # Load the image using OpenCV 
dot_image_path = create_dot_image_opencv(contourImage, adrian_block_size)# Call the function to create and save the dot image
image = cv2.imread(dot_image_path, cv2.IMREAD_COLOR)
grayDotsImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# Convert the image to grayscale using OpenCV
black_centers = find_centers_of_black_sections(grayDotsImage)# Call the function to find centers of black sections

x_coords = [point[0] for point in black_centers]# Extract the x and y coordinates from the list of centers
y_coords = [point[1] for point in black_centers]


plt.figure(figsize=(8, 8))# Plot the points using plt.scatter
plt.scatter(x_coords, y_coords, c="black")

# Set the axis limits to the size of the image
h, w = grayDotsImage.shape[:2]
plt.xlim(-w, w)
plt.ylim(-h, h)

# Set the aspect of the plot to be equal
plt.gca().set_aspect("equal", adjustable="box")

# Display the plot
plt.show()


