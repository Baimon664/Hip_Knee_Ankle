import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

def line_slope(x_1,y_1,x_2,y_2):
    if(y_1 == y_2):
        return 0
    return abs((y_2 - y_1) / (x_2 - x_1))

def filter_line(lines):
    a = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if( x2 == x1):
            continue
        slope = (y2 - y1) / (x2 - x1)
        if(abs(slope) < 0.5):
            a.append(line)
    return a

def select_line_slope(lines):
    select_line = lines[0][0]
    for line in lines[1:]:
        x1, y1, x2, y2 = select_line
        x3, y3, x4, y4 = line[0]
        if(x3==x4):
            continue
        if(line_slope(x3,y3,x4,y4) < line_slope(x1,y1,x2,y2)):
            # if(slope(x3,y3,x4,y4) - slope(x1,y1,x2,y2) < 0.005):
            if(line_slope(x1,y1,x2,y2) - line_slope(x3,y3,x4,y4) < 0.4): # old 0.05
                if(math.dist([x1,y1],[x2,y2]) - 10 > math.dist([x3,y3],[x4,y4])):
                    continue
            select_line = line[0]
        else:
            if(line_slope(x3,y3,x4,y4) - line_slope(x1,y1,x2,y2) < 0.4):
                if(math.dist([x3,y3],[x4,y4]) - 10 > math.dist([x1,y1],[x2,y2])):
                    select_line = line[0]
    return select_line

def midpoint(p1, p2):
    return (p1+p2)/2  

def getAnklePoint(img):
    """
    Get Ankle point in image
    
    Args:
        img (numpy array): A grayscale ankle image
 
    Returns:
        tuple of int: position of ankle point
    """

    th = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,31,5)
    ankle = cv2.medianBlur(th,7)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
    ankle_erosoion = cv2.erode(ankle,kernel,iterations = 1)

    lines = cv2.HoughLinesP(ankle_erosoion, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=1)

    filtered_lines = filter_line(lines)

    if(len(filtered_lines) == 0):
        kernel = np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]], dtype=np.uint8)
        knee_dilate = cv2.dilate(ankle_erosoion,kernel,iterations = 1)
        lines = cv2.HoughLinesP(knee_dilate, 1, np.pi/180, threshold=50, minLineLength=20, maxLineGap=1) # old theta np.pi/180
        filtered_lines = filter_line(lines)
    
    selected_line = select_line_slope(filtered_lines)
    x1, y1, x2, y2 = selected_line
    m = midpoint(np.array([x1,y1]), np.array([x2,y2]))

    return (int(m[1]), int(m[0]))