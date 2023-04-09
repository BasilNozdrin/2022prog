import pygame as pg
import pygame.freetype as ft
import sys
from enum import IntEnum


class Control:
    def __init__(self, app):
        self.app = app
        self.width, self.height = app.screen.get_width(), app.screen.get_height()
        self.x, self.y = 100, 100
        self.x_velocity, self.y_velocity = 0, 0
        self.max_speed = 600
        self.moving = {'up': False, 'left': False, 'down': False, 'right': False}

    def update(self):
        acceleration = 400
        if self.moving['up'] and abs(self.y_velocity) < self.max_speed:
            self.y_velocity -= acceleration * self.app.dt
        if self.moving['left'] and abs(self.x_velocity) < self.max_speed:
            self.x_velocity -= acceleration * self.app.dt
        if self.moving['down'] and abs(self.y_velocity) < self.max_speed:
            self.y_velocity += acceleration * self.app.dt
        if self.moving['right'] and abs(self.x_velocity) < self.max_speed:
            self.x_velocity += acceleration * self.app.dt

        self.x += self.x_velocity * self.app.dt
        self.y += self.y_velocity * self.app.dt

        # bounce from screen edges
        if self.x < 0 or self.x > 1600:
            self.x_velocity *= -1
        if self.y < 0 or self.y > 900:
            self.y_velocity *= -1

    def draw(self):
        pg.draw.circle(self.app.screen, (87, 197, 182), (self.x, self.y), 30)

    def move_up(self):
        if self.y_velocity > 0:
            self.stop_move_down()
        else:
            self.moving['up'] = True

    def move_down(self):
        if self.y_velocity < 0:
            self.stop_move_up()
        else:
            self.moving['down'] = True

    def move_left(self):
        if self.x_velocity < 0:
            self.stop_move_right()
        else:
            self.moving['left'] = True

    def move_right(self):
        if self.x_velocity < 0:
            self.stop_move_left()
        else:
            self.moving['right'] = True

    def stop_move_up(self):
        self.moving['up'] = False
        self.y_velocity = 0

    def stop_move_down(self):
        self.moving['down'] = False
        self.y_velocity = 0

    def stop_move_left(self):
        self.moving['left'] = False
        self.x_velocity = 0

    def stop_move_right(self):
        self.moving['right'] = False
        self.x_velocity = 0


class App:
    def __init__(self):
        pg.init()
        self.width, self.height = 1600, 900
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption('Game title should be here!')
        self.clock = pg.time.Clock()
        self.font = ft.SysFont('exo2extrabold', 30)
        self.dt = 0.0
        self.control = Control(self)

    def update(self):
        self.control.update()
        pg.display.flip()
        self.dt = self.clock.tick() * 0.001

    def draw_fps(self):
        fps = f'{self.clock.get_fps() :.0f} FPS | {round(self.control.x_velocity, 2)}; {round(self.control.y_velocity, 2)}'
        self.font.render_to(self.screen, (0, 0), text=fps)

    def draw(self):
        self.screen.fill((26, 95, 122))
        self.control.draw()
        self.draw_fps()

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_UP or e.key == ord('w'):
                    self.control.move_up()
                if e.key == pg.K_DOWN or e.key == ord('s'):
                    self.control.move_down()
                if e.key == pg.K_LEFT or e.key == ord('a'):
                    self.control.move_left()
                if e.key == pg.K_RIGHT or e.key == ord('d'):
                    self.control.move_right()
            elif e.type == pg.KEYUP:
                if e.key == pg.K_UP or e.key == ord('w'):
                    self.control.stop_move_up()
                if e.key == pg.K_DOWN or e.key == ord('s'):
                    self.control.stop_move_down()
                if e.key == pg.K_LEFT or e.key == ord('a'):
                    self.control.stop_move_left()
                if e.key == pg.K_RIGHT or e.key == ord('d'):
                    self.control.stop_move_right()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    App().run()
