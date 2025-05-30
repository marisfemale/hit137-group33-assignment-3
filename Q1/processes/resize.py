# process/resize.py
import cv2
import numpy as np

def resize_image(img: np.ndarray, pct: int):
    """
    pct = 10–200
    """
    h, w = img.shape[:2]
    nw, nh = int(w * pct/100), int(h * pct/100)
    return cv2.resize(img, (nw, nh))
