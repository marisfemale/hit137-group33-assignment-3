# configs.py

import os

# Window
window_title      = "Launcher"
window_geometry   = "300x150"

# Buttons
button_photo_text = "Edit the photo"
button_game_text  = "Play the game"
button_width      = 20
button_pad_y      = 10

# Script paths
base_dir               = os.path.dirname(__file__)
photo_editor_script    = os.path.join(base_dir, "Q1\main.py")
game_script            = os.path.join(base_dir, "Q2\HIT3 GAME.py")
