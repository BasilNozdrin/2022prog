import pygame as pg
import pygame.freetype as ft
import sys
from enum import IntEnum

class State(IntEnum):
    IDLE = 0
    MOVING_UPWARD = 1
    MOVING_LEFTWARD = 2
    MOVING_DOWNWARD = 3
    MOVING_RIGHTWARD = 4
    MOVING_UPLEFT = 5
    MOVING_UPRIGHT = 6
    MOVING_DOWNRIGHT = 7
    MOVING_DOWNLEFT = 8

class Control:
    def __init__(self, app):
        self.app = app
        self.x, self.y = 100, 100
        self.x_velocity, self.y_velocity = 0, 0
        self.state = State.IDLE

    def update(self):
        acceleration = 60
        if self.state == State.MOVING_UPWARD or self.state == State.MOVING_UPLEFT or self.state == State.MOVING_UPRIGHT:
            self.y_velocity -= acceleration * self.app.dt
        if self.state == State.MOVING_LEFTWARD or self.state == State.MOVING_UPLEFT or self.state == State.MOVING_DOWNLEFT:
            self.x_velocity -= acceleration * self.app.dt
        if self.state == State.MOVING_DOWNWARD:
            self.y_velocity += acceleration * self.app.dt
        if self.state == State.MOVING_RIGHTWARD:
            self.x_velocity += acceleration * self.app.dt
        if self.state == State.IDLE:
            self.x_velocity *= 0.8
            self.y_velocity *= 0.8

        self.x += self.x_velocity * self.app.dt
        self.y += self.y_velocity * self.app.dt
        if self.x < 0 or self.x > 1600:
            self.x_velocity *= -1
        if self.y < 0 or self.y > 900:
            self.y_velocity *= -1

    def draw(self):
        pg.draw.circle(self.app.screen, (87, 197, 182), (self.x, self.y), 30)

    def move_up(self):
        if self.state == State.MOVING_LEFTWARD:
            self.state == State.MOVING_UPLEFT
        elif self.state == State.MOVING_RIGHTWARD:
            self.state == State.MOVING_UPRIGHT
        else:
            self.state = State.MOVING_UPWARD

    def move_down(self):
        self.state = State.MOVING_DOWNWARD

    def move_left(self):
        self.state = State.MOVING_LEFTWARD

    def move_right(self):
        self.state = State.MOVING_RIGHTWARD

    def idle(self):
        self.state = State.IDLE


class App:
    def __init__(self):
        pg.init()
        self.width, self.height = 1600, 900
        self.screen = pg.display.set_mode((self.width, self.height))
        print(type(self.screen))
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
                self.control.idle()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
