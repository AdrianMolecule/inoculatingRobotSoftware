import numbers as np
import csv
import cv2

# run from labrobot folder!!!
path="C:/a/diy/pythonProjects/pointImage/"
src = cv2.imread(path+'leaf.png', cv2.IMREAD_GRAYSCALE)
src = 255 - src
# convert to binary by thresholding
ret, binary_map = cv2.threshold(src,127,255,0)

# do connected components processing
nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_map, None, None, None, 8, cv2.CV_32S)

#get CC_STAT_AREA component as stats[label, COLUMN] 
areas = stats[1:,cv2.CC_STAT_AREA]

result = np.zeros((labels.shape), np.uint8)

for i in range(0, nlabels - 1):
    if areas[i] >= 100:   #keep
        result[labels == i + 1] = 255

cv2.imwrite(path+"leafPoints.png", result)


# Load the input image in grayscale
img = cv2.imread(path+'leafPoints.png', cv2.IMREAD_GRAYSCALE)

# Apply thresholding to identify the white dots
ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Find contours of the white dots
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Write the coordinates of each dot to a CSV file
with open(path+'output.csv', mode='w') as csv_file:
    fieldnames = ['x', 'y']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for cnt in contours:
        M = cv2.moments(cnt)
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])
        writer.writerow({'x': x, 'y': y})