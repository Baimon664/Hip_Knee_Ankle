# Automated measurement of hip–knee–ankle angle in total knee arthroplasty using image-based raptor assistance
### Advisors

Assoc. Prof. Dr. Thanarat Chalidabhongse

### Team Members

Nutchapol Winmoon 6231320321 

Wichaphon Kiattisin 6231357621 

Taechit Phowthongbutr 6231324921

Perasit Suebchat 6231344421

# Problem Statement
Find these following:
- Hip–Knee–Ankle angle (HKA)
- Mose circle
- Femoral mechanical axis
- Tibial mechanical axis 

from the lower limb radiograph images using computer vision technique.

<p align="center">
<img src="https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/images/problem_statement.jpg" height="600">
</p>

To find all of these we need to figure out the following points in the images:
1. Mose circle or Hip center
2. Distal Femur sulcus
3. Intertibial spine
4. Upper midpoint of talus

<p align="center">
<img src="https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/images/problem_statement_2.jpg" height="450">
</p>

# Technical Challenges
- Small Dataset (<50 Images)
- Required expert domain knowledge

# Related Works
Kamil Kwolek, Measuring Lower Limb Alignment and Joint Orientation Using Deep Learning Based Segmentation of Bones (2019) ([link to publication](https://www.researchgate.net/publication/336345786))

This work presented a deep learning approach to measuring lower limb alignment and joint orientation using an U-Net based neural architecture to segment the bones with only fifty annotated X-ray images. This experiments demonstrated that the experimental results are promising and the proposed approach has a potential.

# Method and Results

<p align="center">
<img src="https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/images/pipeline.jpg" height="450">
</p>

1. [Template Matching](https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/Detector#template-matcher)
2. [AutoML: Roboflow Train](https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/Detector#automl-roboflow-train)
3. [Segment Anything Model (SAM)](https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/Detector#segment-anything-model-sam)
4. [Hip Algorithm: Find Mose Circle](https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/Hip)
5. [Knee Algorithm: Find distal femur sulcus](https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/topKnee#knee-algorithm-find-distal-femur-sulcus)
6. [Knee Algorithm: Find interetibial spine](https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/kneeBottom#knee-algorithm-find-interetibial-spine)
7. [Ankle Algorithm: Find upper midpoint of talus](https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/Ankle#ankle-algorithm-find-upper-midpoint-of-talus)

# Future Works:
- Gather more dataset and labels to increase precision of the model
- Transfer the results to medical experts for evaluation
- Update ankle parts from traditional algorithm to ml-based model