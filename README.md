# Mini Photoshop (Q1)

This is a simple "Mini Photoshop" desktop application built with Python, Tkinter, OpenCV, and Pillow. It allows you to open an image, crop, resize, convert to black & white, change the background, and save the edited result. The app displays the original and edited images side by side for easy comparison.

## Features

- **Open Image:** Load JPG, PNG, BMP, or TIFF images.
- **Crop:** Select and crop a region of the image using the mouse.
- **Resize:** Use a slider to resize the edited image in real time.
- **Black & White:** Convert the edited image to grayscale.
- **Change Background:** Replace the background color based on a mask.
- **Save:** Save the edited image to your computer.
- **Side-by-Side View:** See the original and edited images together, each labeled.

## How to Run

1. **Install requirements:**
    ```bash
    pip install opencv-python pillow numpy
    ```

2. **Run the app:**
    ```bash
    python main.py
    ```

## Controls

- **Open:** Click the "Open" button to select an image.
- **Crop:** Click "Crop", drag to select an area, then click "Apply Crop".
- **Resize:** Move the slider to resize the edited image.
- **Black & White:** Click to convert the edited image to grayscale.
- **Change Background:** Click to change the background color.
- **Save:** Click to save the edited image.

## File Structure

```
Q1/
├── main.py
├── configs.py
└── (assets, if any)
```

## Configuration

All UI labels, colors, and settings are in `configs.py`. You can adjust:
- Window size and title
- Button labels and styles
- Crop rectangle color
- Background color and mask for background replacement
- Slider min/max/default values

## Notes

- The original image is always shown on the left and never modified.
- The edited image (right) updates with each operation.
- The app uses OpenCV for image processing and Pillow for Tkinter image display.

## Troubleshooting

- If you see errors about missing modules, ensure you have installed all requirements.
- If images do not display, check that your image files are valid and supported.

---

**Developed for HIT137 Assignment 3, CDU.**