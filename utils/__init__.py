import math
import cv2

def calculate_angle(x1, y1, x2, y2, x3, y3, x4, y4):
    # Calculate the slopes of the lines
    slope1 = (y2 - y1) / (x2 - x1)
    slope2 = (y4 - y3) / (x4 - x3)
    
    # Calculate the angle between the lines
    angle = math.atan((slope2 - slope1) / (1 + slope1 * slope2))
    
    # Convert the angle to degrees
    angle_degrees = math.degrees(angle)

    # if angle_degrees < 90 or angle_degrees > 270:
    #     angle_degrees = (angle_degrees + 180) % 360

    if( angle_degrees - 180 >= 0):
        return 360 - angle_degrees
    
    return angle_degrees

# # Example usage
# x1, y1 = -0.3, 1
# x2, y2 = 0, 0
# x3, y3 = 0.15, -1
# x4, y4 = 0, 0

# angle = calculate_angle(x1, y1, x2, y2, x3, y3, x4, y4)
# print(f"The angle between the lines is {angle} degrees.")

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized