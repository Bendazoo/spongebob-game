import pygame

import actor

class Game:
    def __init__(self, width, height):
        """
        Start up Pygame and instantiate all
        relevant actors.
        @width : sets width of the screen
        @height : sets height of the screen
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))

        # this allows us to filter the event queue
        # for faster event processing
        pygame.event.set_allowed([
            pygame.QUIT,
            pygame.KEYDOWN
        ])

        self.player = actor.Player(0, 0)

        # colliders put right off-screen on both sides in order
        # to keep player from walking off the edge
        collider_left = actor.Collider(pygame.Rect(-1, 0, 1, height))
        collider_right = actor.Collider(pygame.Rect(width+1, 0, 1, height))
        self.collider_ground = actor.Collider(
            pygame.Rect(0, height-40, width, 40), color="chartreuse4"
        )

        # sprite groups allows us to perform batch
        # collision detection, as seen in Player.update()
        self.colliders = pygame.sprite.Group(
            collider_left, collider_right, self.collider_ground
        )

    def loop(self):
        """
        Primary game loop. This should be
        run perpetually until the game is
        over or is closed.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.screen.fill("black")

            self.player.processInput(pygame.key.get_pressed())
            self.player.update(self.colliders)
            self.player.render(self.screen)
            self.collider_ground.render(self.screen)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game(800, 600)
    game.loop()
