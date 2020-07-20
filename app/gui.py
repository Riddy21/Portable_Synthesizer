import pygame as pg
from pygame.locals import *
import platform


class GUI(object):
    def __init__(self):
        # Setup display
        if platform.system() == 'Darwin' or platform.system() == 'Windows':
            self.screen = pg.display.set_mode((480, 320), 32)
        else:
            self.screen = pg.display.set_mode((480, 320), FULLSCREEN | DOUBLEBUF, 32)

        # Fonts
        self.font = pg.font.SysFont(None, 20)

    # Draws the text on the screen
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def draw_interface(self):
        self.update(self.screen.fill((0, 0, 255)))
        self.update(self.draw_text('Test text', self.font, (255, 255, 255), self.screen, 20, 20))

        test_button = pg.Rect(50, 100, 200, 50)
        pg.draw.rect(self.screen, (255, 0, 0), test_button)

    def update(self, func):
        pg.display.update(func)