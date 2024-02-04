import pygame

class Animator:
    """
    Manages sprite sheets with many animations laid out in a
    grid format. 
    """
    def __init__(self, filepath, horiz_cnt, vert_cnt, scale_by=None):
        """
        Loads image, sets up surface, and initializes state.
        @filepath : Path to image file.
        @horiz_cnt : Number of sprite images on each row.
        @vert_cnt : Number of rows of sprite images.
        """
        self.surf = pygame.image.load(filepath).convert()
        # this line is to set up transparencies properly
        # RLEACCEL is some acceleration flag for software rendering
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.horiz_cnt = horiz_cnt
        self.vert_cnt = vert_cnt
        if scale_by:
            self.surf = pygame.transform.scale_by(self.surf, scale_by)

        full_size = self.surf.get_rect()
        self.rect = pygame.Rect(
            0, 0, full_size.w / horiz_cnt, full_size.h / vert_cnt
        )
        # this rect is set up such that it represents a single frame
        # of animation. this rect will get moved around between
        # frames as animations proceed.

        self.anims = dict()
        self.anim_curr = None
        self.anim_i = 0
        self.flip_x = False

    def registerAnim(self, name, *frames):
        """
        Add a new named animation with a list of frames that should
        be displayed in the animation routine.
        @name : String name of the animation.
        @frames : List of (x,y) pairs representing frames, where x is the
        column and y is the row. Starts at 0,0 in the upper left.
        """
        # note that *frames corresponds to the unpacking seen
        # in Player.__init__(). What this *frames represents
        # is a wildcard object, where every argument given after
        # `name` is packed into a list known as `frames`.
        self.anims[name] = frames

    def flipHoriz(self, flip):
        """
        Flips the entire spritesheet and marks itself as flipped
        or unflipped for frame rect calculations in `Animator.next()`.
        @flip : Marks whether the frames should be flipped or unflipped.
        `False` matches original orientation, `True` matches flipped
        orientation.
        """
        if flip != self.flip_x:
            self.flip_x = flip
            self.surf = pygame.transform.flip(self.surf, True, False)

    def change(self, name):
        """
        Switches the animation based on a name pre-registered 
        using `Animator.registerAnim()`.
        @name: Name of the animation to switch to.
        """
        self.anim_curr = name
        self.anim_i = 0

    def next(self):
        """
        Advances the animation forward a frame.
        """
        self.anim_i += 1
        anim_len = len(self.anims[self.anim_curr])
        if self.anim_i >= anim_len:
            self.anim_i = 0

        x, y = self.anims[self.anim_curr][self.anim_i]
        # if flipped, the whole sprite sheet is backwards
        # so recalculate the position of the frame 
        # from the opposite side
        x_mul = self.horiz_cnt - 1 - x if self.flip_x else x
        self.rect.x = self.rect.w * x_mul
        self.rect.y = self.rect.h * y
