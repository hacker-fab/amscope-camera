# program to capture single image from webcam in python

# importing OpenCV library
import cv2 as cv

def take_photo():
    # initialize the camera
    # If you have multiple camera connected with
    # current device, assign a value in cam_port
    # variable according to that
    cam_port = 0
    cam = cv.VideoCapture(cam_port)

    # reading the input using the camera
    result, image = cam.read()

    # If image will detected without any error,
    # show result
    if result:

        # showing result, it take frame name and image
        # output
        imshow("AMSCOPE", image)

        # saving image in local storage
        imwrite("AMSCOPE.png", image)

        # If keyboard interrupt occurs, destroy image
        # window
        waitKey(0)
        destroyWindow("AMSCOPE")

    # If captured image is corrupted, moving to else part
    else:
        print("No image detected. Please! try again")

take_photo()