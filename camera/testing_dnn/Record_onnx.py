# Requires OAK camera attached with USB3 cable and trained YOLO model
# depthai API vailable at: https://docs.luxonis.com/projects/api/en/latest/
# EW309 Computer Vision, P. Frontera, March 2024

import cv2
import depthai as dai
import datetime 
import os

import EW309_YOLOv8_cpu as EW309 # Adds class to perform NN detection/display

# onnx model and yaml file file
path_to_model = r'G:\My Drive\EW309_CV\YOLO_Output_3_28_1914\yolov8s_EW309.onnx' # path to .onnx weights
path_to_yaml = r'G:\My Drive\EW309_CV\data.yaml' # path to data.yaml file used to train the model 
conf_thres = 0.15 # classification confidence threshold, 0.0-1.0
iou_thres = 0.15 # iou threshold, 0.0-1.0

# Flag to toggle video recording
record = False # Use True to record; use False for no recording

# Set up window
windowName = 'OAK-1 Live Stream'
windowSize = (640,480)#(1920, 1080) # Maintain aspect ratio (16:9) 

# Create pipeline    
pipeline = dai.Pipeline()

# Define source and output 
camRgb = pipeline.createColorCamera()
xoutRgb = pipeline.createXLinkOut()

# Camera Properties
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)#THE_1080_P)
camRgb.setPreviewSize(camRgb.getVideoSize()) # must match resolution, max 4K
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
camRgb.setFps(30)

xoutRgb.setStreamName("rgb")

# Linking
camRgb.preview.link(xoutRgb.input)

# Verify OAK connected, access OAK information
try:
    print(f'Product Name: {dai.Device(pipeline).getProductName()}')
    print(f'Connected Camera(s): {dai.Device(pipeline).getConnectedCameraFeatures()}')
except:
    print('OAK Camera not connected.')
    exit()

# Start pipeline
with dai.Device(pipeline) as device:
    # Get camera information 
    calibData = device.readCalibration()
    M_row1, M_row2, M_row3  = calibData.getCameraIntrinsics(dai.CameraBoardSocket.CAM_A)
    fov = calibData.getFov(dai.CameraBoardSocket.CAM_A)
    print('Camera Intrinsic Matrix:')
    print(f'{M_row1}')
    print(f'{M_row2}')
    print(f'{M_row3}')
    print(f'Camera Horizontal FOV: {fov} deg \n')
    print('')
    
    # Queues        
    qRgb = device.getOutputQueue("rgb", 1, False) # Non-blocking

    # Create video writer
    vidSize = camRgb.getVideoSize() # Video (height, width)
 
    if record:
        # Set up folder path, assumes google drive mounted to PC
        VID_FOLDER = r"G:\My Drive\Videos"
        if not os.path.exists(VID_FOLDER):
            os.makedirs(VID_FOLDER)
        # Generate path/filename
        now = datetime.datetime.now().strftime('%m_%d_%H%M%S')
        filename = os.path.join(VID_FOLDER,'OAKvid_'+now+'.avi')
        # Create videowriter object, outputs .avi file
        out = cv2.VideoWriter(filename, cv2.VideoWriter.fourcc(*'MJPG'), 30, vidSize)

    # Create output window
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, windowSize[0], windowSize[1])

    # Instantiate YOLOv8 object
    detect=EW309.YOLOv8(path_to_model,path_to_yaml,[],conf_thres,iou_thres)

    # Global variables
    clicked = False
    image_counter = 0

    # Function to handle mouse events
    def mouse_callback(event, x, y, flags, param):
        global clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            clicked = True
    
    cv2.setMouseCallback(windowName, mouse_callback)

    print('Entering loop')
    
    while True:
        inRgb = qRgb.get() 

        if inRgb is not None:

            # Get frame
            frame = inRgb.getCvFrame()

            
            # Get the center of the frame
            height, width, _ = frame.shape
            center_x = int(width / 2)
            center_y = int(height / 2)
            
            # Draw horizontal line
            cv2.line(frame, (0, center_y), (width, center_y), (0, 255, 0), 2)
            # Draw vertical line
            cv2.line(frame, (center_x, 0), (center_x, height), (0, 255, 0), 2)
            # Draw circle
            cv2.circle(frame, (center_x, center_y), 10, (0,0,255), 1)

            # Check for mouse click event
            if clicked:
                # Save the current frame as an image with a unique file name
                image_name = f'run_images/still_{image_counter}.jpg'

                # Perform inference
                detect.input_image = frame #frame
                out_img = detect.CPUinference()
                cv2.imwrite(image_name, out_img)
                print(f"Image saved as {image_name}")
                clicked = False  # Reset the flag
                image_counter += 1  # Increment the counter

                if detect.nn:
                    for item in detect.nn:
                        print(f'{item}')

            
                # Display 
                cv2.imshow(windowName, out_img)
            # Display 
            cv2.imshow(windowName, frame)

            # Write video
            if record:
                out.write(frame)          

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release resources    
    cv2.destroyAllWindows()
    if record:
        out.release()
        print(f"Video is located at: {filename}")
    print('Complete')