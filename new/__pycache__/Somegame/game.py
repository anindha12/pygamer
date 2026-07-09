import pygame
import random 

# Constants
screenwidth = 800
screenheight = 600
move_speed = 5
font_size = 72

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Sprite Collision")
font = pygame.font.Font(None, font_size)

# Setup Safe Background Fallback
try:
    bg_image = pygame.image.load("er.png").convert()
    bg_image = pygame.transform.scale(bg_image, (screenwidth, screenheight))
except:
    # Creating a solid fallback background manually to avoid hanging
    bg_image = pygame.Surface((screenwidth, screenheight))
    bg_image.fill((240, 240, 240)) 

# Sprite Class
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def move(self, x_change, y_change):
        # Keep sprite strictly inside screen boundaries
        self.rect.x = max(0, min(self.rect.x + x_change, screenwidth - self.rect.width))
        self.rect.y = max(0, min(self.rect.y + y_change, screenheight - self.rect.height))

# Setup Sprites
all_sprites = pygame.sprite.Group()

sprite1 = Sprite((255, 0, 0), 50, 50)
sprite1.rect.x = random.randint(0, screenwidth - sprite1.rect.width)
sprite1.rect.y = random.randint(0, screenheight - sprite1.rect.height)
all_sprites.add(sprite1)

sprite2 = Sprite((0, 255, 0), 50, 50)
sprite2.rect.x = random.randint(0, screenwidth - sprite2.rect.width)
sprite2.rect.y = random.randint(0, screenheight - sprite2.rect.height)
all_sprites.add(sprite2)

running = True
won = False
clock = pygame.time.Clock()

# Main Game Loop
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 2. Movement Logic (Only if game is not won yet)
    if not won:
        keys = pygame.key.get_pressed()
        x_change, y_change = 0, 0
        if keys[pygame.K_LEFT]:
            x_change = -move_speed
        if keys[pygame.K_RIGHT]:
            x_change = move_speed
        if keys[pygame.K_UP]:
            y_change = -move_speed
        if keys[pygame.K_DOWN]:
            y_change = move_speed

        sprite1.move(x_change, y_change)

        # 3. Collision Detection
        if pygame.sprite.collide_rect(sprite1, sprite2):
            won = True

        if pygame.sprite.collide_rect(sprite2, sprite1):
            all_sprites.remove(sprite2)  # Remove sprite2 from the group to stop drawing it

    # 4. Drawing and Rendering
    screen.blit(bg_image, (0, 0))
    all_sprites.draw(screen)

    # Display win message if collision happens
    if won:
        win_text = font.render("You Win!", True, pygame.Color("black"))
        text_x = screenwidth // 2 - win_text.get_width() // 2
        text_y = screenheight // 2 - win_text.get_height() // 2
        screen.blit(win_text, (text_x, text_y))

    pygame.display.flip()
    clock.tick(60)  # Locked back to stable 60 FPS

pygame.quit()
