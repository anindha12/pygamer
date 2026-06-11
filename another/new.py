import pygame

pygame.init()
screen = pygame.display.set_mode((900, 450))

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.draw.circle(screen, (255, 0, 0), (100, 100), 50)
    pygame.draw.circle(screen, (0, 255, 0), (200, 100), 50, 2)

    pygame.display.flip()