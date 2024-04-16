import cv2

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Pixel Position (x, y): ({x}, {y})")

imag = cv2.imread('./run_images/still_1.jpg')
print(imag.shape)
window_width = 800
window_height = 600

# Resize the window
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image', window_width, window_height)

# Resize the image to fit the window size
#resized_image = cv2.resize(imag, (window_width, window_height))
print(imag.shape)
cv2.imshow('Image', imag)
cv2.setMouseCallback('Image', click_event)

while cv2.waitKey(1) & 0xFF != ord('q'):
    pass

cv2.destroyAllWindows()
