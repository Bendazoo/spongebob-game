import pygame
pygame.init()

from pygame.locals import (

    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Creating Window
SCREEN_LENGTH = 1200
SCREEN_WIDTH = 800
screen = pygame.display.set_mode([SCREEN_LENGTH,SCREEN_WIDTH])

# Initializing Game-Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
             if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False
    



    pygame.display.flip()

    






# Done! Time to quit.
pygame.quit()
