from Detector import getAnkle, getRFSegment, getBoxesfromPred
from Ankle import getAnklePoint
from Hip import getCircle
from topKnee import getCenterTopKnee
import cv2
from roboflow import Roboflow
from segment_anything import sam_model_registry, SamPredictor
from kneeBottom import find_tibia_point
from utils import calculate_angle
import torch

# load .env
import os
from dotenv import load_dotenv
load_dotenv()
roboflow_api_key = os.getenv("roboflow_api_key")

rf_model = None
sam_model = None

def load_model():
    global rf_model, sam_model
    rf = Roboflow(api_key=roboflow_api_key)
    project = rf.workspace().project("femoral_head_segmentation")
    rf_model = project.version(2).model

    print("loading SAM...")
    sam_checkpoint = "sam_vit_b_01ec64.pth"
    model_type = "vit_b" #vit_h
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    if(torch.cuda.is_available()):
        sam.to(device="cuda")
    sam_model = SamPredictor(sam)

def get_HKA_angle(image_path):
    global rf_model, sam_model
    if(rf_model == None or sam_model==None):
        load_model()
    image = cv2.imread(image_path)
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
    # rf = Roboflow(api_key=roboflow_api_key)
    # project = rf.workspace().project("femoral_head_segmentation")
    # rf_model = project.version(2).model

    # SAM
    # print("loading SAM...")
    # sam_checkpoint = "sam_vit_b_01ec64.pth"
    # model_type = "vit_b" #vit_h
    # sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    # if(torch.cuda.is_available()):
    #     sam.to(device="cuda")
    # sam_model = SamPredictor(sam)

    sam_model.set_image(image_rgb)

    pred_hip, pred_kneeTop, pred_kneeBottom = getRFSegment(rf_model, image_path)

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


    topKnee = []
    for box in bboxes_kt:
        masks, scores, logits = sam_model.predict(
            box=box,
            multimask_output=False
        )
        # TODO: getPoint(masks[0])
        #left
        coordinate = getCenterTopKnee(masks[0])
        topKnee.append(coordinate)
        cv2.circle(image_result, (int(coordinate[1]), int(coordinate[0])), 5, [0,0,255], 5)
    left_top_knee = min(topKnee, key=lambda x:x[1])
    right_top_knee = max(topKnee, key=lambda x:x[1])
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
        cv2.circle(image_result, (int(x), int(y)), 5, [0,0,255], 5)
        kneeBot.append([y,x])
    kneeBot.sort(key=lambda x:x[1])
    left_bot_knee, right_bot_knee = kneeBot

    cv2.line(image_result, (left_center[1],left_center[0]), (int(left_top_knee[1]), int(left_top_knee[0])), [0,0,255], 5) 
    cv2.line(image_result, (right_center[1],right_center[0]), (int(right_top_knee[1]), int(right_top_knee[0])), [0,0,255], 5) 

    cv2.line(image_result, (left_bot_knee[1],left_bot_knee[0]), (int(left_ankle_point[1]), int(left_ankle_point[0])), [0,0,255], 5) 
    cv2.line(image_result, (right_bot_knee[1],right_bot_knee[0]), (int(right_ankle_point[1]), int(right_ankle_point[0])), [0,0,255], 5) 

    left_angle = 180 + calculate_angle(left_center[1], left_center[0], left_top_knee[1], left_top_knee[0], left_bot_knee[1], left_bot_knee[0], left_ankle_point[1], left_ankle_point[0]) 
    right_angle = 180 - calculate_angle(right_center[1], right_center[0], right_top_knee[1], right_top_knee[0], right_bot_knee[1], right_bot_knee[0], right_ankle_point[1], right_ankle_point[0])
    # print("left:",left_angle)
    # print("right:",right_angle)

    cv2.putText(image_result, str(round(left_angle,3)), (int(left_top_knee[1]) + 20, int(left_top_knee[0])),cv2.FONT_HERSHEY_SIMPLEX, 2, [255,255,0], 5)
    cv2.putText(image_result, str(round(right_angle,3)), (int(right_top_knee[1]) - 300, int(right_top_knee[0])),cv2.FONT_HERSHEY_SIMPLEX, 2, [255,255,0], 5)

    # print("Success")
    return image_result