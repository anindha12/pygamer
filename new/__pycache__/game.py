import random
import pygame 
import sys

# Screen size constants
SCREEN_W, SCREEN_H = 400, 400

# Custom event IDs
spritecolorchangevent = pygame.USEREVENT + 1
bgcolorchangevent = pygame.USEREVENT + 2

pygame.init()

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # Avoid a 0 velocity which makes the sprite get stuck
        self.velocity = [random.choice([-5, -4, -3, 3, 4, 5]), random.choice([-5, -4, -3, 3, 4, 5])]

    def update(self):
        self.rect.move_ip(self.velocity)
        boundary_collision = False

        if self.rect.left <= 0 or self.rect.right >= SCREEN_W:
            self.velocity[0] = -self.velocity[0]
            boundary_collision = True
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_H:
            self.velocity[1] = -self.velocity[1]
            boundary_collision = True

        if boundary_collision:
            pygame.event.post(pygame.event.Event(spritecolorchangevent, sprite=self))
            pygame.event.post(pygame.event.Event(bgcolorchangevent, sprite=self))

    def change_color(self, colors):
        self.image.fill(random.choice(colors))


def main():
    all_sprites = pygame.sprite.Group()
    sp1 = Sprite((255, 0, 0), 50, 50)

    sp1.rect.x = random.randint(0, SCREEN_W - sp1.rect.width)
    sp1.rect.y = random.randint(0, SCREEN_H - sp1.rect.height)
    all_sprites.add(sp1)

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("DVD Logo Example")
    bg_color = (0, 0, 0)

    exit_game = False
    clock = pygame.time.Clock()
    
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == spritecolorchangevent:
                event.sprite.change_color([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
            elif event.type == bgcolorchangevent:
                bg_color = random.choice([(255, 255, 255), (128, 128, 128), (0, 0, 0)])

        all_sprites.update()
        screen.fill(bg_color)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
