import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
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
        self.canvas.pack(padx=configs.canvas_padx, pady=configs.canvas_pady)

        # Button toolbar
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(padx=configs.toolbar_padx, pady=configs.toolbar_pady, fill=tk.X)
        self.open_btn = tk.Button(
            btn_frame,
            text=configs.button_open_text,
            command=self.load_image,
            **configs.button_open_style
        )
        self.open_btn.pack(side=tk.LEFT, padx=configs.button_padx)

        self.crop_btn = tk.Button(
            btn_frame,
            text=configs.button_crop_text,
            command=self.enable_crop_mode,
            **configs.button_style
        )
        self.crop_btn.pack(side=tk.LEFT, padx=configs.button_padx)

        self.bw_btn = tk.Button(
            btn_frame,
            text=configs.button_bw_text,
            command=self.convert_to_bw,
            **configs.button_style
        )
        self.bw_btn.pack(side=tk.LEFT, padx=configs.button_padx)

        self.bg_btn = tk.Button(
            btn_frame,
            text=configs.button_bg_text,
            command=self.change_background,
            **configs.button_style
        )
        self.bg_btn.pack(side=tk.LEFT, padx=configs.button_padx)

        # Resize slider
        slider_frame = tk.Frame(self.root)
        slider_frame.pack(padx=configs.toolbar_padx, pady=configs.toolbar_pady, fill=tk.X)
        self.resize_slider = tk.Scale(
            slider_frame,
            from_=configs.resize_min_pct,
            to=configs.resize_max_pct,
            orient=tk.HORIZONTAL,
            label=configs.resize_label_text,
            command=self.resize_image
        )
        self.status_label = tk.Label(self.root, text="Edited size: —×—", font=configs.label_font)
        self.status_label.pack(pady=(0, configs.button_padx))
        self.resize_slider.set(configs.resize_default_pct)
        self.resize_slider.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=configs.button_padx)

        # Save button
        self.save_btn = tk.Button(
            self.root,
            text=configs.button_save_text,
            command=self.save_image,
            **configs.button_style
        )
        self.save_btn.pack(pady=configs.toolbar_pady)

        # State variables
        self.base_image = None        # original loaded image
        self.master_image = None      # always the source for resizing (original or cropped)
        self.current_image = None     # what’s currently displayed
        self.crop_mode = False
        self.crop_start = None
        self.crop_area = None
        self.has_cropped = False      # track if a crop has been applied

        # Canvas bindings for cropping
        self.canvas.bind("<ButtonPress-1>",     self.start_crop)
        self.canvas.bind("<B1-Motion>",         self.update_crop)
        self.canvas.bind("<ButtonRelease-1>",   self.finish_crop)

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images","*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if not path:
            return
        img_bgr = cv2.imread(path)
        if img_bgr is None:
            return
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        self.base_image = img_rgb.copy()
        self.current_image = img_rgb.copy()
        self.master_image = img_rgb.copy()
        self.crop_mode = False
        self.has_cropped = False
        self.crop_btn.config(text=configs.button_crop_text, command=self.enable_crop_mode)
        self.resize_slider.set(configs.resize_default_pct)
        self._update_canvas()

    def _update_canvas(self):
        if self.current_image is None or self.base_image is None:
            return

        # Canvas dimensions
        c_w, c_h = configs.canvas_width, configs.canvas_height
        self.canvas.config(width=c_w, height=c_h)
        self.canvas.delete("all")

        if not self.has_cropped:
            # -- CENTER THE LOADED IMAGE --

            img = self.current_image
            h, w = img.shape[:2]
            # scale to fit canvas if needed
            scale = min(c_w / w, c_h / h)
            nw, nh = int(w * scale), int(h * scale)
            resized = cv2.resize(img, (nw, nh))
            pil = Image.fromarray(resized)
            tk_img = ImageTk.PhotoImage(pil)

            x_off = (c_w - nw) // 2
            y_off = (c_h - nh) // 2
            self.canvas.create_image(x_off, y_off, anchor=tk.NW, image=tk_img)
            self._tk_single = tk_img  # keep reference

        else:
            # -- SIDE-BY-SIDE ORIGINAL & EDITED --

            half_w = c_w // 2

            # Original (left)
            orig = self.base_image
            h1, w1 = orig.shape[:2]
            scale1 = min(half_w / w1, c_h / h1)
            nw1, nh1 = int(w1 * scale1), int(h1 * scale1)
            orig_r = cv2.resize(orig, (nw1, nh1))
            pil1 = Image.fromarray(orig_r)
            tk1 = ImageTk.PhotoImage(pil1)
            x1_off = (half_w - nw1) // 2
            y1_off = (c_h - nh1) // 2
            self.canvas.create_image(x1_off, y1_off, anchor=tk.NW, image=tk1)
            self.canvas.create_text(
                x1_off + nw1//2, y1_off + nh1 + configs.label_offset,
                text=configs.original_label_text,
                font=configs.label_font,
                fill=configs.label_color
            )
            self._tk_orig = tk1

            # Edited (right)
            curr = self.current_image
            h2, w2 = curr.shape[:2]
            scale2 = min(half_w / w2, c_h / h2)
            nw2, nh2 = int(w2 * scale2), int(h2 * scale2)
            curr_r = cv2.resize(curr, (nw2, nh2))
            pil2 = Image.fromarray(curr_r)
            tk2 = ImageTk.PhotoImage(pil2)
            x2_off = half_w + (half_w - nw2) // 2
            y2_off = (c_h - nh2) // 2
            self.canvas.create_image(x2_off, y2_off, anchor=tk.NW, image=tk2)
            self.canvas.create_text(
                x2_off + nw2//2, y2_off + nh2 + configs.label_offset,
                text=configs.edited_label_text,
                font=configs.label_font,
                fill=configs.label_color
            )
            self._tk_edit = tk2

    def start_crop(self, ev):
        if not self.crop_mode:
            return
        self.crop_start = (ev.x, ev.y)
        self.canvas.delete("crop_rect")

    def update_crop(self, ev):
        if not self.crop_mode or not self.crop_start:
            return
        x0, y0 = self.crop_start
        x1, y1 = ev.x, ev.y
        self.canvas.delete("crop_rect")
        self.canvas.create_rectangle(
            x0, y0, x1, y1,
            outline=configs.crop_rect_color,
            tag="crop_rect"
        )

    def finish_crop(self, ev):
        if not self.crop_mode or not self.crop_start:
            return
        x0, y0 = self.crop_start
        x1, y1 = ev.x, ev.y
        img_h, img_w = self.base_image.shape[:2]
        c_w, c_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        sx, sy = img_w / c_w, img_h / c_h
        rx0, ry0 = int(min(x0, x1) * sx), int(min(y0, y1) * sy)
        rx1, ry1 = int(max(x0, x1) * sx), int(max(y0, y1) * sy)

        self.crop_area = (rx0, ry0, rx1, ry1)
        self.crop_mode = False
        self.crop_btn.config(text=configs.button_apply_crop_text, command=self.apply_crop)

    def enable_crop_mode(self):
        self.crop_mode = True
        self.crop_start = None
        self.crop_area = None
        self.canvas.delete("crop_rect")
        self.crop_btn.config(text=configs.button_crop_text, command=self.finish_crop)

    def apply_crop(self):
        if not self.crop_area:
            return
        x0, y0, x1, y1 = self.crop_area
        self.current_image = self.base_image[y0:y1, x0:x1]
        self.master_image = self.current_image.copy()  # reset master
        self.has_cropped = True
        self.crop_btn.config(text=configs.button_crop_text, command=self.enable_crop_mode)
        self.resize_slider.set(configs.resize_default_pct)
        self._update_canvas()

    def resize_image(self, val):
        if self.master_image is None:
            return

        scale = int(val) / 100
        h0, w0 = self.master_image.shape[:2]
        new_w, new_h = int(w0 * scale), int(h0 * scale)

        # update the status label
        self.status_label.config(text=f"Edited size: {new_w}×{new_h}")

        self.current_image = cv2.resize(self.master_image, (new_w, new_h))
        self._update_canvas()
    def convert_to_bw(self):
        if self.current_image is None:
            return
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
        self.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        self.master_image = self.current_image.copy()
        self.resize_slider.set(configs.resize_default_pct)
        self._update_canvas()

    def change_background(self):
        if self.current_image is None:
            return
        h, w = self.current_image.shape[:2]
        bg = np.full((h, w, 3), configs.bg_color, dtype=np.uint8)
        mask = cv2.inRange(self.current_image, configs.bg_mask_lower, configs.bg_mask_upper)
        fg = cv2.bitwise_and(self.current_image, self.current_image, mask=~mask)
        bg_part = cv2.bitwise_and(bg, bg, mask=mask)
        self.current_image = cv2.add(fg, bg_part)
        self.master_image = self.current_image.copy()
        self.resize_slider.set(configs.resize_default_pct)
        self._update_canvas()

    def save_image(self):
        if self.current_image is None:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=configs.save_default_ext,
            filetypes=configs.save_filetypes
        )
        if path:
            cv2.imwrite(path, cv2.cvtColor(self.current_image, cv2.COLOR_RGB2BGR))
            messagebox.showinfo(configs.save_window_title, configs.save_successful_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniPhotoshopApp(root)
    root.mainloop()
