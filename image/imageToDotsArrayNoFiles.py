import cv2 
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image

# Now we define a function to create a ?x? dot pattern image using OpenCV
def create_dot_image_opencv(image:Image, block_size, threshold=128)->Image:
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

def main():
    # Let's load a simple image with 3 black squares 
    
    fileName="leaf1.png"#change here for new files
    blockDim=5 #change here for higher/lower number of points
    image = cv2.imread("C:/a/diy/pythonProjects/labRobot/image/"+fileName) ;   
    #image = cv2.imread("C:/a/diy/pythonProjects/labRobot/src/image/leaf.png") ;    blockDim=6#12
    adrian_block_size=(blockDim,blockDim) #6 and 6 is the best but image is 2 pixel too large
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Grayscale Maybe ConvertColor?

    edged = cv2.Canny(gray, 30, 200) # Find Canny edges
    # Finding Contours # Use a copy of the image e.g. edged.copy() # since findContours alters the image 
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) ##cv2.imshow('Canny Edges After Contouring', edged) 
    print("Number of Contours found = " + str(len(contours))) # Draw all contours # -1 signifies drawing all contours # cv2.drawContours(image, contours, -1, (0, 255, 0), 3) 
    # cv2.imshow('Contours', image) # cv2.waitKey(0) 
    h, w = image.shape[:2]
    contourArray = np.full((h,w),255, dtype=np.uint8) #255 is white empty image just anarray of numbers
    cv2.drawContours(contourArray, contours, -1, (0, 255, 0), 3)    
    dotArray = create_dot_image_opencv(contourArray, adrian_block_size)# Call the function to create and save the dot image
    black_centers = find_centers_of_black_sections(dotArray)# Call the function to find centers of black sections
    if   fileName=="mam.png":
        black_centers.append((-12, 17))
    x_coords = [point[0] for point in black_centers]# Extract the x and y coordinates from the list of centers
    y_coords = [point[1] for point in black_centers]
    plt.figure(figsize=(8, 8))# Plot the points using plt.scatter
    plt.scatter(x_coords, y_coords, c="black")
    h, w = dotArray.shape[:2] # Set the axis limits to the size of the image
    plt.xlim(-w, w)
    plt.ylim(-h, h)
    plt.gca().set_aspect("equal", adjustable="box")# Set the aspect of the plot to be equal
    print (findLimits(black_centers))
    np.save("C:/a/diy/pythonProjects/labRobot/image/dotarray",black_centers)
    arr=np.load("C:/a/diy/pythonProjects/labRobot/image/dotarray.npy")
    print (findLimits(arr))
    plt.show()# Display the plot

main()


