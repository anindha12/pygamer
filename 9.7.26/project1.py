import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Color Changer")

# You only need one Class template to create multiple independent sprites
class Sprite:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# CREATE ACTUAL INSTANCES (OBJECTS) FROM THE CLASS
# Sprite 1 (Left side, initially Red)
sprite1 = Sprite(50, 100, 100, 100, (255, 0, 0))
# Sprite 2 (Right side, initially Blue)
sprite2 = Sprite(250, 100, 100, 100, (0, 0, 255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Change the color of the specific object instances, not the class template
                sprite1.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                sprite2.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # DRAWING CODE INSIDE THE LOOP
    # 1. Fill the background first to clear the previous frame (Black)
    screen.fill((0, 0, 0))
    
    # 2. Draw your sprite objects onto the screen
    sprite1.draw(screen)
    sprite2.draw(screen)

    # 3. Refresh the display (Use update OR flip, you don't need both)
    pygame.display.update()
    
    # Cap the frame rate (better than pygame.time.delay for smooth performance)
    pygame.time.Clock().tick(60)
                
pygame.quit()
