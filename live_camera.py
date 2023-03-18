# Basic camera test

import cv2 as cv
import matplotlib.pyplot as plt

cam = cv.VideoCapture(0)

result, image = cam.read()

if result:
    plt.imshow("AMSCOPE", image) # show image
    plt.imwrite("AMSCOPE.png", image) # save image
    
    waitKey(0) # press key to close window
    plt.destroywWindow("AMSCOPE")
else:
    print("Image capture was unsuccessful")
