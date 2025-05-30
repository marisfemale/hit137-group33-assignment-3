# HIT137 Group 33 Assignment 3

This repository contains two main Python projects developed for HIT137 Assignment 3 at CDU:

- **Q1: Mini Photoshop** – A simple desktop image editor.
- **Q2: Side Scroller Shooter Game** – A classic arcade-style shooter game.

---

## 📁 Project Structure

```
HIT137-GROUP33-ASSIGNMENT-3/
├── Q1/
│   ├── main.py
│   ├── configs.py
│   ├── README.md
│   └── assets/
├── Q2/
│   ├── HIT3 GAME.py
│   ├── configs.py
│   ├── highscores.txt
│   ├── README.md
│   └── assets/
└── README.md  ← (this file)
```

---

## Q1: Mini Photoshop

A simple desktop application built with Python, Tkinter, OpenCV, and Pillow.  
**Features:**
- Open, crop, resize, convert to black & white, change background, and save images.
- Side-by-side view of original and edited images.
- Real-time resizing and cropping with mouse interaction.

**How to run:**
```bash
cd Q1
pip install opencv-python pillow numpy
python main.py
```
See [Q1/README.md](Q1/README.md) for full details.

---

## Q2: Side Scroller Shooter Game

A classic side-scroller shooter game built with Python and Pygame.  
**Features:**
- Multiple levels, player classes, projectile types, collectibles, and boss fights.
- Highscore system and menu navigation.
- Customizable assets and settings.

**How to run:**
```bash
cd Q2
pip install pygame
python "HIT3 GAME.py"
```
See [Q2/README.md](Q2/README.md) for full details.

---

## Requirements

- Python 3.8+
- See each subproject's README for specific dependencies.

## Credits

- Developed by Group 33 for HIT137 Assignment 3, Charles Darwin University.
- Uses [Pygame](https://www.pygame.org/), [OpenCV](https://opencv.org/), and [Pillow](https://python-pillow.org/).

---

**Enjoy exploring both projects!**