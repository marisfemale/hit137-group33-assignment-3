import pygame
import os
import random
from configs import screen_width, screen_height, default_difficulty, enemy_width, enemy_height, green, red
from Utils import get_asset_path, load_sprite_sheet

class Enemy:
    def __init__(self, player):
        self.rect = pygame.Rect(0, screen_height - enemy_height, enemy_width, enemy_height)
        self.rect.x = 0 if random.choice([True, False]) else screen_width - enemy_width
        self.hp = {'Easy': 2, 'Normal': 3, 'Hard': 4}.get(default_difficulty, 3)
        self.direction = 1 if self.rect.x == 0 else -1
        self.speed = 2

        zombie_id = random.choice(["Zombie_1", "Zombie_2", "Zombie_3"])
        base_path = os.path.join("assets", "images", "spritesheets", "Zombie", zombie_id)

        walk_path = get_asset_path(os.path.join(base_path, "zombie_walk.png"))
        death_path = get_asset_path(os.path.join(base_path, "zombie_dead.png"))

        self.walk_frames = load_sprite_sheet(walk_path, 128, 128, 10)
        self.death_frames = load_sprite_sheet(death_path, 128, 128, 5)
        self.frames = self.walk_frames

        self.dying = False
        self.death_frame_index = 0
        self.death_timer = 0
        self.current_frame = 0
        self.frame_timer = 0
        self.facing_left = False
        self.player = player

    def update(self):
        if not self.dying:
            self.rect.x += self.speed * self.direction
            self.facing_left = self.direction == -1
            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
        else:
            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.frame_timer = 0
                if self.death_frame_index < len(self.death_frames) - 1:
                    self.death_frame_index += 1

    def draw(self, screen):
        if self.dying:
            if self.death_frame_index < len(self.death_frames):
                frame = self.death_frames[self.death_frame_index]
            else:
                return
        else:
            frame = self.frames[self.current_frame]

        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)

        screen.blit(frame, self.rect)

        if not self.dying:
            pygame.draw.rect(screen, green, (self.rect.x, self.rect.y - 5, self.hp * 10, 3))

class Boss(Enemy):
    def __init__(self, level, player):
        super().__init__(player)
        boss_base_path = os.path.join("assets", "images", "spritesheets", "Boss")
        idle_path = get_asset_path(os.path.join(boss_base_path, "boss_idle.png"))
        shoot_path = get_asset_path(os.path.join(boss_base_path, "boss_shoot.png"))

        self.idle_frames = load_sprite_sheet(idle_path, 128, 128, 5)
        self.shoot_frames = load_sprite_sheet(shoot_path, 128, 128, 8)

        self.current_frame = 0
        self.frame_timer = 0
        self.state = "idle"
        self.facing_left = True

        self.rect = pygame.Rect(screen_width - enemy_width - 10, screen_height - enemy_height, enemy_width, enemy_height)
        self.hp = 10 + level * 5
        self.cooldown = 60
        self.level = level
        self.player = player

    def shoot(self, player):
        if self.cooldown <= 0:
            self.cooldown = 60
            self.state = "shooting"
            self.current_frame = 0
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            vx = dx / dist * 5
            vy = dy / dist * 5
            from Projectile import BossProjectile
            return BossProjectile(self.rect.centerx, self.rect.centery, vx, vy, damage=2)
        return None

    def draw(self, screen):
        if self.state == "idle":
            frame = self.idle_frames[self.current_frame % len(self.idle_frames)]
        elif self.state == "shooting":
            frame = self.shoot_frames[self.current_frame % len(self.shoot_frames)]
        else:
            frame = self.idle_frames[0]

        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)

        frame_rect = frame.get_rect(center=self.rect.center)
        screen.blit(frame, frame_rect)

        bar_width = 100
        hp_ratio = self.hp / (10 + self.level * 5)
        pygame.draw.rect(screen, red, (self.rect.x, self.rect.y - 10, bar_width, 5))
        pygame.draw.rect(screen, green, (self.rect.x, self.rect.y - 10, int(bar_width * hp_ratio), 5))

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= 6:
            self.frame_timer = 0
            self.current_frame += 1
            if self.state == "idle":
                self.current_frame %= len(self.idle_frames)
            elif self.state == "shooting":
                if self.current_frame >= len(self.shoot_frames):
                    self.current_frame = 0
                    self.state = "idle"
