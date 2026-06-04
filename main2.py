import pygame 

pygame.init()   
s_w, s_h = 600,600



display_surface = pygame.display.set_mode((s_w, s_h))
pygame.display.set_caption("Adding picture and Background Image")

background_image = pygame.transform.scale(pygame.image.load("download.jpeg").convert(), (s_w, s_h))

penguin_image = pygame.transform.scale(pygame.image.load("download.jpeg").convert_alpha(), (100, 100))
penguin_rect = penguin_image.get_rect()
penguin_rect.center = (s_w//2, s_h//2)


text = pygame.font.SysFont("Arial", 30).render("Hello, Pygame!", True, (text_color := (0, 0, 0)))
text_rect = text.get_rect()
text_rect.center = (s_w//2, 50)

def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display_surface.blit(background_image, (0, 0))
        display_surface.blit(penguin_image, penguin_rect)
        display_surface.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



if __name__ == "__main__":
    clock = pygame.time.Clock()
    game_loop()