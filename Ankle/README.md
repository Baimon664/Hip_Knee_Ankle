# Ankle Algorithm: Find upper midpoint of talus
## How the algorithm works?
1. Threshold the cropped ankle image recieved from template matching
2. Apply erosion on the threshold image
3. Using Houghline to detect every line in the image
4. Finding the longest line that have a low angle
5. Calculate the middle point of the selected line
6. Draw a point on an input image.

<p align="center">
<img src="https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/images/ankle.jpg" height="450">
</p>