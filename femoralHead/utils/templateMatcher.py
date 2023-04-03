import numpy as np
import cv2

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, -angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def templateMatcher(img, template, scales=np.arange(0.8,1.21,0.1), angles=np.arange(-45,46,15)):
    # Initialize best match values
    best_scale = 1
    best_loc = None
    best_angle = None
    best_score = -np.inf
        
    # Iterate over rotation
    for angle in angles:
        rotated = rotate_image(template, angle)
        h,w = rotated.shape[:2]
        rotated = rotated[h//4:-h//4,w//4:-w//4]
        # res = cv2.matchTemplate(img, rotated, cv2.TM_CCOEFF_NORMED)

        # Iterate over scales
        for scale in scales:         
            # Resize template
            resized_template = cv2.resize(rotated, None, fx=scale, fy=scale)

            res = cv2.matchTemplate(img,resized_template,cv2.TM_CCOEFF_NORMED)

            # Find location of best match for current scale
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # Update best match values if current scale has better match
            if max_val > best_score:
                best_scale = scale
                best_angle = angle
                best_loc = max_loc
                best_score = max_val

    w, h = (np.array(rotated.shape[1::-1]) * best_scale).astype(int)

    return best_loc[0], best_loc[1], w, h