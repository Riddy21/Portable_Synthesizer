import pygame as pg
from pygame.locals import *
from sonic_pi_api import SynthStream
from keyboard import Keyboard
import sys

class Main_Menu(object):
    def __init__(self):
        pg.init()
        pg.display.set_caption('OP1 interface test')
        self.screen = pg.display.set_mode((500, 500), 32)
        self.font = pg.font.SysFont(None, 20)
        self.mainClock = pg.time.Clock()
        self.stream = SynthStream(stream_num=0)
        self.stream.open_stream()
        self.keyboard = Keyboard(self.stream)

        self.loop()

    def draw_interface(self):
        self.screen.fill((0, 0, 255))
        self.draw_text('main menu', self.font, (255, 255, 255), self.screen, 20, 20)

        mx, my = pg.mouse.get_pos()

        button_1 = pg.Rect(50, 100, 200, 50)
        pg.draw.rect(self.screen, (255, 0, 0), button_1)

    def get_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit(0)
        keys = pg.key.get_pressed()
        if keys[pg.K_z]:
            self.keyboard.key_down(0)
        elif not keys[pg.K_z]:
            self.keyboard.key_up(0)
        if keys[pg.K_s]:
            self.keyboard.key_down(1)
        elif not keys[pg.K_s]:
            self.keyboard.key_up(1)
        if keys[pg.K_x]:
            self.keyboard.key_down(2)
        elif not keys[pg.K_x]:
            self.keyboard.key_up(2)
        if keys[pg.K_d]:
            self.keyboard.key_down(3)
        elif not keys[pg.K_d]:
            self.keyboard.key_up(3)
        if keys[pg.K_c]:
            self.keyboard.key_down(4)
        elif not keys[pg.K_c]:
            self.keyboard.key_up(4)
        if keys[pg.K_v]:
            self.keyboard.key_down(5)
        elif not keys[pg.K_v]:
            self.keyboard.key_up(5)
        if keys[pg.K_g]:
            self.keyboard.key_down(6)
        elif not keys[pg.K_g]:
            self.keyboard.key_up(6)
        if keys[pg.K_b]:
            self.keyboard.key_down(7)
        elif not keys[pg.K_b]:
            self.keyboard.key_up(7)
        if keys[pg.K_h]:
            self.keyboard.key_down(8)
        elif not keys[pg.K_h]:
            self.keyboard.key_up(8)
        if keys[pg.K_n]:
            self.keyboard.key_down(9)
        elif not keys[pg.K_n]:
            self.keyboard.key_up(9)
        if keys[pg.K_j]:
            self.keyboard.key_down(10)
        elif not keys[pg.K_j]:
            self.keyboard.key_up(10)
        if keys[pg.K_m]:
            self.keyboard.key_down(11)
        elif not keys[pg.K_m]:
            self.keyboard.key_up(11)


    def loop(self):
        while True:
            self.draw_interface()
            self.get_events()
            pg.display.update()
            self.mainClock.tick(60)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)