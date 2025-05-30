# process/bg_change.py
import cv2
import numpy as np

def change_background(img: np.ndarray,
                      bg_color: tuple,
                      mask_lower: tuple,
                      mask_upper: tuple):
    """
    Replace pixels in [mask_lower..mask_upper] with bg_color.
    """
    h, w = img.shape[:2]
    bg = np.full((h, w, 3), bg_color, dtype=np.uint8)
    mask = cv2.inRange(img, mask_lower, mask_upper)
    fg   = cv2.bitwise_and(img, img, mask=~mask)
    bgp  = cv2.bitwise_and(bg, bg, mask=mask)
    return cv2.add(fg, bgp)
