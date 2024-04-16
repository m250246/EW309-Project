import cv2
import datetime 
import os
import math
import EW309_YOLOv8_cpu as EW309 # Adds class to perform NN detection/display

RANGE = 10 #FEET
TARGETS = "yellow" #orange, yellow
FT_DIAMETER = 5 /12 #10, 15 INCHES -> FEET

PX_WIDTH = 1920 # image pixel width size
FOV_FEET = 2*RANGE*math.tan(math.radians(69)/2)
PX_FT_RATIO = PX_WIDTH/FOV_FEET
PX_DIAMETER = round(FT_DIAMETER*PX_FT_RATIO) #rounded number of pixels
PX_RANGE = PX_DIAMETER / 5

# onnx model and yaml file file
path_to_model = r'G:\My Drive\EW309_CV\YOLO_Output_3_28_1914\yolov8s_EW309.onnx' # path to .onnx weights
path_to_yaml = r'G:\My Drive\EW309_CV\data.yaml' # path to data.yaml file used to train the model 
conf_thres = 0.15 # classification confidence threshold, 0.0-1.0
iou_thres = 0.15 # iou threshold, 0.0-1.0

# Set up window
windowName = 'IMAGE TEST'
windowSize = (640,480)#(1920, 1080) # Maintain aspect ratio (16:9) 

    # Create output window
cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
cv2.resizeWindow(windowName, windowSize[0], windowSize[1])
img = cv2.imread("sending_angles/still_image_20.jpg")

# Instantiate YOLOv8 object
detect=EW309.YOLOv8(path_to_model,path_to_yaml,[],conf_thres,iou_thres)

# Get the center of the frame
height, width, _ = img.shape
center_x = int(width / 2)
center_y = int(height / 2)

# Perform inference
detect.input_image = img
out_img = detect.CPUinference()
if detect.nn:
    detected_data = sorted(detect.nn, key=lambda x: (x[0], min(x[1])))
    for item in detected_data:
        if item[0].lower() == TARGETS:
            print(f'{item}')
# Draw horizontal line
cv2.line(img, (0, center_y), (width, center_y), (0, 255, 0), 2)
# Draw vertical line
cv2.line(img, (center_x, 0), (center_x, height), (0, 255, 0), 2)
# Draw circle
cv2.circle(img, (center_x, center_y), 10, (0,0,255), 1)
# Display 
cv2.imshow(windowName, img)
cv2.waitKey(0)
print("EXIT and DONE")