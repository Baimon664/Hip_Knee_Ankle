from Detector import getAnkle
from Ankle import getAnklePoint
import cv2

image = cv2.imread("dev/001.jpg")
imgae_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
left_ankle, left_pos, right_ankle, right_pos = getAnkle(image)

# point left ankle
left_ankle_point = getAnklePoint(left_ankle)
left_ankle_point = (left_ankle_point[0] + left_pos[0], left_ankle_point[1] + left_pos[1]) # y,x
imgae_RGB = cv2.circle(imgae_RGB, (left_ankle_point[1], left_ankle_point[0]), 5, [0,0,255], 5)

# point right ankle
right_ankle_point = getAnklePoint(right_ankle)
right_ankle_point = (right_ankle_point[0] + right_pos[0], right_ankle_point[1] + right_pos[1]) # y,x
imgae_RGB = cv2.circle(imgae_RGB, (right_ankle_point[1], right_ankle_point[0]), 5, [0,0,255], 5)

cv2.imwrite("ankle.jpg", imgae_RGB)