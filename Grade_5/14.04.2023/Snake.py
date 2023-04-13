import pygame as pg
import pygame.freetype as ft
import sys
from random import randint


# https://pygame.readthedocs.io/en/latest/


class Snake:
    def __init__(self, logic, x, y, start_length=5):
        self.logic = logic
        self.blocks = []
        for _ in range(start_length):
            self.blocks.append((x, y))
        self.direction = (1, 0)
        self.last_direction = self.direction
        self.colors = None
        self.make_colors()

    def update(self):
        self.last_direction = self.direction
        new_head = (
            (self.blocks[-1][0] + self.direction[0]) % self.logic.field_width,
            (self.blocks[-1][1] + self.direction[1]) % self.logic.field_height,
        )

        if new_head in self.blocks:
            self.logic.game_over = True
            if self.logic.score > self.logic.max_score:
                self.logic.max_score = self.logic.score
            return

        self.blocks.append(new_head)
        if new_head == self.logic.food.coords:
            self.logic.food.spawn()
            self.logic.score += 1
            self.make_colors()
        else:
            self.blocks.pop(0)

    def draw(self):
        for index, square in enumerate(self.blocks):
            pg.draw.rect(self.logic.app.screen, self.colors[index], [square[0] * 20, square[1] * 20, 20, 20])

    def make_colors(self):
        color1 = (26, 95, 122)
        color2 = (0, 43, 91)
        n = len(self.blocks)
        self.colors = []
        for i in range(n):
            # some gradient magic
            self.colors.append(tuple(map(lambda x: x[0] * i / n + x[1] * (n - i) / n, zip(color1, color2))))
        print(self.colors)

    def move_up(self):
        if self.last_direction != (0, 1):
            self.direction = (0, -1)

    def move_left(self):
        if self.last_direction != (1, 0):
            self.direction = (-1, 0)

    def move_down(self):
        if self.last_direction != (0, -1):
            self.direction = (0, 1)

    def move_right(self):
        if self.last_direction != (-1, 0):
            self.direction = (1, 0)


class Food:
    def __init__(self, logic, width_range, height_range):
        self.logic = logic
        self.width_range = width_range
        self.height_range = height_range
        self.coords = None
        self.spawn()
        self.sprite = pg.image.load('cherry.png')
        self.rect = self.sprite.get_rect()

    def spawn(self):
        self.coords = (randint(0, self.width_range - 1), randint(0, self.height_range - 1))
        if self.coords in self.logic.snake.blocks:
            self.spawn()

    def draw(self):
        self.logic.app.screen.blit(self.sprite, [self.coords[0] * 20, self.coords[1] * 20, 20, 20])
        # pg.draw.rect(self.logic.app.screen, (21, 152, 149), [self.coords[0] * 20, self.coords[1] * 20, 20, 20])


class GameLogic:
    def __init__(self, app, max_score=0):
        self.app = app

        self.field_width = self.app.screen.get_width() // 20
        self.field_height = self.app.screen.get_height() // 20

        self.snake = Snake(self, self.app.screen.get_width() // 40, self.app.screen.get_height() // 40)
        self.food = Food(self, self.field_width, self.field_height)

        self.game_over = False
        self.timer = 0
        self.score = 0
        self.max_score = max_score

    def restart(self):
        self.snake = Snake(self, self.app.screen.get_width() // 40, self.app.screen.get_height() // 40)
        self.game_over = False
        self.timer = 0
        self.score = 0
        print(f'Max score is {self.max_score}!')

    def update(self):
        if self.game_over:
            return

        self.timer += self.app.dt

        delay = 0.1
        if self.timer < delay:
            return
        self.timer -= delay

        self.snake.update()

    def draw(self):
        if self.game_over:
            self.snake.draw()
            self.food.draw()
            self.draw_score()
            self.draw_game_over()
        else:
            self.snake.draw()
            self.food.draw()
            self.draw_score()

    def draw_game_over(self):
        img = self.app.score_font.render(f'You lose scoring {self.score}. Max record is {self.max_score}', True,
                                         (0, 43, 91))
        self.app.screen.blit(img, (200, 200))

    def draw_score(self):
        img = self.app.score_font.render(f'Score: {self.score}', True, (0, 43, 91))
        self.app.screen.blit(img, (20, 20))

class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        pg.display.set_caption('Snake')
        print(type(self.screen))
        self.clock = pg.time.Clock()
        self.score_font = pg.font.SysFont("exo2extrabold", 24)
        self.dt = 0.0
        self.logic = GameLogic(self)
        pg.ListBox

    def update(self):
        self.logic.update()
        pg.display.flip()
        self.dt = self.clock.tick() * 0.001

    def draw(self):
        self.screen.fill((87, 197, 182))
        self.logic.draw()

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if self.logic.game_over:
                if e.type == pg.KEYDOWN:
                    # TODO: save records to file
                    self.logic.restart()
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_UP or e.key == ord('w'):
                    self.logic.snake.move_up()
                if e.key == pg.K_DOWN or e.key == ord('s'):
                    self.logic.snake.move_down()
                if e.key == pg.K_LEFT or e.key == ord('a'):
                    self.logic.snake.move_left()
                if e.key == pg.K_RIGHT or e.key == ord('d'):
                    self.logic.snake.move_right()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    snake = App()
    snake.run()
