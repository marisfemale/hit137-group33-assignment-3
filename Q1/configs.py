import tkinter as tk
#Window set up
window_title = 'Mini Photoshop'
window_size = '800x600'

#Resize
resize_min=50
resize_max = 200
resize_label = 'resize %'

# Button open images 
button_open_text = 'Open'
button_open_style = {
    'bg': '#4CAF52',
    'fg': 'white',
    'font': ('Arial', 12, 'bold'),
    'padx': 10,
    'pady': 5
}

button_save_text = 'Save'

# Window
window_title        = "Mini Photoshop"
window_geometry     = "1200x800"

# Layout padding
canvas_padx         = 10
canvas_pady         = 10
toolbar_padx        = 10
toolbar_pady        = 5
button_padx         = 5

# Canvas styling
canvas_bg_color     = "grey"

# Crop rectangle
crop_rect_color     = "#ff0000"

# Slider settings
resize_min_pct      = 50
resize_max_pct      = 200
resize_default_pct  = 100
resize_label_text   = "Resize %"

# Button text & style
button_open_text    = "Open Image"
button_save_text    = "Save Image"
button_open_style   = {"bg":"#4CAF50","fg":"white","font":("Arial",10,"bold")}
button_crop_text    = "Crop Image"
button_apply_crop_text = "Apply Crop"
button_bw_text      = "Black & White"
button_bg_text      = "Change Background"
button_style        = {"bg":"#4CAF50","fg":"white","font":("Arial",10,"bold")}

# Labels under images
original_label_text = "Original"
edited_label_text   = "Edited"
label_font          = ("Arial",14,"bold")
label_color         = "white"

# Save dialog
save_default_ext    = ".png"
save_filetypes      = [("PNG files","*.png"),("JPEG files","*.jpg")]

# Canvas dimensions for side-by-side display
canvas_width        = 800
canvas_height       = 600

#Background
bg_color = (255,0,0)
bg_mask_lower = (0,0,0)
bg_mask_upper = (200,200,200)
