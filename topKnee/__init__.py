import cv2
import numpy as np

## region ที่เป็นสีขาว
def callGetRegionInImage(image):
  # binary_mask = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)[1]
  image = np.uint8(image)
  num_labels, lebels, stats, _ = cv2.connectedComponentsWithStats(image)
  # Print the count of regions (excluding the background)
  component_width = 0
  num_regions = num_labels - 1
  if(num_regions == 1):
    component_width = stats[1, cv2.CC_STAT_WIDTH]
  # print("Count of regions:", num_regions, 'index', index)
  return num_regions,component_width


def GetBounaryImage(image, isCoordinate,isCenter):
  # Threshold the image to obtain a binary image
  image = np.uint8(image)
  # Find contours in the binary image
  contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Initialize variables for the leftmost x-coordinate
  leftmost_x = np.inf
  leftmost_x_width = 0
  rightmost_x = 0
  rightmost_x_width = 0

  # Iterate through the contours
  for contour in contours:
      # Approximate the contour to a rectangle
      x, _, width, _ = cv2.boundingRect(contour)
      # Update the leftmost x-coordinate if necessary
      if x < leftmost_x:
          leftmost_x = x
          leftmost_x_width = width
      if x + width > rightmost_x:
          rightmost_x = x
          rightmost_x_width= width
  if(isCenter):
    return (leftmost_x+rightmost_x+rightmost_x_width)/2
  if(isCoordinate):
      return (leftmost_x+leftmost_x_width+rightmost_x)/2
  return (rightmost_x+rightmost_x_width)-leftmost_x

# First case
# 1.ถ้าเจอ 1 ก่อน
# 2. หาที่มากกว่า2 เพื่อ toggle ว่าเจอ 2 แล้ว
# 2. หา 1 เอา index

# Second case
# 1. ถ้าเจอ 2 ก่อน
# 2. หา 1 เอา index



# Draw the horizontal line on the image
def getCenterTopKnee(image):
  defaultImage = image

  max_width = GetBounaryImage(defaultImage,False,False)
  print(max_width)
  image_with_line = defaultImage.copy()


  isFoundNumberNotZero = False
  case = 0
  isFoundNumberMoreThanTwo = False
  isAssginCase = False
  breaked = False
  selected_index = 0
  for i in range (defaultImage.shape[0],1,-1):
    image = defaultImage[i-1:i,:]
    regionsCount, width = callGetRegionInImage(image)
    match case:
      case 0:
        if(regionsCount == 0): pass
        if(regionsCount > 0 and isFoundNumberNotZero == False):
          isFoundNumberNotZero = True
          if(regionsCount == 1):
            case = 1
          else:
            case = 2
      case 1:
        if ( regionsCount >= 2): isFoundNumberMoreThanTwo = True
        if(isFoundNumberMoreThanTwo == True and regionsCount == 1 and width > 0.6*(max_width)): 
          selected_index= i
          print('index',i,case)
          breaked = True
          break
      case 2:
        if ( regionsCount >= 2): pass
        if (regionsCount == 1 and width > 0.6*(max_width)):
          selected_index= i
          print('index',i,case)
          breaked = True
          break

  if breaked == False:
    coordinate_x = GetBounaryImage(defaultImage,False,True)
    coordinate_y = 0
    new_image = defaultImage[:,int(coordinate_x):int(coordinate_x+1)]
    for i in range(new_image.shape[0]-1,0,-1):
      if new_image[i,0] == 1:
        coordinate_y = i
        break
    return (coordinate_y,coordinate_x)
  return selected_index+0.5,GetBounaryImage(defaultImage[selected_index:selected_index+1,:],True,False)