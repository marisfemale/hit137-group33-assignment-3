import pygame
import random
import os
pygame.init()

shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")

FPS = 30
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background_img = pygame.image.load("assets/images/background.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))


pygame.display.set_caption("Side Scroller Shooter")
difficulty = 'Normal'
score_bonus = {'Easy': 0, 'Normal': 1, 'Hard': 2}.get(difficulty, 1)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)

font = pygame.font.SysFont("Arial", 24)
highscore_file = "highscores.txt"

LEVEL_DURATIONS = [30, 45, 60]
PROJECTILE_TYPES = ["Fast", "Strong", "Puncture"]
PLAYER_CLASSES = {
    "Tank": {"speed": 3, "jump": 10, "lives": 3},
    "Jumper": {"speed": 5, "jump": 15, "lives": 3},
    "Speedster": {"speed": 7, "jump": 10, "lives": 3},
    "Extra Life": {"speed": 5, "jump": 10, "lives": 5}
}

PLAYER_WIDTH, PLAYER_HEIGHT = 30, 40
player_img = pygame.image.load("assets/images/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
ENEMY_WIDTH, ENEMY_HEIGHT = 30, 30
PROJECTILE_WIDTH, PROJECTILE_HEIGHT = 10, 5

def load_sprite_sheet(path, frame_width, frame_height, num_frames):
    sheet = pygame.image.load("assets/images/spritesheets/Tank/Walk.png").convert_alpha()
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT))
        frames.append(frame)
    return frames

def draw_text(text, x, y):
    screen.blit(font.render(text, True, WHITE), (x, y))

