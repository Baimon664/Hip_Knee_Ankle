import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from .utils.preprocess import preprocess
from .utils.peakDetect import getBreakpoint
from .utils.templateMatcher import templateMatcher, rotate_image

# Set parameters
## Templates
template_left_path = './Detector/templates/template_talus_left.jpg'
template_right_path = './Detector/templates/template_talus_right.jpg'

## Template scaling
min_scale = 0.9
max_scale = 1.1
scale_step = 0.1

## Template rotating angles
min_angle = -45
max_angle = 45
angle_step = 15

def getAnkle(img):
    """
    Get Left and Right Ankle image with position
    
    Args:
        img (numpy array): A grayscale image
 
    Returns:
        nunpy array: left ankle image
        tuple of float: top left position of left ankle image (y,x)
        nunpy array: right ankle image
        tuple of float: top left position of right ankle image (y,x)
    """
    

    # Preprocess
    resized = (1024,1024)
    img_prep = preprocess(img, resized, region="low")

    # Get breakpoints for left and right legs
    bp = getBreakpoint(img_prep)

    # Template Matching: Left image
    template_left = cv2.imread(template_left_path, cv2.IMREAD_GRAYSCALE)
    img_left = img_prep[:,:bp]
    x, y, w, h, angle = templateMatcher(img_left,
                                    template_left,
                                    scales=np.arange(min_scale, max_scale+scale_step, scale_step),
                                    angles=np.arange(min_angle, angle_step+1, angle_step),
                                    )
    
    ## scale back
    [x,y,w,h] = np.array([x,y,w,h]) * img.shape[1] // resized[0] 
    y += img.shape[0]-img.shape[1]

    left_ankle = img[y:y+h,x:x+w]
    left_position = (y,x)

    # Template Matching: Right image
    template_right = cv2.imread(template_right_path, cv2.IMREAD_GRAYSCALE)
    img_right = img_prep[:,bp:]
    x, y, w, h, angle = templateMatcher(img_right,
                                template_right,
                                scales=np.arange(min_scale, max_scale+scale_step, scale_step),
                                angles=np.arange(-1*angle_step, max_angle+1, angle_step),
                                )
    x += bp
    ## scale back
    [x,y,w,h] = np.array([x,y,w,h]) * img.shape[1] // resized[0] 
    y += img.shape[0]-img.shape[1]

    right_ankle = img[y:y+h,x:x+w]
    right_position = (y,x)

    return left_ankle, left_position, right_ankle, right_position
    