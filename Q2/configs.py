# configs.py

# ========== Window & Display ==========
screen_width      = 640
screen_height     = 480
fps               = 30
window_title      = "Side Scroller Shooter"

# ========== Colors ==========
white             = (255, 255, 255)
black             = (0, 0, 0)
green             = (0, 200, 0)
red               = (200, 0, 0)
blue              = (0, 0, 200)
yellow            = (255, 255, 0)
purple            = (160, 32, 240)

# ========== Font Settings ==========
font_name         = "Arial"
font_size         = 24

# ========== File Paths ==========
highscore_file    = "highscores.txt"
background_paths  = [
    "assets/images/background.png",
    "assets/images/background2.png",
    "assets/images/background3.png"
]
medkit_path       = "assets/images/medkit.png"
extralife_path    = "assets/images/extralife.png"

# ========== Gameplay Settings ==========
difficulty_levels = ["Easy", "Normal", "Hard"]
score_bonus_map   = {'Easy': 0, 'Normal': 1, 'Hard': 2}
level_durations   = [30, 45, 60]        # seconds per level
projectile_types  = ["Fast", "Strong", "Puncture"]

# ========== Player Classes ==========
player_classes    = {
    "Tank":      {"speed": 3, "jump": 10, "lives": 3},
    "Jumper":    {"speed": 5, "jump": 15, "lives": 3},
    "Speedster": {"speed": 7, "jump": 10, "lives": 3},
}

# ========== Sprite Sizes ==========
player_width      = 64
player_height     = 128
enemy_width       = 128
enemy_height      = 128
projectile_width  = 10
projectile_height = 5

# ========== HUD ==========
hud_bar_width     = 50
hud_bar_height    = 10
