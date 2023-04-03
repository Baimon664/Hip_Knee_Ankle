import cv2

def preprocess(img, resized=(1024,1024), region="low"):
    # Grayscale Input

    # Normalization: CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)

    # Region of Interest
    h,w = img.shape[:2]
    if region=="low":
        img = img[w:]
    elif region=="mid":
        img = img[(h-w)//2:(h+w)//2]
    elif region=="high":
        img = img[:w]

    # Resized
    img = cv2.resize(img, dsize=resized)

    return img