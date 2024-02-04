import pygame
import Sprite

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,

)
SCREEN_LENGTH = 1200
SCREEN_WIDTH = 800
screen = pygame.display.set_mode([SCREEN_LENGTH, SCREEN_WIDTH])

# Creating Sprite Class
player = Sprite.Player()

pygame.init()

# Creating Window

# Initializing Game-Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
             if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    player.movement(pressed_keys)

    screen.fill((0, 0, 0))
    screen.blit(player.surf, player.rect)

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
