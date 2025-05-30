import pygame
import random
from configs import screen_width, screen_height, white
from Utils import get_medkit_img, get_extralife_img, get_score_bonus, get_ui_font

class Collectible:
    def __init__(self):
        self.types = [("Health", 30), ("ExtraLife", 5), ("Bonus", 40)]
        pool = [t for t, chance in self.types for _ in range(chance)]
        self.kind = random.choice(pool)
        self.rect = pygame.Rect(random.randint(100, screen_width - 100), screen_height - 30, 20, 20)

    def apply(self, player):
        if self.kind == "Health":
            player.hp = min(50, player.hp + 10)
        elif self.kind == "ExtraLife":
            player.lives += 1
        elif self.kind == "Bonus":
            player.score += 1 + get_score_bonus()

    def draw(self, screen):
        if self.kind == "Health":
            screen.blit(get_medkit_img(), self.rect)
        elif self.kind == "ExtraLife":
            screen.blit(get_extralife_img(), self.rect)
        else:
            bonus_text = get_ui_font().render("+1", True, white)
            text_rect = bonus_text.get_rect(center=self.rect.center)
            screen.blit(bonus_text, text_rect)