def show_menu(options, title):
    while True:
        screen.fill(BLACK)
        draw_text(title, WIDTH//2 - 100, 50)
        for i, opt in enumerate(options):
            draw_text(f"{i + 1}. {opt}", WIDTH//2 - 100, 100 + i * 40)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_1
                    if index < len(options):
                        return options[index]

def pause_menu():
    choice = show_menu(["Resume", "Main Menu", "Quit"], "Game Paused")
    if choice == "Resume":
        return "resume"
    elif choice == "Main Menu":
        return "menu"
    elif choice == "Quit":
        pygame.quit()
        exit()

class Player:
    def __init__(self, cls, proj_type):
        self.rect = pygame.Rect(50, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vx = PLAYER_CLASSES[cls]["speed"]
        self.vy = 0
        self.on_ground = True
        self.jump_strength = PLAYER_CLASSES[cls]["jump"]
        self.hp = 50
        self.lives = PLAYER_CLASSES[cls]["lives"]
        self.score = 0
        self.class_type = cls
        self.projectile_type = proj_type

    def move(self, keys):
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.vx
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.vx
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = -self.jump_strength
            self.on_ground = False

    def apply_gravity(self):
        self.vy += 1
        self.rect.y += self.vy
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.on_ground = True
            self.vy = 0

    def shoot(self):
        shoot_sound.play()      #EDIT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        speed = 10 if self.projectile_type == "Fast" else 5
        damage = 2 if self.projectile_type == "Strong" else 1
        puncture = self.projectile_type == "Puncture"
        return Projectile(self.rect.right, self.rect.centery, speed, damage, puncture)

    def draw(self):
        screen.blit(player_img, self.rect)

class Projectile:
    def __init__(self, x, y, speed, damage, puncture=False):
        self.rect = pygame.Rect(x, y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
        self.speed = speed
        self.damage = damage
        self.puncture = puncture
        self.hit_count = 0

    def update(self):
        self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH - ENEMY_WIDTH - 10, HEIGHT - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.hp = {'Easy': 2, 'Normal': 3, 'Hard': 4}.get(difficulty, 3)
        self.direction = -1

    def update(self):
        self.rect.x += self.direction * 2
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction = 1
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.direction = -1

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 5, self.hp * 10, 3))

class Boss(Enemy):
    def __init__(self, level):
        super().__init__()
        self.rect = pygame.Rect(WIDTH - ENEMY_WIDTH - 10, HEIGHT - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.hp = 10 + level * 5
        self.cooldown = 60

    def shoot(self, player):
        if self.cooldown <= 0:
            self.cooldown = 60
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = max(1, (dx**2 + dy**2)**0.5)
            return BossProjectile(self.rect.centerx, self.rect.centery, dx/dist*5, dy/dist*5, 2)
        return None

class BossProjectile:
    def __init__(self, x, y, vx, vy, damage):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.vx = vx
        self.vy = vy
        self.damage = damage

    def update(self):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

class Collectible:
    def __init__(self):
        self.types = [("Health", 30), ("ExtraLife", 5), ("Bonus", 40)]
        pool = [t for t, chance in self.types for _ in range(chance)]
        self.kind = random.choice(pool)
        self.rect = pygame.Rect(random.randint(100, WIDTH - 100), HEIGHT - 30, 20, 20)

    def apply(self, player):
        if self.kind == "Health":
            player.hp = min(50, player.hp + 10)
        elif self.kind == "ExtraLife":
            player.lives += 1
        elif self.kind == "Bonus":
            player.score += 1 + score_bonus

    def draw(self):
        color = GREEN if self.kind == "Health" else YELLOW if self.kind == "Bonus" else WHITE
        pygame.draw.rect(screen, color, self.rect)

def draw_hud(player):
    pygame.draw.rect(screen, RED, (10, 10, 50, 10))
    pygame.draw.rect(screen, GREEN, (10, 10, player.hp, 10))
    draw_text(f"Score: {player.score}", 70, 5)
    draw_text(f"Lives: {player.lives}", 200, 5)

def handle_projectiles(projectiles, enemies, player, boss):
    for proj in projectiles[:]:
        proj.update()
        for enemy in enemies[:]:
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
        if proj.rect.x > WIDTH and proj in projectiles:
            projectiles.remove(proj)

def handle_enemies(enemies, player):
    remaining = []
    for enemy in enemies:
        enemy.update()
        if enemy.rect.colliderect(player.rect):
            player.hp -= 1
        if enemy.hp > 0:
            remaining.append(enemy)
        else:
            player.score += 2 + score_bonus
    enemies[:] = remaining

def handle_boss(boss, player, boss_projectiles):
    if boss:
        boss.cooldown -= 1
        shot = boss.shoot(player)
        if shot:
            boss_projectiles.append(shot)
        for bp in boss_projectiles[:]:
            bp.update()
            if bp.rect.colliderect(player.rect):
                player.hp -= bp.damage
                boss_projectiles.remove(bp)
            elif bp.rect.right < 0 or bp.rect.top < 0 or bp.rect.bottom > HEIGHT:
                boss_projectiles.remove(bp)

def end_game(player, win):
    screen.fill(BLACK)
    message = "You Win!" if win else "Game Over"
    draw_text(message, WIDTH//2 - 50, HEIGHT//2 - 20)
    draw_text(f"Score: {player.score}", WIDTH//2 - 50, HEIGHT//2 + 10)
    draw_text("Enter Name (optional):", WIDTH//2 - 80, HEIGHT//2 + 40)
    pygame.display.flip()

    name = ""
    entering = True
    while entering:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 10 and event.unicode.isprintable():
                    name += event.unicode
        screen.fill(BLACK)
        draw_text(message, WIDTH//2 - 50, HEIGHT//2 - 20)
        draw_text(f"Score: {player.score}", WIDTH//2 - 50, HEIGHT//2 + 10)
        draw_text("Enter Name (optional):", WIDTH//2 - 80, HEIGHT//2 + 40)
        draw_text(name, WIDTH//2 - 50, HEIGHT//2 + 70)
        pygame.display.flip()
        clock.tick(FPS)

    with open(highscore_file, "a") as file:
        file.write(f"{name if name else 'Anonymous'}:{player.score}\n")
    draw_text("Press Enter to return to Main Menu", WIDTH//2 - 120, HEIGHT//2 + 100)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def show_highscores():
    screen.fill(BLACK)
    draw_text("Highscores:", WIDTH//2 - 50, 50)
    try:
        with open(highscore_file, "r") as file:
            scores = [line.strip().split(":") for line in file.readlines()]
            scores = sorted(scores, key=lambda x: int(x[1]), reverse=True)
    except FileNotFoundError:
        scores = []
    for i, (name, score) in enumerate(scores[:10]):
        draw_text(f"{i+1}. {name}: {score}", WIDTH//2 - 70, 100 + i * 25)
    draw_text("Press any key to return", WIDTH//2 - 90, HEIGHT - 40)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                waiting = False
        clock.tick(FPS)

def run_game(player):
    level = 0
    projectiles = []
    enemies = []
    boss = None
    boss_projectiles = []
    collectible = None
    collect_timer = 0
    level_start = pygame.time.get_ticks()
    enemy_timer = pygame.time.get_ticks()
    running = True

    while running:
        screen.blit(background_img, (0, 0))
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    projectiles.append(player.shoot())
                elif event.key == pygame.K_ESCAPE:
                    pause_result = pause_menu()
                    if pause_result == "menu":
                        return

        player.move(keys)
        player.apply_gravity()
        player.draw()
        draw_hud(player)

        now = pygame.time.get_ticks()
        spawn_delay = {'Easy': 6000, 'Normal': 5000, 'Hard': 3000}.get(difficulty, 5000)
        if now - enemy_timer > spawn_delay:
            enemies.append(Enemy())
            enemy_timer = now

        handle_projectiles(projectiles, enemies, player, boss)
        handle_enemies(enemies, player)

        for e in enemies:
            e.draw()
        for p in projectiles:
            p.draw()

        if boss:
            pygame.draw.rect(screen, PURPLE, boss.rect)
            pygame.draw.rect(screen, GREEN, (boss.rect.x, boss.rect.y - 5, boss.hp * 10, 3))
            handle_boss(boss, player, boss_projectiles)
            for bp in boss_projectiles:
                bp.draw()

        if (now - level_start) > LEVEL_DURATIONS[level] * 1000 and not boss:
            if not enemies:
                boss = Boss(level + 1)

        if boss and boss.hp <= 0:
            player.score += 5 + score_bonus + score_bonus
            level += 1
            boss = None
            boss_projectiles.clear()
            if level < 3:
                choice = show_menu(["Continue to next level", "Return to Main Menu"], "Continue or Quit")
                if choice != "Continue to next level":
                    return
            level_start = pygame.time.get_ticks()

        if collect_timer <= 0 and not collectible:
            if random.randint(1, 100) <= 30:
                collectible = Collectible()
            collect_timer = 10000
        collect_timer -= clock.get_time()

        if collectible:
            collectible.draw()
            if player.rect.colliderect(collectible.rect):
                collectible.apply(player)
                player.score += 1 + score_bonus + score_bonus
                collectible = None

        if player.hp <= 0:
            player.lives -= 1
            player.hp = 50
            if player.lives < 0:
                return end_game(player, False)

        if level >= 3:
            return end_game(player, True)

        pygame.display.flip()
        clock.tick(FPS)

def main():
    while True:
        choice = show_menu(["Start Game", "View Highscores", "Quit"], "Main Menu")
        if choice == "Quit" or choice is None:
            break
        elif choice == "View Highscores":
            show_highscores()
        elif choice == "Start Game":
            global difficulty
            difficulty = show_menu(["Easy", "Normal", "Hard"], "Select Difficulty")
            global score_bonus
            score_bonus = {'Easy': 0, 'Normal': 1, 'Hard': 2}.get(difficulty, 1)
            player_class = show_menu(list(PLAYER_CLASSES.keys()), "Select Class")
            if not player_class:
                continue
            projectile_type = show_menu(PROJECTILE_TYPES, "Select Projectile")
            if not projectile_type:
                continue
            player = Player(player_class, projectile_type)
            run_game(player)

if __name__ == "__main__":
    main()
    pygame.quit()