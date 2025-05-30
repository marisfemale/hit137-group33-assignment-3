import pygame
import os
from Projectile import Projectile
from configs import screen_width, screen_height, player_classes, player_width, player_height
from Utils import get_asset_path

class Player:
    def __init__(self, cls, proj_type):
        self.facing_left = False
        self.rect = pygame.Rect((screen_width - player_width) // 2, screen_height - player_height, player_width, player_height)
        self.vx = player_classes[cls]["speed"]
        self.vy = 0
        self.on_ground = True
        self.jump_strength = player_classes[cls]["jump"]
        self.hp = 50
        self.lives = player_classes[cls]["lives"]
        self.score = 0
        self.class_type = cls
        self.projectile_type = proj_type

        base_path = os.path.join("assets", "images", "spritesheets", cls)
        sheet_path = get_asset_path(os.path.join(base_path, f"{cls.lower()}_walk.png"))
        self.walk_frames = self.load_sprite_sheet(sheet_path, 128, 128, 8)

        idle_path = get_asset_path(os.path.join(base_path, f"{cls.lower()}_idle.png"))
        idle_sheet = pygame.image.load(idle_path).convert_alpha()
        self.idle_frame = idle_sheet.subsurface(pygame.Rect(0, 0, 112, 128))

        self.jump_frame = self.walk_frames[0]
        self.current_frame = 0
        self.frame_timer = 0

    def load_sprite_sheet(self, path, frame_screen_width, frame_screen_height, num_frames):
        sheet = pygame.image.load(path).convert_alpha()
        frames = []
        for i in range(num_frames):
            frame = sheet.subsurface(pygame.Rect(i * frame_screen_width, 0, frame_screen_width, frame_screen_height))
            frames.append(frame)
        return frames

    def move(self, keys):
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.vx
            self.facing_left = True
        if keys[pygame.K_d] and self.rect.right < screen_width:
            self.rect.x += self.vx
            self.facing_left = False
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = -self.jump_strength
            self.on_ground = False

    def apply_gravity(self):
        self.vy += 1
        self.rect.y += self.vy
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.on_ground = True
            self.vy = 0

    def shoot(self):
        speed = 10 if self.projectile_type == "Fast" else 5
        damage = 2 if self.projectile_type == "Strong" else 1
        puncture = self.projectile_type == "Puncture"

        direction = -1 if self.facing_left else 1
        x_pos = self.rect.left if self.facing_left else self.rect.right
        return Projectile(x_pos, self.rect.centery, speed, damage, puncture, direction)

    def draw(self, screen):
        keys = pygame.key.get_pressed()
        if not self.on_ground:
            frame = self.jump_frame
        elif keys[pygame.K_a] or keys[pygame.K_d]:
            self.frame_timer += 1
            if self.frame_timer >= 5:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
                self.frame_timer = 0
            frame = self.walk_frames[self.current_frame]
        else:
            frame = self.idle_frame

        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)

        screen.blit(frame, self.rect)
