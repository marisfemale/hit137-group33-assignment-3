# process/crop.py
import numpy as np

def crop_image(img: np.ndarray, area: tuple, canvas_size: tuple):
    """
    area = (x0,y0,x1,y1) in canvas coords.
    canvas_size = (can_w, can_h)
    img.shape gives (h, w).
    """
    x0,y0,x1,y1 = area
    can_w, can_h = canvas_size
    img_h, img_w = img.shape[:2]
    sx, sy = img_w / can_w, img_h / can_h
    rx0, ry0 = int(min(x0,x1)*sx), int(min(y0,y1)*sy)
    rx1, ry1 = int(max(x0,x1)*sx), int(max(y0,y1)*sy)
    return img[ry0:ry1, rx0:rx1]
