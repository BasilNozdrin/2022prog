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
            if self.logic.score > self.logic.records['username']:
                self.logic.records['username'] = self.logic.score
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
            self.colors.append(tuple(map(lambda x: x[0] * i / n + x[1] * (1 - i / n), zip(color1, color2))))

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
        self.sprite = pg.image.load('cherry.png')
        self.rect = self.sprite.get_rect()

        self.spawn()

    def spawn(self):
        self.coords = (randint(0, self.width_range - 1), randint(0, self.height_range - 1))
        self.rect.left = self.coords[0] * 20
        self.rect.top = self.coords[1] * 20

        if self.coords in self.logic.snake.blocks:
            self.spawn()

    def draw(self):
        self.logic.app.screen.blit(self.sprite, self.rect)
        # self.logic.app.screen.blit(self.sprite, [self.coords[0] * 20, self.coords[1] * 20, 20, 20])
        # pg.draw.rect(self.logic.app.screen, (21, 152, 149), [self.coords[0] * 20, self.coords[1] * 20, 20, 20])


class MenuScene:
    def __init__(self, app):
        self.app = app

        self.bg = pg.image.load('background.png')
        self.bg = pg.transform.smoothscale(self.bg, self.app.screen.get_size())

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
        # self.app.screen.blit(self.bg, (0, 0))

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

        self.bg = pg.image.load('background.png')
        self.bg = pg.transform.smoothscale(self.bg, self.app.screen.get_size())

        self.field_width = self.app.screen.get_width() // 20
        self.field_height = self.app.screen.get_height() // 20

        self.snake = Snake(self, self.app.screen.get_width() // 40, self.app.screen.get_height() // 40)
        self.food = Food(self, self.field_width, self.field_height)

        self.button = Button(self.app.screen, self.field_width * 10, self.field_height * 10,
                             'Restart', self.app.font, on_press=self.restart)

        self.game_over = False
        self.timer = 0
        self.score = 0
        try:
            with open('save.json') as file:
                self.records = json.load(file)
        except FileNotFoundError:
            self.records = {'username': 0}

    def restart(self):
        self.records['username'] = self.score
        self.save_records()
        self.snake = Snake(self, self.app.screen.get_width() // 40, self.app.screen.get_height() // 40)
        self.game_over = False
        self.timer = 0
        self.score = 0

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
        # draw background
        self.app.screen.blit(self.bg, (0, 0))

        # draw other game objects
        if self.game_over:
            self.snake.draw()
            self.food.draw()
            self.draw_score()
            self.draw_game_over()
            self.button.draw()
        else:
            self.snake.draw()
            self.food.draw()
            self.draw_score()

    def check_event(self, event):
        if self.game_over:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.button.press(event)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.scene = self.app.scenes[1]
            if event.key == pg.K_UP or event.key == ord('w'):
                self.snake.move_up()
            if event.key == pg.K_DOWN or event.key == ord('s'):
                self.snake.move_down()
            if event.key == pg.K_LEFT or event.key == ord('a'):
                self.snake.move_left()
            if event.key == pg.K_RIGHT or event.key == ord('d'):
                self.snake.move_right()

    def save_records(self):
        with open('save.json', 'w') as file:
            json.dump(self.records, file)

    def draw_game_over(self):
        img = self.app.font.render(f'You lose scoring {self.score}. Max record is {max(self.records.values())}',
                                   True, (0, 43, 91))
        self.app.screen.blit(img, (self.field_width * 8, self.field_height * 7))

    def draw_score(self):
        img = self.app.font.render(f'Score: {self.score}', True, (0, 43, 91))
        self.app.screen.blit(img, (20, 20))


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
        self.dt = self.clock.tick() * 0.001

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
