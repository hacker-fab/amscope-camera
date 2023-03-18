# Basic camera test

import cv2 as cv

cam = cv.VideoCapture(0)
result, image = cam.read()

if result:
    cv.imshow("AMSCOPE", image) # show image
    cv.imwrite("AMSCOPE.png", image) # save image
    
    cv.waitKey(0) # press key to close window
    cv.destroywWindow("AMSCOPE")
else:
    print("Image capture was unsuccessful")
