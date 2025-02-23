import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image using OpenCV
path="C:/a/diy/pythonProjects/labRobot/src/image/"
#image_path =path +"leaf.png"
outline=True
image_path =path +"leaf.png"
adrian_block_size=(13, 13)
image = cv2.imread(image_path, cv2.IMREAD_COLOR)
cv2.imshow("image", image)
# Convert the image to grayscale using OpenCV\
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Save the grayscale image using OpenCV
gray_image_path = path+"grayImage.png"
cv2.imwrite(gray_image_path, gray_image)

# Now we define a function to create a 32x32 dot pattern image using OpenCV
def create_dot_image_opencv(image, block_size=adrian_block_size, threshold=128):
#def create_dot_image_opencv(image, block_size=(26, 26), threshold=128):
    # Get the dimensions of the image
    h, w = image.shape[:2]

    # Calculate the number of blocks
    w_blocks = w / block_size[0]
    h_blocks = h / block_size[1]

    # Create a new image for the dots, initializing to white
    dot_image = np.full((int(h_blocks), int(w_blocks)), int(255), np.uint8)  # '255' for white in a 1-channel image

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

    return gray_image_path, dot_image_path

# Call the function to create and save the dot image
gray_image_path, dot_image_path = create_dot_image_opencv(gray_image)


def find_centers_of_black_sections(image, block_size=(1, 1), threshold=128):
    # Get the dimensions of the image
    h, w = image.shape[:2]
    # List to store the centers of black sections
    black_centers = []
    # Process each block
    lastWasBlack=False
    lastSkippedBlackX=0
    lastSkippedBlackY=0
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
                if not outline:
                    black_centers.append((center_x, center_y)) 
                else:
                    if lastWasBlack==False:
                        black_centers.append((center_x, center_y))
                        lastWasBlack=True
                    else:
                        lastSkippedBlackX=center_x; lastSkippedBlackY=center_y
            else: #it's white
                if lastWasBlack and outline:                    
                    black_centers.append((lastSkippedBlackX,lastSkippedBlackY))
                lastWasBlack=False
    print(" number of points:",len(black_centers))

    return black_centers


# Load the image using OpenCV
image_path = dot_image_path
image = cv2.imread(image_path, cv2.IMREAD_COLOR)

# Convert the image to grayscale using OpenCV
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Call the function to find centers of black sections
black_centers = find_centers_of_black_sections(gray_image)


# Extract the x and y coordinates from the list of centers
x_coords = [point[0] for point in black_centers]
y_coords = [point[1] for point in black_centers]

# Plot the points using plt.scatter
plt.figure(figsize=(8, 8))
plt.scatter(x_coords, y_coords, c="black")

# Set the axis limits to the size of the image
h, w = gray_image.shape[:2]
plt.xlim(-w, w)
plt.ylim(-h, h)

# Set the aspect of the plot to be equal
plt.gca().set_aspect("equal", adjustable="box")

# Display the plot
plt.show()