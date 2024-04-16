# import the opencv library 
import cv2 as cv
import numpy as np

# define a video capture object
vid = cv.VideoCapture(0)

while True:

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv.imshow('frame', frame)

    # setting values for base colors
    b = frame[:, :, :1]
    g = frame[:, :, 1:2]
    r = frame[:, :, 2:]

    # computing the mean
    b_mean = np.mean(b)
    g_mean = np.mean(g)
    r_mean = np.mean(r)

    # displaying the most prominent color
    if b_mean > g_mean and b_mean > r_mean:
        print("Blue")
    if g_mean > r_mean and g_mean > b_mean:
        print("Green")
    else:
        print("Red")

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object 
vid.release()
# Destroy all the windows 
cv.destroyAllWindows()