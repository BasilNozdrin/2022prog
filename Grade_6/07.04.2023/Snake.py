import pygame as pg
import pygame.freetype as ft
import sys
from random import randint

# https://pygame.readthedocs.io/en/latest/


class GameLogic:
    def __init__(self, app, max_score=0):
        self.app = app
        self.field_width = self.app.screen.get_width() // 20
        self.field_height = self.app.screen.get_height() // 20
        self.snake = [[self.app.screen.get_width() // 40, self.app.screen.get_height() // 40]]
        self.colors = []
        self.make_colors()
        self.snake_direction = (1, 0)
        self.last_direction = (1, 0)
        self.food = None
        self.spawn_food()
        self.game_over = False
        self.timer = 0
        self.score = 0
        self.max_score = max_score

    def make_colors(self):
        color1 = (26, 95, 122)
        color2 = (0, 43, 91)
        n = len(self.snake)
        self.colors = []
        for i in range(n):
            # some gradient magic
            self.colors.append(tuple(map(lambda x: x[0] * i / n + x[1] * (n - i) / n, zip(color1, color2))))

    def spawn_food(self):
        self.food = [randint(0, self.field_width-1), randint(0, self.field_height-1)]
        if self.food in self.snake:
            self.food = None

    def restart(self):
        self.snake = [[self.app.screen.get_width() // 40, self.app.screen.get_height() // 40]]
        self.snake_direction = (1, 0)
        self.last_direction = (1, 0)
        self.game_over = False
        self.timer = 0
        self.score = 0
        self.food = None
        while self.food is None:
            self.spawn_food()
        print(f'Max score is {self.max_score}!')

    def update(self):
        if self.game_over:
            return

        self.timer += self.app.dt

        while self.food is None:
            self.spawn_food()

        delay = 0.1
        if self.timer < delay:
            return
        self.timer -= delay

        self.last_direction = self.snake_direction

        new_head = [
            (self.snake[-1][0] + self.snake_direction[0]) % self.field_width,
            (self.snake[-1][1] + self.snake_direction[1]) % self.field_height,
        ]

        if new_head in self.snake:
            self.game_over = True
            if self.score > self.max_score:
                self.max_score = self.score
            return

        self.snake.append(new_head)
        if new_head == self.food:
            self.spawn_food()
            self.score += 1
            self.make_colors()
        else:
            self.snake.pop(0)

    def draw(self):
        if self.game_over:
            self.draw_snake()
            self.draw_food()
            self.draw_score()
            self.draw_game_over()
        else:
            self.draw_snake()
            self.draw_food()
            self.draw_score()

    def draw_game_over(self):
        img = self.app.score_font.render(f'You lose scoring {self.score}. Max record is {self.max_score}', True, (0, 43, 91))
        self.app.screen.blit(img, (200, 200))

    def draw_score(self):
        img = self.app.score_font.render(f'Score: {self.score}', True, (0, 43, 91))
        self.app.screen.blit(img, (20, 20))

    def draw_food(self):
        if self.food:
            pg.draw.rect(self.app.screen, (21, 152, 149), [self.food[0]*20, self.food[1]*20, 20, 20])

    def draw_snake(self):
        for index, square in enumerate(self.snake):
            pg.draw.rect(self.app.screen, self.colors[index], [square[0]*20, square[1]*20, 20, 20])

    def move_up(self):
        if self.last_direction != (0, 1):
            self.snake_direction = (0, -1)

    def move_left(self):
        if self.last_direction != (1, 0):
            self.snake_direction = (-1, 0)

    def move_down(self):
        if self.last_direction != (0, -1):
            self.snake_direction = (0, 1)

    def move_right(self):
        if self.last_direction != (-1, 0):
            self.snake_direction = (1, 0)


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1600, 900))
        pg.display.set_caption('Snake')
        print(type(self.screen))
        self.clock = pg.time.Clock()
        self.score_font = pg.font.SysFont("exo2extrabold", 24)
        self.dt = 0.0
        self.logic = GameLogic(self)

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
                    # TODO: save records
                    self.logic.restart()
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_UP or e.key == ord('w'):
                    self.logic.move_up()
                if e.key == pg.K_DOWN or e.key == ord('s'):
                    self.logic.move_down()
                if e.key == pg.K_LEFT or e.key == ord('a'):
                    self.logic.move_left()
                if e.key == pg.K_RIGHT or e.key == ord('d'):
                    self.logic.move_right()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    snake = App()
    snake.run()
