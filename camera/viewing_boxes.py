import cv2
import numpy as np

data = [['Red', [273, 334, 208, 197], 0.98500437],
['Orange', [564, 402, 31, 30], 0.53845733],
['Red', [272, 334, 209, 197], 0.9848679],
['Orange', [564, 402, 32, 30], 0.5211925],
['Orange', [452, 620, 38, 38], 0.1600565]]

sorted_data = sorted(data, key=lambda x: (x[0], min(x[1])))
cv2.namedWindow('image')

# Create a black image
width = 4208
height = 3120

img = 255 * np.zeros((height, width, 3), dtype=np.uint8)

# Manual input for box coordinates
for obj in sorted_data:
    if obj[0]=="Red":
        print(obj)
        left = obj[1][0] 
        top = obj[1][1]
        right = left + obj[1][2]
        bottom = top + obj[1][3]      
        centerX = left+int(obj[1][2]/2)
        centerY = top+int(obj[1][3]/2)
        # Draw the box on the image
        cv2.circle(img, (centerX, centerY), 10, (0,0,255),1)
        cv2.rectangle(img, (left, top), (right, bottom),(0,255,0),2)
cv2.imshow('image', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
