import pygame as pg
from pygame.locals import *
import platform


class Gui(object):

    def __init__(self, event_handler):
        # Setup display
        if platform.system() == 'Darwin' or platform.system() == 'Windows':
            self.screen = pg.display.set_mode((480, 320), 32)
        else:
            self.screen = pg.display.set_mode((480, 320), FULLSCREEN | DOUBLEBUF, 32)

        # Fonts
        self.font = pg.font.SysFont('Helvetica', 20)

        # Get the playback handler to get all the events
        self.events = event_handler

        self.interface = StartupInt(self.events, self)

    # sets the interface of the OP1 and passes in the pointer to the player
    def set_interface(self, mode):
        if mode == 'freeplay':
            self.interface = FreeplayInt(self)
        elif mode == 'test':
            self.interface = TestInt(self)

    # Draws whatever interface is currently on and updates
    def draw_interface(self):
        # switch interfaces if the interface changed
        mode_name = self.events.get_current_mode().name
        if mode_name != self.interface.name:
            self.set_interface(mode_name)

        # draw the interface and update
        self.interface.draw_interface()
        pg.display.update()

    # Get event_handler


# -----------------------------
# Interface Modes
# -----------------------------

class GuiInterface(object):
    def __init__(self, name, gui):
        self.name = name
        self.events = gui.events
        self.gui = gui
        self.channel_index = self.events.current_channel_index

    # Draws the text on the screen
    @staticmethod
    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    # Draw interface abstract method
    def draw_interface(self):
        pass

class FreeplayInt(GuiInterface):
    def __init__(self, gui):
        super().__init__('freeplay',gui)

    # draws the interface on the screen
    def draw_interface(self):
        self.gui.screen.fill((0, 0, 255))
        self.draw_text(self.name, self.gui.font, (255, 255, 255), self.gui.screen, 20, 20)
        if self.events.player.recording:
            self.draw_text('recording', self.gui.font, (255, 255, 255), self.gui.screen, 20, 40)
        if self.events.player.playing:
            self.draw_text('playing', self.gui.font, (255, 255, 255), self.gui.screen, 20, 60)

        # TODO: Make api
        channel = self.events.get_current_channel()

        self.draw_text('channel: %s' % self.channel_index[0],
                       self.gui.font, (255, 255, 255), self.gui.screen, 20, 80)
        self.draw_text('instrument: %s' % channel.instr_list[channel.instr],
                  self.gui.font, (255, 255, 255), self.gui.screen, 20, 100)


class TestInt(GuiInterface):
    def __init__(self, gui):
        super().__init__('test', gui)

    # draws the interface on the screen
    def draw_interface(self):
        self.gui.screen.fill((0, 0, 255))
        self.draw_text(self.name, self.gui.font, (255, 255, 255), self.gui.screen, 20, 20)
        if self.events.player.recording:
            self.draw_text('recording', self.gui.font, (255, 255, 255), self.gui.screen, 20, 40)
        if self.events.player.playing:
            self.draw_text('playing', self.gui.font, (255, 255, 255), self.gui.screen, 20, 60)


class StartupInt(GuiInterface):
    def __init__(self, events, gui):
        self.name = 'startup'
        self.events = events
        self.gui = gui

    # draws the interface on the screen
    def draw_interface(self):
        self.gui.screen.fill((0, 0, 255))
        self.draw_text(self.name, self.gui.font, (255, 255, 255), self.gui.screen, 20, 20)

        test_button = pg.Rect(50, 100, 200, 50)
        pg.draw.rect(self.gui.screen, (255, 0, 0), test_button)
