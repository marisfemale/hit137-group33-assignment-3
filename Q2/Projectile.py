import pygame
from configs import projectile_width, projectile_height, blue, purple

class Projectile:
    def __init__(self, x, y, speed, damage, puncture=False, direction=1):
        self.rect = pygame.Rect(x, y, projectile_width, projectile_height)
        self.speed = speed * direction
        self.damage = damage
        self.puncture = puncture
        self.hit_count = 0
        self.direction = direction

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, blue, self.rect)

class BossProjectile:
    def __init__(self, x, y, vx, vy, damage):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.vx = vx
        self.vy = vy
        self.damage = damage

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, purple, self.rect.center, 5)
