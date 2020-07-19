import time

import pygame as pg
from pygame.locals import *
from modes import Synth, open_stream
from input import Keyboard
import sys


# Main class for the interface
class Interface(object):
    def __init__(self):
        # Initialize pygame
        pg.init()

        # Display settings
        pg.display.set_caption('OP1 interface test')
        # self.screen = pg.display.set_mode((480, 320), FULLSCREEN | DOUBLEBUF, 32)
        self.screen = pg.display.set_mode((480, 320), 32)

        # Fonts
        self.font = pg.font.SysFont(None, 20)

        # Clock
        self.mainClock = pg.time.Clock()

        # Fluid synth connection
        self.port = open_stream()
        print('establisted fluid synth connection')
        self.stream = Synth(channel=0, port=self.port)

        self.keyboard = Keyboard(self.stream)
        self.key_set = self.make_key_mapping()
        self.on_notes = []

        self.loop()

    def draw_interface(self):
        self.screen.fill((0, 0, 255))
        self.draw_text('main menu', self.font, (255, 255, 255), self.screen, 20, 20)

        mx, my = pg.mouse.get_pos()

        button_1 = pg.Rect(50, 100, 200, 50)
        pg.draw.rect(self.screen, (255, 0, 0), button_1)

    def get_events(self):
        events = pg.event.get()
        for e in events:
            if e.type == pg.KEYDOWN:
                try:
                    note = self.key_set[e.key]
                except KeyError:
                    pass
                else:
                    if note not in self.on_notes:
                        self.keyboard.key_down(note)
                        self.on_notes.append(note)
            elif e.type == pg.KEYUP:
                try:
                    note = self.key_set[e.key]
                except KeyError:
                    pass
                else:
                    if note in self.on_notes:
                        self.keyboard.key_up(note)
                        self.on_notes.remove(note)

        knobs = self.keyboard.get_knobs()
        if knobs[0]:
            self.keyboard.use_knob(0)

    def make_key_mapping(self):
        key_list = [
            pg.K_z,
            pg.K_s,
            pg.K_x,
            pg.K_d,
            pg.K_c,
            pg.K_v,
            pg.K_g,
            pg.K_b,
            pg.K_h,
            pg.K_n,
            pg.K_j,
            pg.K_m,
            pg.K_COMMA,
        ]
        mapping = {}
        for i in range(len(key_list)):
            mapping[key_list[i]] = (i)
        return mapping

    def loop(self):
        while True:
            self.draw_interface()
            self.get_events()
            pg.display.update()
            self.mainClock.tick(120)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
