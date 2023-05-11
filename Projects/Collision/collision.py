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


class Bullet:
    def __init__(self, logic, pos, direction):
        self.logic = logic
        self.pos = pos
        self.direction = direction
        self.speed = 100
        x, y = self.pos
        xx, yy = self.direction
        delta = (xx - x, yy - y)
        delta_len = (delta[0] ** 2 + delta[1] ** 2) ** 0.5
        self.step = tuple(map(lambda a: self.speed * a / delta_len, delta))
        self.sprite = pg.image.load('bullet2.svg')
        # self.angle = -90 - math.degrees(math.atan2(self.step[1], self.step[0]))
        # self.sprite = pg.transform.rotate(self.sprite, self.angle)
        self.rect = self.sprite.get_rect()
        self.rect.topleft = self.pos

    def update(self):
        self.pos = tuple(map(lambda a: a[0]+a[1], zip(self.pos, self.step)))
        self.rect.topleft = self.pos
        if self.pos[0] > self.logic.app.screen.get_width():
            self.logic.bullets.pop(0)
        if self.pos[1] > self.logic.app.screen.get_height():
            self.logic.bullets.pop(0)

    def draw(self):
        self.logic.app.screen.blit(self.sprite, self.rect)



class Player:
    def __init__(self, logic, x, y):
        self.logic = logic
        self.pos = (x, y)
        self.aim = (x, y)
        self.offset = (-150, -150)
        self.angle = 0
        self.velocity = (0, 0)
        self.speed = 10
        self.sprite = pg.image.load('character.svg')
        self.sprite = pg.transform.scale(self.sprite, (100, 100))
        self.rect = self.sprite.get_rect()
        self.rect.topleft = tuple(map(lambda a: a[0] + a[1], zip(self.pos, self.offset)))

    def update(self):
        self.pos = tuple(map(lambda a: a[0] + a[1], zip(self.pos, self.velocity)))
        self.rect.topleft = tuple(map(lambda a: a[0] + a[1], zip(self.pos, self.offset)))
        # self.rect.left = self.pos[0] + self.offset[0]
        # self.rect.top = self.pos[1] + self.offset[1]
        # dx = self.rect.left - self.aim[0]
        # dy = self.rect.top - self.aim[1]
        # self.angle = -90 - math.degrees(math.atan2(dy, dx))
        # print(self.angle)

    def draw(self):
        self.logic.app.screen.blit(self.sprite, self.rect)
        # rotated_image = pg.transform.rotate(self.sprite, self.angle)
        # new_rect = rotated_image.get_rect()
        # new_rect.center = self.rect.center
        # self.logic.app.screen.blit(rotated_image, new_rect)

    def start_move_up(self):
        self.velocity = (self.velocity[0], -self.speed)

    def start_move_left(self):
        self.velocity = (-self.speed, self.velocity[1])

    def start_move_down(self):
        self.velocity = (self.velocity[0], self.speed)

    def start_move_right(self):
        self.velocity = (self.speed, self.velocity[1])

    def stop_move_up(self):
        if self.velocity[1] < 0:
            self.velocity = (self.velocity[0], 0)

    def stop_move_left(self):
        if self.velocity[0] < 0:
            self.velocity = (0, self.velocity[1])

    def stop_move_down(self):
        if self.velocity[1] > 0:
            self.velocity = (self.velocity[0], 0)

    def stop_move_right(self):
        if self.velocity[0] > 0:
            self.velocity = (0, self.velocity[1])

    def check_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP or event.key == ord('w'):
                self.start_move_up()
            if event.key == pg.K_DOWN or event.key == ord('s'):
                self.start_move_down()
            if event.key == pg.K_LEFT or event.key == ord('a'):
                self.start_move_left()
            if event.key == pg.K_RIGHT or event.key == ord('d'):
                self.start_move_right()
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP or event.key == ord('w'):
                self.stop_move_up()
            if event.key == pg.K_DOWN or event.key == ord('s'):
                self.stop_move_down()
            if event.key == pg.K_LEFT or event.key == ord('a'):
                self.stop_move_left()
            if event.key == pg.K_RIGHT or event.key == ord('d'):
                self.stop_move_right()
        elif event.type == pg.MOUSEMOTION:
            self.aim = event.pos
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.logic.bullets.append(
                Bullet(self.logic, tuple(map(lambda a: a[0] + a[1], zip(self.pos, self.offset))), event.pos))
            print(event)


