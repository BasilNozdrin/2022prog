import pygame as pg
import pygame.freetype as ft
import sys
from random import randint

# https://pygame.readthedocs.io/en/latest/


class GameLogic:
    def __init__(self, app):
        self.app = app
        self.field_width = self.app.screen.get_width() // 20
        self.field_height = self.app.screen.get_height() // 20
        self.snake = [[self.app.screen.get_width() // 40, self.app.screen.get_height() // 40]]
        for x in range(40):
            self.snake.append([self.snake[-1][0]+1, self.snake[-1][1]])
        self.snake_direction = (0, 0)
        self.last_direction = (0, 0)
        self.food = None
        self.spawn_food()
        self.game_over = False
        self.timer = 0
        self.score = 0
        self.score_font = pg.font.SysFont("exo2extrabold", 24)

    def spawn_food(self):
        self.food = [randint(0, self.field_width-1), randint(0, self.field_height-1)]
        if self.food in self.snake:
            self.food = None

    def update(self):
        if self.game_over:
            return
        self.timer += self.app.dt
        if self.food is None:
            self.spawn_food()
        if self.timer < 0.1:
            return
        self.timer -= 0.1
        self.last_direction = self.snake_direction
        new_head = [
            (self.snake[-1][0] + self.snake_direction[0]) % self.field_width,
            (self.snake[-1][1] + self.snake_direction[1]) % self.field_height,
        ]
        if new_head == self.food:
            self.spawn_food()
            self.score += 1
        elif new_head not in self.snake:
            self.snake.pop(0)
        else:
            self.game_over = True
        self.snake.append(new_head)

    def draw(self):
        if self.game_over:
            self.draw_snake()
            self.draw_food()
            self.draw_score()
        else:
            self.draw_snake()
            self.draw_food()
            self.draw_score()

    def draw_score(self):
        img = self.score_font.render(f'Score: {self.score}', True, (200, 0, 0))
        self.app.screen.blit(img, (20, 20))

    def draw_food(self):
        if self.food:
            pg.draw.rect(self.app.screen, (59, 161, 5), [self.food[0]*20, self.food[1]*20, 20, 20])

    def draw_snake(self):
        red = (161, 5, 5)
        yellow = (145, 161, 5)
        n = len(self.snake)
        for index, square in enumerate(self.snake):
            color = tuple(map(lambda x: x[0] * index / n + x[1] * (n - index) / n, zip(red, yellow)))
            pg.draw.rect(self.app.screen, color, [square[0]*20, square[1]*20, 20, 20])

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
        if self.last_direction != (1, 0):
            self.snake_direction = (1, 0)


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1600, 900))
        pg.display.set_caption('Snake')
        print(type(self.screen))
        self.clock = pg.time.Clock()
        self.font = ft.SysFont('Verdana', 40)
        self.dt = 0.0
        self.logic = GameLogic(self)

    def update(self):
        self.logic.update()
        pg.display.flip()
        self.dt = self.clock.tick() * 0.001

    def draw(self):
        self.screen.fill((0, 84, 31))
        self.logic.draw()

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if self.logic.game_over:
                if e.type == pg.KEYDOWN:
                    # TODO: save records
                    self.logic = GameLogic(self)
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
