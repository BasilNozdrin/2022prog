import pygame as pg
import sys
from random import randint
import json
import math

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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


class MenuScene:
    def __init__(self, app):
        self.app = app

        self.play_button = Button(self.app.screen, self.app.screen.get_width() // 2, self.app.screen.get_height() // 3,
                                  'Play', self.app.font, on_press=self.play)
        self.exit_button = Button(self.app.screen, self.app.screen.get_width() // 2,
                                  self.app.screen.get_height() // 3 + 100,
                                  'Exit', self.app.font, on_press=exit_application)
        self.buttons = [self.play_button, self.exit_button]

    def play(self):
        self.app.scene = self.app.scenes['game']

    def update(self):
        if self.app.scenes['game'].game_over:
            self.app.scenes['game'].restart()

    def draw(self):
        # self.app.screen.blit(self.bg, (0, 0))

        for b in self.buttons:
            b.draw()

    def check_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.play()
        if event.type == pg.MOUSEBUTTONDOWN:
            for b in self.buttons:
                b.press(event)



class GameScene:
    def __init__(self, app):
        self.app = app

        self.images = []
        self.game_over = False
        self.x_turn = True
        self.o_turn = False

        self.timer = 0

        self.game_array = [[None, None, None], [None, None, None], [None, None, None]]
        self.initialize_grid()

        self.X_IMAGE = pg.transform.scale(pg.image.load("x.png"), (80, 80))
        self.O_IMAGE = pg.transform.scale(pg.image.load("o.png"), (80, 80))

    def restart(self):
        # del self.images
        self.images = []
        self.game_over = False
        self.x_turn = True
        self.o_turn = False
        self.timer = 0
        # del self.game_array
        self.game_array = [[None, None, None], [None, None, None], [None, None, None]]
        self.initialize_grid()

    def update(self):
        if self.has_won():
            self.game_over = True
        elif self.has_drawn():
            self.game_over = True

        if self.game_over:
            self.app.scene = self.app.scenes['menu']
            self.restart()

        # self.timer += self.app.dt
        # delay = 0.1
        # if self.timer < delay:
        #     return
        # self.timer -= delay

    def draw(self):
        self.app.screen.fill(WHITE)
        gap = self.app.screen.get_width() // 3
        # Starting points
        x, y = 0, 0
        for i in range(3):
            x = i * gap
            pg.draw.line(self.app.screen, GRAY, (x, 0), (x, self.app.screen.get_width()), 3)
            pg.draw.line(self.app.screen, GRAY, (0, x), (self.app.screen.get_width(), x), 3)
        for image in self.images:
            x, y, img = image
            self.app.screen.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))
        pg.display.update()

    def check_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.click()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.scene = self.app.scenes['menu']

    def click(self):
        # Mouse position
        m_x, m_y = pg.mouse.get_pos()

        for (row_id, row) in enumerate(self.game_array):
            for (cell_id, cell) in enumerate(row):
                x, y, char, can_play = cell
                # Distance between mouse and the centre of the square
                dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                # If it's inside the square
                if dis < self.app.screen.get_width() // 3 // 2 and can_play:
                    if self.x_turn:  # If it's X's turn
                        self.images.append((x, y, self.X_IMAGE))
                        self.x_turn = False
                        self.o_turn = True
                        self.game_array[row_id][cell_id] = (x, y, 'x', False)
                    elif self.o_turn:  # If it's O's turn
                        self.images.append((x, y, self.O_IMAGE))
                        self.x_turn = True
                        self.o_turn = False
                        self.game_array[row_id][cell_id] = (x, y, 'o', False)

    def has_won(self):
        # Checking rows
        for row in range(len(self.game_array)):
            if (self.game_array[row][0][2] == self.game_array[row][1][2] == self.game_array[row][2][2]) and self.game_array[row][0][
                2] != "":
                self.display_message(self.game_array[row][0][2].upper() + " has won!")
                return True

        # Checking columns
        for col in range(len(self.game_array)):
            if (self.game_array[0][col][2] == self.game_array[1][col][2] == self.game_array[2][col][2])\
                    and self.game_array[0][col][2] != "":
                self.display_message(self.game_array[0][col][2].upper() + " has won!")
                return True

        # Checking main diagonal
        if (self.game_array[0][0][2] == self.game_array[1][1][2] == self.game_array[2][2][2]) and self.game_array[0][0][2] != "":
            self.display_message(self.game_array[0][0][2].upper() + " has won!")
            return True

        # Checking reverse diagonal
        if (self.game_array[0][2][2] == self.game_array[1][1][2] == self.game_array[2][0][2]) and self.game_array[0][2][2] != "":
            self.display_message(self.game_array[0][2][2].upper() + " has won!")
            return True

        return False

    def has_drawn(self):
        for a in self.game_array:
            for b in a:
                if b[2] == "":
                    return False
        self.display_message("It's a draw!")

        return True

    def display_message(self, content):
        pg.time.delay(500)
        self.app.screen.fill(WHITE)
        end_text = self.app.font.render(content, 1, BLACK)
        self.app.screen.blit(end_text, (
            (self.app.screen.get_width() - end_text.get_width()) // 2,
            (self.app.screen.get_width() - end_text.get_height()) // 2))
        pg.display.update()
        pg.time.delay(3000)

    def initialize_grid(self):
        dis_to_cen = self.app.screen.get_width() // 3 // 2

        # Initializing the array
        for i in range(len(self.game_array)):
            for j in range(len(self.game_array[i])):
                x = dis_to_cen * (2 * j + 1)
                y = dis_to_cen * (2 * i + 1)

                # Adding centre coordinates
                self.game_array[i][j] = (x, y, "", True)


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((300, 300))
        pg.display.set_caption('TicTacToe')
        self.clock = pg.time.Clock()
        self.END_FONT = pg.font.SysFont('arial', 40)
        self.font = pg.font.SysFont("exo2extrabold", 40)
        self.dt = 0.0

        self.scenes = {
            'menu': MenuScene(self),
            'game': GameScene(self),
        }
        self.scenes[0] = self.scenes['menu']
        self.scenes[1] = self.scenes['game']

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
            if e.type == pg.QUIT:
                pg.quit()

            self.scene.check_event(e)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    App().run()
