# Basic camera test

import cv2

cam = cv2.VideoCapture(0)
result, image = cam.read()

if result:
    cv2.imshow("AMSCOPE", image) # show image
    cv2.imwrite("AMSCOPE.png", image) # save image
    
    cv2.waitKey(0) # press key to close window
    cv2.destroywWindow("AMSCOPE")
else:
    print("Image capture was unsuccessful")
