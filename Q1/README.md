# Mini Photoshop

A simple desktop image editor built with Python, Tkinter and OpenCV.  
It demonstrates core OOP principles, a responsive GUI, and basic image processing (crop, resize, black & white, background replace, save).

---

## Features

- **Load Image**  
  Select and display an image from your local filesystem.  

- **Crop**  
  Click “Crop Image,” drag a rectangle on the image, then “Apply Crop” to extract that region.

- **Resize**  
  Use the slider (50–200 %) to scale the current (cropped or full) image in real time.

- **Black & White**  
  Convert the displayed image to grayscale.

- **Change Background**  
  Mask out dark pixels and replace them with a solid color.

- **Side-by-Side Preview**  
  Always shows the **Original** (left) and **Edited** (right) images together.

- **Save**  
  Export your edited image as PNG or JPEG.

---

## Project Structure

.
├── main.py # Application entry point
└── configs.py # All “magic” values (colors, labels, ranges, paddings)

---

## Requirements

- Python 3.7+
- [OpenCV Python](https://pypi.org/project/opencv-python/)  
- [Pillow](https://pypi.org/project/Pillow/)  

Install with:

```bash
- 'pip install opencv-python Pillow'


---