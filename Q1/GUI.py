# GUI.py
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk

import configs
from processor import ImageProcessor

class MiniPhotoshopApp:
    def __init__(self, root):
        self.root        = root
        self.processor   = ImageProcessor()
        self.has_cropped = False           # <-- track crop state

        root.title(configs.window_title)
        root.geometry(configs.window_geometry)

        # Canvas
        self.canvas = tk.Canvas(root, bg=configs.canvas_bg_color)
        self.canvas.pack(padx=configs.canvas_padx, pady=configs.canvas_pady)

        # Toolbar
        tf = tk.Frame(root)
        tf.pack(padx=configs.toolbar_padx, pady=configs.toolbar_pady, fill=tk.X)

        self.open_btn = tk.Button(
            tf, text=configs.button_open_text,
            command=self.load_image,
            **configs.button_open_style
        )
        self.open_btn.pack(side=tk.LEFT, padx=configs.button_padx)

        self.crop_btn = tk.Button(
            tf, text=configs.button_crop_text,
            command=self.enable_crop_mode,
            **configs.button_style
        )
        self.crop_btn.pack(side=tk.LEFT, padx=configs.button_padx)

        self.bw_btn = tk.Button(
            tf, text=configs.button_bw_text,
            command=self.convert_to_bw,
            **configs.button_style
        )
        self.bw_btn.pack(side=tk.LEFT, padx=configs.button_padx)

        self.bg_btn = tk.Button(
            tf, text=configs.button_bg_text,
            command=self.change_background,
            **configs.button_style
        )
        self.bg_btn.pack(side=tk.LEFT, padx=configs.button_padx)

        # Resize slider & status
        sf = tk.Frame(root)
        sf.pack(padx=configs.toolbar_padx, pady=configs.toolbar_pady, fill=tk.X)
        self.resize_slider = tk.Scale(
            sf,
            from_=configs.resize_min_pct,
            to=configs.resize_max_pct,
            orient=tk.HORIZONTAL,
            label=configs.resize_label_text,
            command=self.resize_image
        )
        self.resize_slider.set(configs.resize_default_pct)
        self.resize_slider.pack(side=tk.LEFT, expand=True, fill=tk.X,
                                padx=configs.button_padx)

        self.status_label = tk.Label(
            root, text="Edited size: —×—",
            font=configs.label_font
        )
        self.status_label.pack(pady=(0, configs.button_padx))

        # Save
        self.save_btn = tk.Button(
            root, text=configs.button_save_text,
            command=self.save_image,
            **configs.button_style
        )
        self.save_btn.pack(pady=configs.toolbar_pady)

        # Crop state
        self.crop_mode  = False
        self.crop_start = None

        self.canvas.bind("<ButtonPress-1>",     self.start_crop)
        self.canvas.bind("<B1-Motion>",         self.update_crop)
        self.canvas.bind("<ButtonRelease-1>",   self.finish_crop)

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images","*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if not path:
            return
        try:
            self.processor.load(path)
        except IOError as e:
            messagebox.showerror("Load Error", str(e))
            return

        # reset crop flag
        self.has_cropped = False
        self.crop_mode    = False
        self.crop_btn.config(
            text=configs.button_crop_text,
            command=self.enable_crop_mode
        )
        self.resize_slider.set(configs.resize_default_pct)
        self._update_canvas()

    def _update_canvas(self):
        img  = self.processor.current
        base = self.processor.base_image
        if img is None or base is None:
            return

        cw, ch = configs.canvas_width, configs.canvas_height
        self.canvas.config(width=cw, height=ch)
        self.canvas.delete("all")

        if not self.has_cropped:
            # single centered display of the loaded image
            h, w = img.shape[:2]
            scale = min(cw / w, ch / h)
            nw, nh = int(w*scale), int(h*scale)
            resized = cv2.resize(img, (nw, nh))
            tk_img = ImageTk.PhotoImage(Image.fromarray(resized))

            x_off = (cw - nw)//2
            y_off = (ch - nh)//2
            self.canvas.create_image(x_off, y_off, anchor=tk.NW, image=tk_img)
            self._ref_single = tk_img

        else:
            # side by side
            half_w = cw // 2

            # left: original
            h1, w1 = base.shape[:2]
            s1     = min(half_w/w1, ch/h1)
            o2     = cv2.resize(base, (int(w1*s1), int(h1*s1)))
            tk1    = ImageTk.PhotoImage(Image.fromarray(o2))
            x1_off = (half_w - o2.shape[1])//2
            y1_off = (ch - o2.shape[0])//2
            self.canvas.create_image(x1_off, y1_off,
                                     anchor=tk.NW, image=tk1)
            self.canvas.create_text(
                x1_off+o2.shape[1]//2,
                y1_off+o2.shape[0]+configs.label_offset,
                text=configs.original_label_text,
                font=configs.label_font,
                fill=configs.label_color
            )
            self._ref_orig = tk1

            # right: edited
            h2, w2 = img.shape[:2]
            s2     = min(half_w/w2, ch/h2)
            e2     = cv2.resize(img, (int(w2*s2), int(h2*s2)))
            tk2    = ImageTk.PhotoImage(Image.fromarray(e2))
            x2_off = half_w + (half_w-e2.shape[1])//2
            y2_off = (ch-e2.shape[0])//2
            self.canvas.create_image(x2_off, y2_off,
                                     anchor=tk.NW, image=tk2)
            self.canvas.create_text(
                x2_off+e2.shape[1]//2,
                y2_off+e2.shape[0]+configs.label_offset,
                text=configs.edited_label_text,
                font=configs.label_font,
                fill=configs.label_color
            )
            self._ref_edit = tk2

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
        # Pass canvas coordinates directly; let crop_image handle mapping
        self.processor.crop_area = (x0, y0, x1, y1)
        self.crop_mode = False
        self.crop_btn.config(
            text=configs.button_apply_crop_text,
            command=self.apply_crop
        )

    def enable_crop_mode(self):
        self.crop_mode = True
        self.processor.crop_area = None
        self.canvas.delete("crop_rect")
        self.crop_btn.config(
            text=configs.button_crop_text,
            command=self.finish_crop
        )

    def apply_crop(self):
        self.processor.crop()
        self.has_cropped = True          # <-- now show side by side
        self.crop_btn.config(
            text=configs.button_crop_text,
            command=self.enable_crop_mode
        )
        self.resize_slider.set(configs.resize_default_pct)
        self._update_canvas()

    def resize_image(self, val):
        if self.processor.master is None:
            return

        pct = int(val)
        self.processor.resize(pct)
        h2, w2 = self.processor.current.shape[:2]
        self.status_label.config(text=f"Edited size: {w2}×{h2}")
        self._update_canvas()

    def convert_to_bw(self):
        self.processor.to_bw()
        self.resize_slider.set(configs.resize_default_pct)
        self._update_canvas()

    def change_background(self):
        self.processor.change_bg()
        self.resize_slider.set(configs.resize_default_pct)
        self._update_canvas()

    def save_image(self):
        path = filedialog.asksaveasfilename(
            defaultextension=configs.save_default_ext,
            filetypes=configs.save_filetypes
        )
        if not path:
            return
        self.processor.save(path)
        messagebox.showinfo(
            configs.save_window_title,
            configs.save_successful_message
        )
