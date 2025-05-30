import pygame
import random
import os
from configs import *
from Player import Player
from Enemy import Enemy, Boss
from Projectile import Projectile
from Collectible import Collectible
from Utils import draw_text, show_menu, init_font, set_assets, get_asset_path

pygame.init()
pygame.font.init()
init_font()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(window_title)
clock = pygame.time.Clock()

shoot_sound = pygame.mixer.Sound(get_asset_path(shoot_sound_path))

background_images = [
    pygame.transform.scale(
        pygame.image.load(get_asset_path(path)).convert(),
        (screen_width, screen_height)
    )
    for path in background_paths
]

medkit_img = pygame.image.load(get_asset_path(medkit_path)).convert_alpha()
medkit_img = pygame.transform.scale(medkit_img, (20, 20))
extralife_img = pygame.image.load(get_asset_path(extralife_path)).convert_alpha()
extralife_img = pygame.transform.scale(extralife_img, (20, 20)) 

set_assets(medkit_img, extralife_img, 1)

def draw_hud(player):
    pygame.draw.rect(screen, red, (10, 10, hud_bar_width, hud_bar_height))
    pygame.draw.rect(screen, green, (10, 10, player.hp, hud_bar_height))
    draw_text(f"Score: {player.score}", 70, 5, screen)
    draw_text(f"Lives: {player.lives}", 200, 5, screen)

def run_game(player):
    global score_bonus
    level = 0
    projectiles = []
    enemies = []
    boss = None
    boss_projectiles = []
    collectible = None
    collect_timer = 0
    level_start = pygame.time.get_ticks()
    background_img = random.choice(background_images)
    enemy_timer = pygame.time.get_ticks()
    running = True

    while running:
        screen.blit(background_img, (0, 0))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    shoot_sound.play()
                    projectiles.append(player.shoot())

        player.move(keys)
        player.apply_gravity()
        player.draw(screen)
        draw_hud(player)

        now = pygame.time.get_ticks()
        spawn_delay = {'Easy': 6000, 'Normal': 5000, 'Hard': 3000}.get(difficulty, 5000)

        if now - enemy_timer > spawn_delay:
            enemies.append(Enemy(player))
            enemy_timer = now

        for proj in projectiles[:]:
            proj.update()
            for enemy in enemies[:]:
                if enemy.dying:
                    continue
                if proj.rect.colliderect(enemy.rect):
                    enemy.hp -= proj.damage
                    if not proj.puncture or proj.hit_count >= 1:
                        if proj in projectiles:
                            projectiles.remove(proj)
                        break
                    proj.hit_count += 1

            if boss and proj.rect.colliderect(boss.rect):
                boss.hp -= proj.damage
                if not proj.puncture or proj.hit_count >= 1:
                    if proj in projectiles:
                        projectiles.remove(proj)
                else:
                    proj.hit_count += 1

            if proj.rect.x > screen_width and proj in projectiles:
                projectiles.remove(proj)

        remaining = []
        for enemy in enemies:
            enemy.update()
            if enemy.rect.colliderect(player.rect) and not enemy.dying:
                player.hp -= 1
            if enemy.hp <= 0 and not enemy.dying:
                enemy.dying = True
                enemy.death_frame_index = 0
                enemy.frame_timer = 0
            if enemy.dying:
                if enemy.death_frame_index < len(enemy.death_frames):
                    remaining.append(enemy)
                else:
                    player.score += 2 + score_bonus
            else:
                remaining.append(enemy)
        enemies[:] = remaining

        for e in enemies: e.draw(screen)
        for p in projectiles: p.draw(screen)

        if boss:
            boss.update()
            boss.draw(screen)
            boss.cooldown -= 1
            shot = boss.shoot(player)
            if shot:
                boss_projectiles.append(shot)
            for bp in boss_projectiles[:]:
                bp.update()
                if bp.rect.colliderect(player.rect):
                    player.hp -= bp.damage
                    boss_projectiles.remove(bp)
                elif bp.rect.right < 0 or bp.rect.top < 0 or bp.rect.bottom > screen_height:
                    boss_projectiles.remove(bp)
            for bp in boss_projectiles:
                bp.draw(screen)

        if (now - level_start) > level_durations[level] * 1000 and not boss:
            if all(e.dying for e in enemies):
                boss = Boss(level + 1, player)

        if boss and boss.hp <= 0:
            player.score += 5 + score_bonus + score_bonus
            level += 1
            boss = None
            boss_projectiles.clear()
            if level >= 3:
                return
            level_start = pygame.time.get_ticks()

        if collect_timer <= 0 and not collectible:
            if random.randint(1, 100) <= 30:
                collectible = Collectible()
            collect_timer = 10000
        collect_timer -= clock.get_time()

        if collectible:
            collectible.draw(screen)
            if player.rect.colliderect(collectible.rect):
                collectible.apply(player)
                player.score += 1 + score_bonus + score_bonus
                collectible = None

        if player.hp <= 0:
            player.lives -= 1
            player.hp = 50
            if player.lives < 0:
                return

        pygame.display.flip()
        clock.tick(fps)

def main():
    global difficulty, score_bonus

    while True:
        choice = show_menu(["Start Game", "Quit"], "Main Menu", screen)
        if choice != "Start Game":
            break
        difficulty = show_menu(difficulty_levels, "Select Difficulty", screen)
        score_bonus = score_bonus_map.get(difficulty, 1)
        set_assets(medkit_img, extralife_img, score_bonus)

        player_class = show_menu(list(player_classes.keys()), "Select Class", screen)
        projectile_type = show_menu(projectile_types, "Select Projectile", screen)
        player = Player(player_class, projectile_type)
        run_game(player)

if __name__ == "__main__":
    main()
    pygame.quit()
