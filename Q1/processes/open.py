# process/open.py
import cv2

def load_image(path: str):
    """Load from disk & convert BGR→RGB, or raise IOError."""
    bgr = cv2.imread(path)
    if bgr is None:
        raise IOError(f"Cannot load {path!r}")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
