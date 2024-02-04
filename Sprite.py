import pygame 
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()


        self.surf = pygame.image.load("images/sp_2.png").convert_alpha()
        self.sponge_right = pygame.transform.scale_by(self.surf, 3)
        self.rect = self.surf.get_rect()
        self.sponge_dir = self.sponge_right

    def movement(self, pressed_keys):
        self.sponge_left = pygame.transform.flip(self.sponge_right, True, False)

        if pressed_keys[K_w]:
            self.rect.move_ip(0,-1)
        if pressed_keys[K_s]:
            self.rect.move_ip(0,1)
        if pressed_keys[K_a]:
            self.rect.move_ip(-1,0)
            self.sponge_dir = self.sponge_left
        if pressed_keys[K_d]:
            self.rect.move_ip(1,0)
            self.sponge_dir = self.sponge_right

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1200:
            self.rect.right = 1200
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 800:
            self.rect.bottom = 800


    



        