class Asteroid:
    def __init__(self, logic, pos):
        self.logic = logic
        self.sprite = pg.image.load('cherry.svg')
        self.sprite = pg.transform.scale(self.sprite, (200, 200))
        self.rect = self.sprite.get_rect()
        self.rect.center = pos
        self.speed = (10, 10)
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 120, 255)]
        self.color_id = 0

    def update(self):
        x, y = self.rect.center
        dx, dy = self.speed
        screen_width = self.logic.app.screen.get_width()
        screen_height = self.logic.app.screen.get_height()
        print(self.rect, self.speed, end=' -> ')

        self.rect.center = (x + dx, y + dy)
        left, top = self.rect.topleft
        right, bottom = self.rect.bottomright

        if (right > screen_width and self.speed[0] > 0) or (left < 0 and self.speed[0] < 0):
            print('horizontal bound hit')
            # invert horizontal speed
            new_speed = (self.speed[0] * -1, self.speed[1])
            self.speed = new_speed
            self.color_id = (self.color_id + 1) % 4
        if (bottom > screen_height and self.speed[1] > 0) or (top < 0 and self.speed[1] < 0):
            # invert vertical speed
            new_speed = (self.speed[0], self.speed[1] * -1)
            print(f'vertical bound hit, {new_speed = }')
            self.speed = new_speed
            self.color_id = (self.color_id + 1) % 4

        self.rect.update(self)
        print(self.rect, self.speed)

    def draw(self):
        pg.draw.rect(self.logic.app.screen, self.colors[self.color_id], self.rect)
        # self.logic.app.screen.blit(self.sprite, self.rect)

class MenuScene:
    def __init__(self, app):
        self.app = app

        self.play_button = Button(self.app.screen, self.app.screen.get_width() // 2, self.app.screen.get_height() // 3,
                                  'Play', self.app.font, on_press=self.play)
        self.records_button = Button(self.app.screen, self.app.screen.get_width() // 2,
                                     self.app.screen.get_height() // 3 + 50,
                                     'Records', self.app.font, on_press=None)
        self.exit_button = Button(self.app.screen, self.app.screen.get_width() // 2,
                                  self.app.screen.get_height() // 3 + 100,
                                  'Exit', self.app.font, on_press=exit_application)
        self.buttons = [self.play_button, self.records_button, self.exit_button]

    def play(self):
        self.app.scene = self.app.scenes[0]

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

        self.player = Player(self, self.app.screen.get_width() // 40, self.app.screen.get_height() // 40)
        self.stone = Asteroid(self, (500, 500))
        self.bullets = []

        self.button = Button(self.app.screen, self.field_width * 10, self.field_height * 10,
                             'Restart', self.app.font, on_press=self.restart)

        self.game_over = False
        self.timer = 0

    def restart(self):
        self.player = Player(self, self.app.screen.get_width() // 40, self.app.screen.get_height() // 40)
        self.game_over = False
        self.timer = 0

    def update(self):
        if self.game_over:
            return
        # self.timer += self.app.dt
        self.stone.update()
        self.player.update()
        for x in self.bullets:
            x.update()

    def draw(self):
        self.app.screen.fill((100, 100, 100))
        # draw other game objects
        if self.game_over:
            self.player.draw()
            self.stone.draw()
            self.button.draw()
        else:
            self.player.draw()
            self.stone.draw()
            for x in self.bullets:
                x.draw()

    def check_event(self, event):
        if self.game_over:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.button.press(event)
        else:
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
