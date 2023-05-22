# Template Matcher
## How the algorithm works?
1. Preprocess
    - Grayscale
    - Normalization with [CLAHE (Contrast Limited Adaptive Histogram Equalization)](https://en.wikipedia.org/wiki/Adaptive_histogram_equalization#Contrast_Limited_AHE)
    - Seperate region of interest into 3 parts
        - 0 : h/3 for foot
        - h/3 : 2h/3 for knee
        - 2h/3 : h for femoral head
    - Resize
2. Seperate 2 legs apart
    
    Turn grayscale image into sequence data by summing every columns and using peak detection algorithm to find valley between the two legs. Use that valley as breakpoint to seperate apart
    
    <p align="center">
    <img src="https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/images/tempolate_match_01.jpg" height="300">
    </p>
    
3. Template Matching
    
    Using cv2’s template matching (Normalized Correlation Coefficient, cv2.TM_CCOEFF_NORMED) and iterate template to different scaling and rotation. Find the bounding box that give the maximum confidence value.

    <p align="center">
    <img src="https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/images/tempolate_match_02.jpg" height="300">
    </p>

## Results
<p align="center">
<img src="https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/images/template_match_03.jpg" height="450">
</p>

# AutoML: Roboflow Train
- Train a machine learning model with autoML from [Roboflow Train](https://roboflow.com/) to do instance segmentation task on femoral head, end of femur, and top of tibia.
- Using pretrained weights from Microsoft COCO Dataset
- Dataset:
    - Train-Validate-Test Split [ 70:20:10 ]
        - 45 images -> 30 : 9 : 6
    - Data Augmentation:
        - Rotation, Brightness, Exposure, Blur
        - 30*3 = 90 images

## Test Results
<p align="center">
<img src="https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/images/roboflow_results.jpg" height="450">
</p>

# Segment Anything Model (SAM)
- Segmentation results for the knee area (end of femur and top of tibia) are imprecise and do not accurately depict the real shape of the bones. This may have occurred due to our limited resources in the dataset.
- To increase precision of the segmentation results from our trained model, we added another model  called SAM to our process pipeline.
- [Segment Anything Model(SAM)](https://github.com/facebookresearch/segment-anything) is a promptable foundation model for image segmentation developed by Meta AI Research, FAIR. It is trained on a very large dataset for image segmentation (11 million images and 1.1 billion masks) and is open-sourced.
- We implemented SAM by using bounding box from Roboflow train segmentation as SAM's prompt to find more precise segmentation of the bone.

<p align="center">
<img src="https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/images/sam.jpg" height="300">
</p>

## Test Results
<p align="center">
<img src="https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/images/sam_results.jpg" height="450">
</p>