import pygame as pg
from .. import constants as c
from .. import setup

class Powerup(pg.sprite.Sprite):
    """Base class for all powerup_group"""
    def __init__(self, x, y):
        super(Powerup, self).__init__()

    def setup_powerup(self, x, y, name, setup_frames):
        """This separate setup function allows me to pass a different
        setup_frames method depending on what the powerup is"""
        self.sprite_sheet = setup.GFX['1-up']
        self.frames = []
        self.frame_index = 0
        setup_frames()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.state = c.REVEAL
        self.y_vel = -1
        self.x_vel = 0
        self.direction = c.RIGHT
        self.box_height = y
        self.gravity = 1
        self.max_y_vel = 8
        self.animate_timer = 0
        self.name = name

    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)
        image = pg.transform.scale(image,
                                   (int(rect.width*c.SIZE_MULTIPLIER),
                                    int(rect.height*c.SIZE_MULTIPLIER)))
        return image

    def update(self, game_info, *args):
        """Updates powerup behavior"""
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state()

    def handle_state(self):
        pass

    def revealing(self, *args):
        """Action when powerup leaves the coin box or brick"""
        self.rect.y += self.y_vel
        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.y_vel = 0
            self.state = c.RESTING

class LifeMushroom(Powerup):
    def __init__(self, x, y, name='1up_mushroom'):
        super(LifeMushroom, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)

    def setup_frames(self):
        self.frames.append(self.get_image(0, 0, 16, 16))

    def handle_state(self):
        if self.state == c.REVEAL:
            self.revealing()

    def revealing(self):
        self.rect.y += self.y_vel
        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.y_vel = 0
            self.state = c.RESTING