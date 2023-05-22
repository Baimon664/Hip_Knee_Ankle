# Knee Algorithm: Find distal femur sulcus
## How the algorithm works?
1. The input is a mask.
2. Send the mask into a function.
3. Find the maximum weight in the image.
4. Split the mask by index and find the first part that has a value equal to 
5. Assign a case number to identify it based on the count of regions.

    5.1 Case 1:
    - Find the value that is equal to 1 and has an index with a count of 1 region.
    - Find the first index that has a count of 2 regions.
    - Find the number of regions that equal 
    - Find the index where the number of regions equals 1 and the width of the row is more than 60% of the maximum width.
    - Save the index (coordinate-y).
    - Find the coordinate-x by splitting the image from the coordinate-y and the center between two regions (left and right).
    - In the left part, find the rightmost point (x1).
    - In the right part, find the leftmost point (x2).
    - Save the coordinate-x as (x1 + x2)/2.
    
    5.2 Case 2:
    - Find the value that is equal to 1 and has an index with a count of 2 regions.
    - Find the first index that has a count of 1 region and the width of the row is more than 60% of the maximum width.
    - Save the index (coordinate-y).
    - Find the coordinate-x by splitting the image from the coordinate-y and the center between two regions (left and right).
    - In the left part, find the rightmost point (x1).
    - In the right part, find the leftmost point (x2).
    - Save the coordinate-x as (x1 + x2)/2.

    5.3 Other cases:
    1. Find the largest contour and determine the leftmost, rightmost, topmost, and bottommost points.
    2. Divide the sum of the rightmost and leftmost points by 2.
    3. Find the first value equal to 1 in the coordinate-y (from bottommost to topmost) and coordinate-x equal to the value from step 1.5.3.2.
    4. Save the index.
6. Mask the point on the image

<p align="center">
<img src="https://github.com/Baimon664/Hip_Knee_Ankle/blob/main/images/distal_femur_sulcus.jpg" height="450">
</p>