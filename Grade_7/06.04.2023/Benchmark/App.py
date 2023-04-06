from Settings import *
import pygame as pg
import pygame.freetype as ft
import sys

from SpriteHandler import SpriteHandler


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN_SIZE)
        print(type(self.screen))
        self.clock = pg.time.Clock()
        self.font = ft.SysFont('Verdana', FONT_SIZE)
        self.sprite_handler = SpriteHandler(self)
        self.dt = 0.0

    def update(self):
        self.sprite_handler.update()
        pg.display.flip()
        self.dt = self.clock.tick() * 0.001

    def draw_fps(self):
        fps = f'{self.clock.get_fps() :.0f} FPS | {len(self.sprite_handler.sprites)} SPRITES'
        self.font.render_to(self.screen, (0, 0), text=fps, fgcolor='green', bgcolor='black')

    def draw(self):
        self.screen.fill('black')
        self.sprite_handler.draw()
        self.draw_fps()

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif e.type == pg.MOUSEBUTTONDOWN:
                self.sprite_handler.on_mouse_press()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
