from Detector import getAnkle, getRFSegment, getBoxesfromPred
from Ankle import getAnklePoint
from Hip import getCircle
import cv2
from roboflow import Roboflow
from segment_anything import sam_model_registry, SamPredictor
import torch
from kneeBottom import check_peak, check_row, find_tibia_point

# load .env
import os
from dotenv import load_dotenv
load_dotenv()
roboflow_api_key = os.getenv("roboflow_api_key")

IMAGE_PATH = "dev/001.jpg"

image = cv2.imread(IMAGE_PATH)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_result = image_rgb.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
left_ankle, left_pos, right_ankle, right_pos = getAnkle(image)

# point left ankle
left_ankle_point = getAnklePoint(left_ankle)
left_ankle_point = (left_ankle_point[0] + left_pos[0], left_ankle_point[1] + left_pos[1]) # y,x
cv2.circle(image_result, (left_ankle_point[1], left_ankle_point[0]), 5, [0,0,255], 5)

# point right ankle
right_ankle_point = getAnklePoint(right_ankle)
right_ankle_point = (right_ankle_point[0] + right_pos[0], right_ankle_point[1] + right_pos[1]) # y,x
cv2.circle(image_result, (right_ankle_point[1], right_ankle_point[0]), 5, [0,0,255], 5)

# Roboflow
rf = Roboflow(api_key=roboflow_api_key)
project = rf.workspace().project("femoral_head_segmentation")
rf_model = project.version(2).model

# SAM
print("loading SAM...")
sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
# print("CUDA is available:", torch.cuda.is_available())
# if torch.cuda.is_available():
    # sam.to(device="cuda")
sam.to(device="cpu")
sam_model = SamPredictor(sam)
sam_model.set_image(image_rgb)

pred_hip, pred_kneeTop, pred_kneeBottom = getRFSegment(rf_model, IMAGE_PATH)

# point hip
left_center, left_circle, right_center, right_circle = getCircle(pred_hip)
## left hip
cv2.circle(image_result,(left_center[1],left_center[0]), int(left_circle[1]), (0,0,255),2)
cv2.circle(image_result,(left_center[1],left_center[0]),2,(0,0,255),3)

## right hip
cv2.circle(image_result,(right_center[1],right_center[0]), int(right_circle[1]), (0,0,255),2)
cv2.circle(image_result,(right_center[1],right_center[0]),2,(0,0,255),3)

# point kneeTop
bboxes_kt = getBoxesfromPred(pred_kneeTop)
for box in bboxes_kt:
    masks, scores, logits = sam_model.predict(
          box=box,
          multimask_output=False
      )
    # TODO: getPoint(masks[0])

# point kneeBottom
bboxes_kb = getBoxesfromPred(pred_kneeBottom)
kneeBot = []
for box in bboxes_kb:
    masks, scores, logits = sam_model.predict(
          box=box,
          multimask_output=False
      )
      # TODO: getPoint(masks[0])
    y,x = find_tibia_point(masks[0])
    # print(y,x)
    cv2.circle(image_result,(x,y),2,(0,0,255),3)
    kneeBot.append([x,y])
kneeBot.sort()
left_bot_knee = kneeBot[0]
right_bot_knee = kneeBot[1]
print("Success")
cv2.imwrite("result.jpg", image_result)