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
        self.keyboard = Keyboard(self.stream)
        self.instrum_index = 0
        self.key_set = self.make_key_mapping()
        self.on_notes = set()

        self.loop()

    def draw_interface(self):
        self.screen.fill((0, 0, 255))
        self.draw_text('main menu', self.font, (255, 255, 255), self.screen, 20, 20)

        mx, my = pg.mouse.get_pos()

        button_1 = pg.Rect(50, 100, 200, 50)
        pg.draw.rect(self.screen, (255, 0, 0), button_1)

    def get_events(self):
        e = pg.event.wait()
        if e.type == pg.QUIT:
            sys.exit()
        elif e.type == pg.KEYDOWN:
            try:
                note = self.key_set[e.key]
            except KeyError:
                pass
            else:
                if note not in self.on_notes:
                    self.keyboard.key_down(note)
                    self.on_notes.add(note)
        elif e.type == pg.KEYUP:
            try:
                note = self.key_set[e.key]
            except KeyError:
                pass
            else:
                if note in self.on_notes:
                    self.keyboard.key_up(note)
                    self.on_notes.remove(note)


        # if keys[pg.K_UP]:
        #     self.keyboard.next_prog(0,pressed=True)
        # elif not keys[pg.K_UP]:
        #     self.keyboard.next_prog(0,pressed=False)
        # if keys[pg.K_DOWN]:
        #     self.keyboard.prev_prog(1, pressed=True)
        # elif not keys[pg.K_DOWN]:
        #     self.keyboard.prev_prog(1, pressed=False)

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