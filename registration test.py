# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 23:18:30 2023

@author: eliob
"""

import cv2
import numpy as np


def registration_pixels(img1, img2):
    # Convert images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Convert grayscale images to float32 format
    gray1_float = np.float32(gray1)
    gray2_float = np.float32(gray2)

    # Calculate phase correlation
    (dx, dy), _ = cv2.phaseCorrelate(gray1_float, gray2_float)

    # Get image size
    height, width = img1.shape[:2]

    # Calculate number of pixels mapped in X and Y directions
    num_pixels_x = dx
    num_pixels_y = dy

    return num_pixels_x, num_pixels_y

# Load images
img = cv2.imread('dots.png')

img1 = img[0:900,0:900]
img2 = img[124:1024,124:1024]

# Perform image registration and get number of pixels mapped
num_pixels_x, num_pixels_y = registration_pixels(img1, img2)

# Print results
print("Number of pixels mapped in X direction:", num_pixels_x)
print("Number of pixels mapped in Y direction:", num_pixels_y)