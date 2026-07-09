# 1) Import required modules:
import math    
import random  
import pygame  

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

# 3) Initialize pygame using pygame.init().
pygame.init()
clock = pygame.time.Clock()  

# 4) Create the game window (screen) using pygame.display.set_mode(...).
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 5) Load background image using pygame.image.load('background.png').
try:
    background = pygame.image.load('background.png')
    icon = pygame.image.load('ufo.png')
    playerImg = pygame.image.load('player.png')
except pygame.error:
    print("Warning: Core graphical assets missing. Generating placeholders.")
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); background.fill((10, 10, 30))
    icon = pygame.Surface((32, 32)); icon.fill((0, 255, 255))
    playerImg = pygame.Surface((64, 64)); playerImg.fill((0, 255, 0))

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
        enemyImg.append(pygame.image.load('enemy.png'))  
    except pygame.error:
        surf = pygame.Surface((64, 64)); surf.fill((255, 0, 0))
        enemyImg.append(surf)
    enemyX.append(random.randint(0, SCREEN_WIDTH - 64))  
    enemyY.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))  
    enemyX_change.append(ENEMY_SPEED_X)                  
    enemyY_change.append(ENEMY_SPEED_Y)                  

# 10) Setup bullet (Correctly placed out of the loop):
try:
    bulletImg = pygame.image.load('bullet.png')
except pygame.error:
    bulletImg = pygame.Surface((16, 16)); bulletImg.fill((255, 255, 0))

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

# 12) Setup game-over text font using a larger font size.
over_font = pygame.font.Font('freesansbold.ttf', 64)
game_is_over = False  

# 13) Define helper functions:
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

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
            if event.key == pygame.K_SPACE and bullet_state == "ready" and not game_is_over:
                bulletX = playerX  
                fire_bullet(bulletX, bulletY)  

        if event.type == pygame.KEYUP:  
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0  

    # 17) Update player movement:
    if not game_is_over:
        playerX += playerX_change  
        playerX = max(0, min(playerX, SCREEN_WIDTH - 64))  

    # 18) Update enemy movement for each enemy:
    for i in range(num_of_enemies):
        if enemyY[i] > 340:  
            game_is_over = True
            for j in range(num_of_enemies):
                enemyY[j] = 2000  
            break

        enemyX[i] += enemyX_change[i]  
        
        if enemyX[i] <= 0 or enemyX[i] >= SCREEN_WIDTH - 64:  
            enemyX_change[i] *= -1  
            enemyY[i] += enemyY_change[i]  
            
        # Intersect validation parsing algorithms:
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY) and bullet_state == "fire":
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

    # 20) Draw the player, show the score, and update the display:
    if game_is_over:
        game_over_text()
    else:
        player(playerX, playerY)  
        
    show_score(textX, textY)      
    pygame.display.update()       
    clock.tick(60)                

pygame.quit()
