# 1) Import required modules:
import math
import os
import random
import sys
import pygame

# Automatically locate the execution folder to bypass directory mismatches
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_asset_path(filename):
    return os.path.join(SCRIPT_DIR, filename)


# 2) Create constants to control game settings:
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_START_X = 370
PLAYER_START_Y = 380
ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_SPEED_X = 4
ENEMY_SPEED_Y = 40
BULLET_SPEED_Y = 10
COLLISION_DISTANCE = 27

# 3) Initialize pygame and its audio engine components
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# 4) Create the game window (screen)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 5) Load background and game images using the local path tracker:
try:
    background = pygame.image.load(get_asset_path('background.png'))
    icon = pygame.image.load(get_asset_path('ufo.png'))
    playerImg = pygame.image.load(get_asset_path('player.png'))

    # LOAD AND RESIZE IMAGES TO FILL THE WHOLE SCREEN (800x500)
    raw_win_image = pygame.image.load(get_asset_path('images.jpeg')).convert_alpha()
    win_image = pygame.transform.scale(raw_win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    raw_lose_image = pygame.image.load(get_asset_path('abc.jpg')).convert_alpha()
    lose_image = pygame.transform.scale(raw_lose_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error:
    print(
        "Warning: Graphical assets missing or renamed. Generating placeholders."
    )
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((10, 10, 30))
    icon = pygame.Surface((32, 32))
    icon.fill((0, 255, 255))
    playerImg = pygame.Surface((64, 64))
    playerImg.fill((0, 255, 0))
    
    # Fallbacks will also fill the screen if files are missing
    win_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    win_image.fill((0, 150, 0))  # Full screen green
    lose_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    lose_image.fill((150, 0, 0))  # Full screen red

# Since they fill the screen, they start at top-left (0, 0)
screen_rect = (0, 0)

# Load your custom SFX clips safely
try:
    win_sound = pygame.mixer.Sound(get_asset_path('win.wav'))
    lose_sound = pygame.mixer.Sound(get_asset_path('gameover.wav'))
except pygame.error:
    print("Warning: Audio sound effects missing. Using silent stubs.")
    win_sound = None
    lose_sound = None

# Stream background score indefinitely
try:
    pygame.mixer.music.load(get_asset_path('background.wav'))
    pygame.mixer.music.play(-1)  # -1 signals persistent loop processing
except pygame.error:
    print("Warning: Background music asset missing.")

# 6) Set the game title and icon:
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(icon)

# 7) Setup the player:
playerX = PLAYER_START_X
playerY = PLAYER_START_Y
playerX_change = 0

# 8) Setup enemies using lists (multiple enemies):
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# 9) Use a loop to create each enemy:
for _i in range(num_of_enemies):
    try:
        enemyImg.append(pygame.image.load(get_asset_path('enemy.png')))
    except pygame.error:
        surf = pygame.Surface((64, 64))
        surf.fill((255, 0, 0))
        enemyImg.append(surf)
    enemyX.append(random.randint(0, SCREEN_WIDTH - 64))
    enemyY.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
    enemyX_change.append(ENEMY_SPEED_X)
    enemyY_change.append(ENEMY_SPEED_Y)

# 10) Setup bullet:
try:
    bulletImg = pygame.image.load(get_asset_path('bullet.png'))
except pygame.error:
    bulletImg = pygame.Surface((16, 16))
    bulletImg.fill((255, 255, 0))
bulletX = 0
bulletY = PLAYER_START_Y
bulletX_change = 0
bulletY_change = BULLET_SPEED_Y
bullet_state = "ready"

# 11) Setup score display:
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

game_is_over = False
game_won = False
sound_played = False  # Lock parameter preventing SFX loop triggers


# 13) Define helper functions:
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return distance < COLLISION_DISTANCE


# 14) Start the main game loop with running = True.
running = True
while running:

    # 15) Every frame inside the loop:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # 16) Handle events (keyboard and quit):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if (
                event.key == pygame.K_SPACE
                and bullet_state == "ready"
                and not game_is_over
            ):
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0

    # Check winning condition (9+ points reached)
    if score_value >= 9 and not game_is_over:
        game_is_over = True
        game_won = True
        for j in range(num_of_enemies):
            enemyY[j] = 2000

    # 17) Update player movement:
    if not game_is_over:
        playerX += playerX_change
        playerX = max(0, min(playerX, SCREEN_WIDTH - 64))

    # 18) Update enemy movement for each enemy:
    for i in range(num_of_enemies):
        # Check lose thresholds
        if enemyY[i] > 340 and enemyY[i] < 1000:
            game_is_over = True
            game_won = False
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= SCREEN_WIDTH - 64:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
        if (
            isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            and bullet_state == "fire"
        ):
            bulletY = PLAYER_START_Y
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, SCREEN_WIDTH - 64)
            enemyY[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)
        if not game_is_over:
            enemy(enemyX[i], enemyY[i], i)

    # 19) Update bullet movement:
    if bulletY <= 0:
        bulletY = PLAYER_START_Y
        bullet_state = "ready"
    elif bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # 20) Draw screens and manage state-dependent sound effects
    if game_is_over:
        # Clear out music tracks to let individual SFX clips capture focus
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        # Displays full-screen images now
        if game_won:
            screen.blit(win_image, screen_rect)
        else:
            screen.blit(lose_image, screen_rect)

        if not sound_played:
            if game_won and win_sound:
                win_sound.play()
            elif not game_won and lose_sound:
                lose_sound.play()
            sound_played = True
    else:
        player(playerX, playerY)
        show_score(textX, textY)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
