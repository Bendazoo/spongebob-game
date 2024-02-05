import pygame.locals as keys

class PlayerState:
    """
    Base class for the player's state machine.
    """
    def __init__(self, parent, anim=None, flip=False):
        """
        Initialize parent (the player), an animation
        to switch to on entry for the state, and
        the horizontal orientation.
        @parent : Reference to the player object.
        @anim : Name of the animation to play on
        entry, if any.
        @flip : Horizontal flip for the animation
        as a boolean.
        """
        self.parent = parent
        self.flip = flip
        if anim:
            self.parent.anim.change(anim)
        self.parent.anim.flipHoriz(flip)

    def processInput(self, pressed):
        """
        Stub method for processing input from the
        keyboard. Passes because some states may
        block input.
        @pressed : A sequence of booleans; one for each key.
        """
        pass
    
    def update(self):
        """
        Stub method for a frame-by-frame update. 
        Passes because some states may only process 
        input without updating.
        """
        pass
    
class StandingState(PlayerState):
    """
    State for when the player is standing still.
    """
    def __init__(self, parent, flip=False):
        """
        Initialize and set the horizontal speed
        to be still.
        @parent : Reference to the player object.
        @flip : Horizontal flip for the animation
        as a boolean.
        """
        super().__init__(parent, "stand", flip)
        self.parent.kinem.vel_x = 0

    def processInput(self, pressed):
        """
        If left is pressed, the player should begin
        running to the left (non-flipped is facing
        right so flip equals True here). Otherwise
        if right is pressed, begin running to the
        right.
        @pressed : A sequence of booleans; one for each key.
        """
        if pressed[keys.K_LEFT]:
            return RunningState(self.parent, flip=True)
        if pressed[keys.K_RIGHT]:
            return RunningState(self.parent, flip=False)
    
class RunningState(PlayerState):
    """
    State for when the player is running along the ground.
    """
    def __init__(self, parent, flip=False):
        """
        Initialize and set the horizontal speed
        to be moving in the appropriate direction.
        @parent : Reference to the player object.
        @flip : Horizontal direction for the animation
        and movement as a boolean. True for right, False
        for left.
        """
        super().__init__(parent, "run", flip)
        self.parent.kinem.vel_x = -5 if flip else 5

    def processInput(self, pressed):
        """
        If moving left and left key is released, switch
        to standing still. Else if moving right and right
        key is released, switch to standing still.
        @pressed : A sequence of booleans; one for each key.
        """
        if self.flip and not pressed[keys.K_LEFT]:
            return StandingState(self.parent, self.flip)
        if not self.flip and not pressed[keys.K_RIGHT]:
            return StandingState(self.parent, self.flip)
        if pressed[keys.K_SPACE] and not pressed[keys.K_LEFT] and not pressed[keys.K_RIGHT]:
            return JumpingState(self.parent, self.flip)

class JumpingState(PlayerState):
    """
    State for when the player is jumping.
    """
    def __init__(self, parent, flip=False):
        """
        Initialize and set the vertical speed
        to be moving in the appropriate direction.
        @parent : Reference to the player object.
        @flip : Horizontal direction for the animation
        and movement as a boolean. True for right, False
        for left.
        """
        super().__init__(parent, "jump", flip)
    
    def processInput(self, pressed):
        """
        If in air and space key is released, switch
        to falling.
        """
        if self.flip and not pressed[keys.K_SPACE]:
            return FallingState(self.parent, self.flip)
        if not self.flip and not pressed[keys.K_SPACE]:
            return FallingState(self.parent, self.flip)

class FallingState(PlayerState):
    """
    State for when the player is falling.
    """
    def __init__(self, parent, flip=False):
        """
        Initialize and set vertical speed
        to be moving in the appropriate direction.
        @parent : Reference to the player object.
        @flip : Horizontal direction for the animation
        and movement as a boolean. True for right, False
        for left.
        """
        super().__init__(parent, "fall", flip)

    def processInput(self, pressed):
        """
        If on the ground and nothing is pressed,
        switch to standing state.
        Else if on the ground and space key is pressed,
        switch to jumping state.
        Else if on the ground and left key is pressed,
        switch to running state.
        Else if on the ground and right key is pressed,
        switch to running state.
        """
        if not pressed[keys.K_SPACE] or not pressed[keys.K_LEFT] or not pressed[keys.K_RIGHT]:
            return StandingState(self.parent, self.flip)
        if pressed[keys.K_SPACE]:
            return JumpingState(self.parent, self.flip)
        if not self.flip and pressed[keys.K_LEFT]:
            return RunningState(self.parent, self.flip)
        if self.flip and pressed[keys.K_RIGHT]:
            return RunningState(self.parent, self.flip)
