import pygame

import state
from anim import Animator

class Kinematics:
    """
    Class that handles basic physics
    calculations for actors (or anything
    with a rect controlling its position).
    """
    def __init__(self, parent):
        """
        Initializes parent, velocity, and
        acceleration in 2D. If you want to
        change these values, set them
        directly:
        @vel_x controls x velocity.
        @vel_y controls y velocity.
        @accel_x controls x acceleration.
        @accel_y controls y acceleration.

        @parent : Anything with a rect attribute controlling
        their position. Any updates and reversions
        will take place on this object's rect.
        """
        self.parent = parent
        self.vel_x = 0
        self.vel_y = 0
        self.accel_x = 0
        self.accel_y = 0

    def updateX(self):
        """
        Update x velocity based on acceleration,
        update x position in parent based on velocity.
        """
        self.vel_x += self.accel_x
        self.old_x = self.parent.rect.x
        self.parent.rect.x += self.vel_x

    def updateY(self):
        """
        Update x velocity based on acceleration,
        update x position in parent based on velocity.
        """
        self.vel_y += self.accel_y
        self.old_y = self.parent.rect.y
        self.parent.rect.y += self.vel_y

    def revertX(self):
        """
        Revert parent's x position to previous state
        with no velocity.
        """
        self.vel_x = 0
        self.parent.rect.x = self.old_x

    def revertY(self):
        """
        Revert parent's y position to previous state
        with no velocity.
        """
        self.vel_y = 0
        self.parent.rect.y = self.old_y

class Player(pygame.sprite.Sprite):
    """
    Class for the player's sprite. Contains components
    for animation and kinematics as well as specialized
    state objects.
    """
    def __init__(self, x, y):
        """
        Sets up animator, kinematic, and state components.
        @x : Starting x location
        @y : Starting y location
        """
        super().__init__()

        # scale by 3 because the original sprites are small
        self.anim = Animator("player.png", 5, 1, scale_by=3)
        # animations start at 0 and go until 4, all on the 0th row
        # may be different depending on your sprite sheet
        self.anim.registerAnim("stand", (0, 0))
        # this produces [(1,0), (1,0), (1,0)... (0,0), (0,0)...]
        # so on and so forth. 20 frames of animation total
        run_frames = [(1,0)]*6 + [(0,0)]*4 + [(2,0)]*6 + [(0,0)]*4
        # the * syntax here means "unpack". basically unrolling
        # a list into a series of sequential arguments
        self.anim.registerAnim("run", *run_frames)
        self.anim.registerAnim("jump", (3, 0))
        self.anim.registerAnim("fall", (4, 0))
        self.rect = pygame.Rect(
            x, y, self.anim.rect.w, self.anim.rect.h
        )

        self.kinem = Kinematics(self)
        self.kinem.accel_y = 0.5  # this is the gravity force right here
        # note that downward y is actually positive! negative y is upward

        # initial state = Standing
        self.state = state.StandingState(self)

    def delgateToState(self, method, *args):
        """
        Helper function for functionality controlled
        by state objects. Updates the state if need be.
        @method : Method to call on the state object.
        Should usually be some variation of `self.state.####`.
        @args : Any number of arguments that should be
        passed into the corresponding state method.
        """
        new_state = method(*args)
        if new_state:
            self.state = new_state

    def processInput(self, pressed):
        """
        Process input using the `pygame.key.get_pressed` method.
        @pressed : A sequence of booleans; one for each key. Should
        be whatever comes out of `pygame.key.get_pressed` (some sort
        of ScanCodeGenerator thing).
        """
        self.delgateToState(self.state.processInput, pressed)

    def update(self, colliders):
        """
        Updates state of the player and performs movement.
        Also checks for collisions and reverts movement
        if need be.
        @colliders : Sprite group of walls/floors. Should
        be some variation of `pygame.sprite.Group`.
        """
        self.delgateToState(self.state.update)

        self.kinem.updateX()
        if pygame.sprite.spritecollideany(self, colliders):
            self.kinem.revertX()
        self.kinem.updateY()
        if pygame.sprite.spritecollideany(self, colliders):
            self.kinem.revertY()

    def render(self, surf):
        """
        Renders the current state of the player to the
        provided Surface.
        @surf : Surface to write to (usually the main screen).
        """
        surf.blit(
            self.anim.surf, self.rect, area=self.anim.rect
        )
        self.anim.next()

class Collider(pygame.sprite.Sprite):
    """
    Stationary sprites meant to primary be used for walls and floors.
    """
    def __init__(self, rect, color=None):
        """
        @rect : Position and dimensions of the collider.
        Should be a `pygame.Rect`.
        @color : Color to fill for the collider. If `None`,
        will be transparent.
        """
        super().__init__()
        self.rect = rect
        self.color = color

    def render(self, surf):
        """
        Renders the collider to a surface. Only useful
        if the collider is non-transparent.
        @surf : Surface to write to (usually the main screen).
        """
        if self.color:
            pygame.draw.rect(surf, self.color, self.rect)
