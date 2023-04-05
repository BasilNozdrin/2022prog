from Settings import *
import pygame as pg
import pathlib
from random import randrange


class SpriteUnit(pg.sprite.Sprite):
    def __init__(self, handler, x, y):
        self.handler = handler
        super().__init__(handler.group)
        self.image_ind = randrange(len(handler.images))
        self.image = handler.images[self.image_ind]
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.angle = 0
        self.rot_vel = randrange(-SPEED, SPEED)
        self.vel_x, self.vel_y = randrange(-SPEED, SPEED), randrange(-SPEED, SPEED)

    def translate(self):
        self.x += self.vel_x * self.handler.app.dt
        self.y += self.vel_y * self.handler.app.dt
        if self.x < 0 or self.x > WIN_W:
            self.vel_x *= -1
        if self.y < 0 or self.y > WIN_H:
            self.vel_y *= -1

    def rotate(self):
        self.angle += self.rot_vel * self.handler.app.dt
        self.image = pg.transform.rotate(self.handler.images[self.image_ind], self.angle)
        self.rect = self.image.get_rect()

    def update(self):
        self.translate()
        self.rotate()
        self.rect.center = self.x, self.y


class SpriteHandler:
    def __init__(self, app):
        self.app = app
        self.images = self.load_images()
        self.group = pg.sprite.Group()
        self.sprites = [SpriteUnit(self, WIN_W // 2, WIN_H // 2)]

    def add_sprite(self, x, y):
        for i in range(NUM_SPRITES_PER_CLICK):
            self.sprites.append(SpriteUnit(self, x, y))

    def del_sprite(self):
        for i in range(NUM_SPRITES_PER_CLICK):
            if len(self.sprites):
                sprite = self.sprites.pop()
                sprite.kill()

    def load_images(self):
        paths = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        return [pg.image.load(str(path)).convert_alpha() for path in paths]

    def update(self):
        self.group.update()

    def draw(self):
        self.group.draw(self.app.screen)

    def on_mouse_press(self):
        mouse_button = pg.mouse.get_pressed()
        if mouse_button[0]:
            x, y = pg.mouse.get_pos()
            self.add_sprite(x, y)
        elif mouse_button[2]:
            self.del_sprite()

