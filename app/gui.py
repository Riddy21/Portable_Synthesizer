import pygame as pg
from pygame.locals import *
import platform


# Draws the text on the screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class GUI(object):
    def __init__(self, playback_handler):
        # Setup display
        if platform.system() == 'Darwin' or platform.system() == 'Windows':
            self.screen = pg.display.set_mode((480, 320), 32)
        else:
            self.screen = pg.display.set_mode((480, 320), FULLSCREEN | DOUBLEBUF, 32)

        # Fonts
        self.font = pg.font.SysFont('Helvetica', 20)

        # Get the playback handler to get all the events
        self.events = playback_handler

        self.interface = StartupInt(self.events, self)

    # sets the interface of the OP1 and passes in the pointer to the player
    def set_interface(self, mode):
        if mode == 'freeplay':
            self.interface = FreeplayInt(self.events, self)
        elif mode == 'test':
            self.interface = TestInt(self.events, self)

    # Draws whatever interface is currently on and updates
    def draw_interface(self):
        # switch interfaces if the interface changed
        if self.events.current_mode.name != self.interface.name:
            self.set_interface(self.events.current_mode.name)

        # draw the interface and update
        self.interface.draw_interface()
        pg.display.update()

    # Updates on certain element of the screen
    def update(self, func):
        pg.display.update(func)

# -----------------------------
# Interface Modes
# -----------------------------

class FreeplayInt(object):
    def __init__(self, events, gui):
        self.name = 'freeplay'
        self.events = events
        self.gui = gui

    # draws the interface on the screen
    def draw_interface(self):
        self.gui.screen.fill((0, 0, 255))
        draw_text(self.name, self.gui.font, (255, 255, 255), self.gui.screen, 20, 20)

class TestInt(object):
    def __init__(self, events, gui):
        self.name = 'test'
        self.events = events
        self.gui = gui

    # draws the interface on the screen
    def draw_interface(self):
        self.gui.screen.fill((0, 0, 255))
        draw_text(self.name, self.gui.font, (255, 255, 255), self.gui.screen, 20, 20)
        if self.events.player.recording:
            draw_text('recording', self.gui.font, (255, 255, 255), self.gui.screen, 20, 40)
        if self.events.player.playing:
            draw_text('playing', self.gui.font, (255, 255, 255), self.gui.screen, 20, 60)

class StartupInt(object):
    def __init__(self, events, gui):
        self.name = 'startup'
        self.events = events
        self.gui = gui

    # draws the interface on the screen
    def draw_interface(self):
        self.gui.screen.fill((0, 0, 255))
        draw_text(self.name, self.gui.font, (255, 255, 255), self.gui.screen, 20, 20)

        test_button = pg.Rect(50, 100, 200, 50)
        pg.draw.rect(self.gui.screen, (255, 0, 0), test_button)