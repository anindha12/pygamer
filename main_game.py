import pygame
import random


pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Color Changer")

current_color = (255, 0, 0)

done = False    
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
            current_color = (255, 0, 0)
            

        elif event.type == pygame.KEYUP:
            current_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


    screen.fill((0, 0, 0)) 

    pygame.draw.rect(screen, current_color, (50, 50, 100, 100))
    pygame.draw.circle(screen, current_color, (250, 100), 50)

    pygame.display.flip()

pygame.quit()
