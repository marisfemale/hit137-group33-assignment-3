# processor.py
import configs
from processes.open        import load_image
from processes.crop        import crop_image
from processes.resize      import resize_image
from processes.black_white import to_black_and_white
from processes.bg_change   import change_background

class ImageProcessor:
    """Encapsulates image state and operations."""

    def __init__(self):
        self.base_image = None
        self.current    = None
        self.master     = None
        self.crop_area  = None

    def load(self, path):
        img = load_image(path)
        self.base_image = img.copy()
        self.current    = img.copy()
        self.master     = img.copy()
        self.crop_area  = None

    def crop(self):
        if self.crop_area:
            self.current   = crop_image(
                self.base_image,
                self.crop_area,
                (configs.canvas_width, configs.canvas_height)
            )
            self.master    = self.current.copy()
            self.crop_area = None

    def resize(self, pct):
        self.current = resize_image(self.master, pct)

    def to_bw(self):
        self.current = to_black_and_white(self.current)
        self.master  = self.current.copy()

    def change_bg(self):
        self.current = change_background(
            self.current,
            configs.bg_color,
            configs.bg_mask_lower,
            configs.bg_mask_upper
        )
        self.master  = self.current.copy()

    def save(self, path):
        import cv2
        bgr = cv2.cvtColor(self.current, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, bgr)
