import tkinter as tk
from tkinter import filedialog
import numpy as np
import configs
import cv2
from PIL import Image, ImageTk

class MiniPhotoshopApp:
    def __init__(self, root):
        self.root = root
        self.root.title(configs.window_title)
        self.root.geometry(configs.window_geometry)

        # Canvas for image display
        self.canvas = tk.Canvas(self.root, bg=configs.canvas_bg_color)
        self.canvas.pack(padx=configs.toolbar_padx, pady=configs.toolbar_pady)

        # Button toolbar
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(padx=configs.canvas_padx, pady=configs.canvas_pady, fill=tk.X)
        self.open_btn = tk.Button(
            btn_frame, text=configs.button_open_text,
            command=self.load_image, **configs.button_open_style
        )
        self.open_btn.pack(side=tk.LEFT, padx=configs.button_padx)

        self.crop_btn = tk.Button(btn_frame, text=configs.button_crop_text,
                                  command=self.enable_crop_mode)
        self.crop_btn.pack(side=tk.LEFT, padx=configs.button_padx)

        self.bw_btn = tk.Button(btn_frame, text=configs.button_bw_text,
                                command=self.convert_to_bw)
        self.bw_btn.pack(side=tk.LEFT, padx=configs.button_padx)

        self.bg_btn = tk.Button(btn_frame, text=configs.button_bg_text,
                                command=self.change_background)
        self.bg_btn.pack(side=tk.LEFT, padx=configs.button_padx)

        # Resize slider
        slider_frame = tk.Frame(self.root)
        slider_frame.pack(padx=configs.toolbar_padx, pady=configs.toolbar_pady, fill=tk.X)
        self.resize_slider = tk.Scale(
            slider_frame, from_=configs.resize_min_pct, to=configs.resize_max_pct, orient=tk.HORIZONTAL,
            label=configs.resize_label_text, command=self.resize_image
        )
        self.resize_slider.set(configs.resize_default_pct)
        self.resize_slider.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=configs.button_padx)

        # Save
        self.save_btn = tk.Button(self.root, text=configs.button_save_text,
                                  command=self.save_image)
        self.save_btn.pack(pady=5)

        # State
        self.current_image = None
        self.base_image = None
        self.crop_mode = False
        self.crop_start = None
        self.crop_area = None

        # Canvas mouse bindings
        self.canvas.bind("<ButtonPress-1>",     self.start_crop)
        self.canvas.bind("<B1-Motion>",         self.update_crop)
        self.canvas.bind("<ButtonRelease-1>",   self.finish_crop)

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images","*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if not path:
            return
        img = cv2.imread(path)
        if img is None:
            return
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.current_image = img
        
        self.base_image = img.copy()  # Store original for resizing
        self.crop_area = None
        self.crop_mode = False
        self.resize_slider.set(configs.resize_default_pct)
        self._update_canvas()

    def _update_canvas(self):
        """Draw original (left) and current/cropped (right) image side by side on the canvas, with labels underneath."""
        if self.current_image is None or self.base_image is None:
            return

        # Canvas size
        c_w, c_h = 800, 600
        half_w = c_w // 2

        # Prepare original (left)
        orig = self.base_image
        h, w = orig.shape[:2]
        scale = min(half_w / w, c_h / h * 0.9)  # leave space for label
        nw, nh = int(w * scale), int(h * scale)
        orig_resized = cv2.resize(orig, (nw, nh))
        orig_pil = Image.fromarray(orig_resized)
        orig_tk = ImageTk.PhotoImage(orig_pil)

        # Prepare current/cropped (right)
        curr = self.current_image
        h2, w2 = curr.shape[:2]
        scale2 = min(half_w / w2, c_h / h2 * 0.9)
        nw2, nh2 = int(w2 * scale2), int(h2 * scale2)
        curr_resized = cv2.resize(curr, (nw2, nh2))
        curr_pil = Image.fromarray(curr_resized)
        curr_tk = ImageTk.PhotoImage(curr_pil)

        self.canvas.config(width=c_w, height=c_h)
        self.canvas.delete("all")
        # Center vertically, leave space for label (20px)
        y_off1 = (c_h - nh - 20) // 2
        y_off2 = (c_h - nh2 - 20) // 2
        # Center horizontally in each half
        x_off1 = (half_w - nw) // 2
        x_off2 = half_w + (half_w - nw2) // 2
        self.canvas.create_image(x_off1, y_off1, anchor=tk.NW, image=orig_tk)
        self.canvas.create_image(x_off2, y_off2, anchor=tk.NW, image=curr_tk)
        # Add labels under each image
        self.canvas.create_text(x_off1 + nw//2, y_off1 + nh + 12, text=configs.original_label_text, font=(configs.label_font), fill=configs.label_color)
        self.canvas.create_text(x_off2 + nw2//2, y_off2 + nh2 + 12, text=configs.edited_label_text, font=(configs.label_font), fill=configs.label_color)
        # Keep references to avoid garbage collection
        self.tkimg_left = orig_tk
        self.tkimg_right = curr_tk

    def start_crop(self, ev):
        if not self.crop_mode: return
        self.crop_start = (ev.x, ev.y)

    def update_crop(self, ev):
        if not self.crop_mode or not self.crop_start: return
        x0, y0 = self.crop_start
        x1, y1 = ev.x, ev.y
        self.canvas.delete("crop_rect")
        self.canvas.create_rectangle(x0,y0, x1,y1,
                                     outline=configs.crop_rect_color, tag="crop_rect")

    def finish_crop(self, ev):
        if not self.crop_mode or not self.crop_start: return
        x0, y0 = self.crop_start
        x1, y1 = ev.x, ev.y
        # Map from canvas to image coords:
        img_h, img_w = self.current_image.shape[:2]
        c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        sx, sy = img_w/c_w, img_h/c_h
        self.crop_area = (
            int(min(x0,x1)*sx), int(min(y0,y1)*sy),
            int(max(x0,x1)*sx), int(max(y0,y1)*sy)
        )
        # Switch button to “Apply Crop”
        self.crop_mode = False
        self.crop_btn.config(text=configs.button_apply_crop_text, command=self.apply_crop)

    def enable_crop_mode(self):
        self.crop_mode = True
        self.crop_start = None
        self.crop_area = None
        self.canvas.delete("crop_rect")
        self.crop_btn.config(text=configs.button_crop_text, command=self.finish_crop)

    def apply_crop(self):
        if not self.crop_area: return
        x0,y0,x1,y1 = self.crop_area
        # Only update current_image, not base_image
        self.current_image = self.current_image[y0:y1, x0:x1]
        self.crop_area = None
        self.crop_mode = False
        self.crop_btn.config(text=configs.button_crop_text, command=self.enable_crop_mode)
        self.resize_slider.set(configs.resize_default_pct)
        self._update_canvas()


    def resize_image(self, val):
        if self.current_image is None:
            return
        scale = int(val)/100
        h, w = self.current_image.shape[:2]
        resized = cv2.resize(self.current_image, (int(w*scale), int(h*scale)))
        self.current_image = resized
        self._update_canvas()


    def convert_to_bw(self):
        if self.current_image is None:
            return
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
        self.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        self.resize_slider.set(configs.resize_default_pct)
        self._update_canvas()

    def change_background(self):
        if self.current_image is None:
            return
        h, w = self.current_image.shape[:2]
        bg = np.full((h, w, 3), configs.bg_color, dtype=np.uint8)
        mask = cv2.inRange(
            self.current_image,
            configs.bg_mask_lower,
            configs.bg_mask_upper
        )
        fg = cv2.bitwise_and(
            self.current_image,
            self.current_image,
            mask=~mask
        )
        bg_part = cv2.bitwise_and(bg, bg, mask=mask)
        self.current_image = cv2.add(fg, bg_part)
        self.resize_slider.set(configs.resize_default_pct)
        self._update_canvas()


    def save_image(self):
        if self.current_image is None:
            return
        p = filedialog.asksaveasfilename(
            defaultextension=configs.save_default_ext,
            filetypes=[configs.save_default_ext]
        )
        if p:
            cv2.imwrite(p,
                        cv2.cvtColor(self.current_image,
                                     cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    root = tk.Tk()
    app  = MiniPhotoshopApp(root)
    root.mainloop()
