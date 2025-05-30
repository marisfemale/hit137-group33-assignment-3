import pygame
import os
from configs import font_name, font_size, white, black

ui_font = None
medkit_img = None
extralife_img = None
score_bonus = 1

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def init_font():
    global ui_font
    ui_font = pygame.font.SysFont(font_name, font_size)
    
def get_ui_font():
    if ui_font is None:
        raise Exception("Font not initialized. Call init_font() before using get_ui_font().")
    return ui_font

def set_assets(medkit, extralife, bonus):
    global medkit_img, extralife_img, score_bonus
    medkit_img = medkit
    extralife_img = extralife
    score_bonus = bonus

def get_medkit_img():
    return medkit_img

def get_extralife_img():
    return extralife_img

def get_score_bonus():
    return score_bonus

def get_asset_path(relative_path):
    return os.path.join(BASE_DIR, relative_path)

def load_sprite_sheet(path, frame_screen_width, frame_screen_height, num_frames):
    full_path = os.path.join(BASE_DIR, "..", path) if not os.path.isabs(path) else path
    sheet = pygame.image.load(full_path).convert_alpha()
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * frame_screen_width, 0, frame_screen_width, frame_screen_height))
        frames.append(frame)
    return frames

def draw_text(text, x, y, screen):
    screen.blit(ui_font.render(text, True, white), (x, y))

def show_menu(options, title, screen):
    while True:
        screen.fill(black)
        draw_text(title, screen.get_width() // 2 - 100, 50, screen)
        for i, opt in enumerate(options):
            draw_text(f"{i + 1}. {opt}", screen.get_width() // 2 - 100, 100 + i * 40, screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_1
                    if index < len(options):
                        return options[index]
