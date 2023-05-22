# Knee Algorithm: Find interetibial spine
## How the algorithm works?
1. Receive a 2-dimensional mask from SAM.
2. Find the index (idx) of the first dimension that has the maximum width (W) of the mask.
3. Loop through the first dimension to find the index (i, j) of the top of the mask.
4. Define the region of interest (RoI) as mask[i:idx, j-(W//4):j+(W//4)].
5. Find the peak of the RoI. If there is only one peak, the answer is the peak's index.
6. If there are two peaks, calculate the mean of the x-dimension of the two peaks. Keeping the x-dimension fixed, loop through the y-dimension until it reaches the mask.

<p align="center">
<img src="https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/images/intertibial.jpg" height="450">
</p>