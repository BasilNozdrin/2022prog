import math

import pygame as pg
import sys
from random import randint
import json


# https://pygame.readthedocs.io/en/latest/
# python -m pygame.docs


def exit_application():
    pg.quit()
    sys.exit()


class Button:
    def __init__(self, screen, x, y, text, font, color=(0, 43, 91), bg_color=(26, 95, 122), margin=10, on_press=None):
        self.screen = screen
        self.bg_color = bg_color

        self.img = font.render(text, True, color)
        self.text_rect = self.img.get_rect()
        self.rect = self.text_rect.copy()

        self.rect.left = x
        self.rect.top = y

        self.text_rect.left = x + margin
        self.text_rect.top = y + margin

        self.rect.width += margin * 2
        self.rect.height += margin * 2

        self.on_press = on_press

    def draw(self):
        pg.draw.rect(self.screen, self.bg_color, self.rect)
        self.screen.blit(self.img, self.text_rect)

    def press(self, event):
        if event.pos[0] < self.rect.left \
                or event.pos[0] > self.rect.left + self.rect.width \
                or event.pos[1] < self.rect.top \
                or event.pos[1] > self.rect.top + self.rect.height:
            return
        if self.on_press:
            self.on_press()


class Collider(pg.rect.Rect):
    colors = [(0, 150, 150), (0, 0, 0), (255, 0, 0), (0, 255, 0)]
    color_id = 0

    def __init__(self, logic, pos, speed):
        self.width = 50
        self.logic = logic
        super().__init__(0, 0, self.width, self.width)
        self.center = pos
        self.speed = speed
        self.color_id = Collider.color_id
        Collider.color_id += 1
        Collider.color_id %= len(Collider.colors)

    def update_position(self):
        x, y = self.center
        dx, dy = self.speed
        self.center = (x + dx, y + dy)
        self.check_screen_border_collision()
        for other in self.logic.colliders:
            self.check_collision_with(other)

    def check_screen_border_collision(self):
        x, y = self.center
        if x > self.logic.app.screen.get_width() or x < 0:
            self.speed = (self.speed[0] * -1, self.speed[1])
        if y > self.logic.app.screen.get_height() or y < 0:
            self.speed = (self.speed[0], self.speed[1] * -1)

    def check_collision_with(self, other):
        collision_tolerance = self.width * 0.1
        if self.colliderect(other):
            if abs(other.top - self.bottom) < collision_tolerance:
                buffer = self.speed[1]
                self.speed = (self.speed[0], other.speed[1])
                other.speed = (other.speed[0], buffer)
            if abs(other.bottom - self.top) < collision_tolerance:
                buffer = self.speed[1]
                self.speed = (self.speed[0], other.speed[1])
                other.speed = (other.speed[0], buffer)
            if abs(other.left - self.right) < collision_tolerance or \
                    abs(other.right - self.left) < collision_tolerance:
                buffer = self.speed[1]
                self.speed = (other.speed[0], self.speed[1])
                other.speed = (buffer, other.speed[1])

    def draw(self):
        pg.draw.rect(self.logic.app.screen, Collider.colors[self.color_id], self)


class Player:
    def __init__(self, logic):
        self.logic = logic
        self.pressed = False
        self.press = (0, 0)
        self.release = (0, 0)

    def update(self):
        pass

    def draw(self):
        if not self.pressed:
            return
        pg.draw.line(self.logic.app.screen, (200, 100, 100), self.press, self.release, 10)

    def check_event(self, event):
        if event.type == pg.MOUSEMOTION:
            if not self.pressed:
                return
            self.release = event.pos
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button != 1:
                return
            self.pressed = False
            speed = tuple(map(lambda p: (p[0] - p[1]) * 0.03, zip(self.release, self.press)))
            self.logic.colliders.append(Collider(self.logic, self.press, speed))
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.pressed = True
                self.press = event.pos
            elif event.button == 3:
                self.logic.colliders.pop(-1)


class MenuScene:
    def __init__(self, app):
        self.app = app

        self.play_button = Button(self.app.screen, self.app.screen.get_width() // 2, self.app.screen.get_height() // 3,
                                  'Play', self.app.font, on_press=self.play)
        self.reset_button = Button(self.app.screen, self.app.screen.get_width() // 2,
                                   self.app.screen.get_height() // 3 + 50,
                                   'Reset', self.app.font, on_press=self.reset)
        self.exit_button = Button(self.app.screen, self.app.screen.get_width() // 2,
                                  self.app.screen.get_height() // 3 + 100,
                                  'Exit', self.app.font, on_press=exit_application)
        self.buttons = [self.play_button, self.reset_button, self.exit_button]

    def play(self):
        self.app.scene = self.app.scenes[0]

    def reset(self):
        self.app.scenes[0].restart()
        self.app.scenes[0].draw()

    def update(self):
        pass

    def draw(self):

        for b in self.buttons:
            b.draw()

    def check_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.app.scene = self.app.scenes[0]
        if event.type == pg.MOUSEBUTTONDOWN:
            for b in self.buttons:
                b.press(event)


class GameScene:
    def __init__(self, app):
        self.app = app

        self.field_width = self.app.screen.get_width() // 20
        self.field_height = self.app.screen.get_height() // 20

        self.player = Player(self)
        self.colliders = []
        self.timer = 0

    def restart(self):
        self.player = Player(self)
        self.colliders = []
        self.timer = 0

    def update(self):
        # self.timer += self.app.dt
        self.player.update()
        for c in self.colliders:
            c.update_position()

    def draw(self):
        self.app.screen.fill((100, 100, 100))
        self.player.draw()
        for c in self.colliders:
            c.draw()

    def check_event(self, event):
        self.player.check_event(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.scene = self.app.scenes[1]


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        pg.display.set_caption('Snake')
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("exo2extrabold", 24)
        self.dt = 0.0

        self.scenes = []
        self.scenes.append(GameScene(self))
        self.scenes.append(MenuScene(self))

        # make GameLogic scene active
        self.scene = self.scenes[1]

    def update(self):
        self.scene.update()
        pg.display.flip()

        # dt is time passed since the last Clock.tick() call in milliseconds
        self.dt = self.clock.tick(60) * 0.001

    def draw(self):
        self.scene.draw()

    def check_events(self):
        for e in pg.event.get():
            self.scene.check_event(e)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    App().run()
