# Side Scroller Shooter Game

This is a classic side-scroller shooter game built with Python and Pygame. The player can select a character class, projectile type, and difficulty, and then fight through multiple levels of zombies and bosses. Collectibles, score tracking, and a highscore system are included.

## Features

- **Multiple Levels:** Progress through 3 levels, each with unique backgrounds and a boss fight.
- **Player Classes:** Choose from different classes, each with unique abilities.
- **Projectile Types:** Select your projectile type for different effects.
- **Collectibles:** Health, extra lives, and bonus score items appear randomly.
- **Boss Fights:** Each level ends with a challenging boss.
- **Highscores:** Top scores are saved and viewable from the main menu.
- **Pause Menu:** Pause the game and return to the main menu at any time.

## Controls

- **A / D:** Move left/right
- **Space:** Jump
- **Backspace:** Shoot
- **Esc:** Pause menu
- **Number Keys (1-9):** Menu selection
- **Enter:** Confirm menu selection or input

## How to Run

1. **Install requirements:**
    ```bash
    pip install pygame
    ```

2. **Run the game:**
    ```bash
    python HIT3\ GAME.py
    ```

3. **Assets:**
    - Make sure the `assets/` folder (with images and sounds) is present as referenced in the code.

## File Structure

```
Q2/
├── HIT3 GAME.py
├── configs.py
├── highscores.txt
└── assets/
    ├── images/
    │   ├── background.png
    │   ├── background2.png
    │   ├── background3.png
    │   ├── medkit.png
    │   ├── extralife.png
    │   └── spritesheets/
    │       └── ... (player, zombie, boss sprites)
    └── sounds/
        └── shoot.wav
```

## Customization

- **Add more backgrounds:** Place new images in `assets/images/` and add their paths to `background_paths` in `configs.py`.
- **Add more player classes or projectiles:** Edit `player_classes` and `projectile_types` in `configs.py`.

## Troubleshooting

- If you see `AttributeError: module 'pygame' has no attribute 'font'`, ensure you have installed pygame in your current environment and there is no file named `pygame.py` in your project.
- If assets are missing, make sure all image and sound files referenced in the code exist in the correct folders.

## Credits

- Developed for HIT137 Assignment 3, CDU.
- Uses [Pygame](https://www.pygame.org/) for graphics and sound.

---

Enjoy the game!