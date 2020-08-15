import pygame as pg
from pygame.locals import *
import platform
from pygame_functions import makeSprite, showSprite, moveSprite


class Gui(object):

    def __init__(self, event_handler):
        # Setup display
        if platform.system() == 'Darwin' or platform.system() == 'Windows':
            self.screen = pg.display.set_mode((480, 320), 32)
        else:
            self.screen = pg.display.set_mode((480, 320), FULLSCREEN | DOUBLEBUF, 32)

        # Fonts
        self.font = pg.font.SysFont('robotomonolightforpowerlinettf', 15)

        # Get the playback handler to get all the events
        self.events = event_handler

        self.interface_dict = self._initialize_interfaces()

        # Make startup interface
        self.interface = self.interface_dict['freeplay']

    def _initialize_interfaces(self):
        interfaces = dict()
        interfaces['freeplay'] = FreeplayInt(self)
        interfaces['soundselect'] = SoundSelectInt(self)
        interfaces['test'] = TestInt(self)
        interfaces['recorder'] = RecorderInt(self)
        return interfaces

    # sets the interface of the OP1 and passes in the pointer to the player
    def set_interface(self, mode):
        self.interface = self.interface_dict[mode]

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

class RecorderInt(GuiInterface):
    def __init__(self, gui):
        self.casset = makeSprite('Assets/Sprites/Recording_Background_Sprite.png', 5).images
        self.casset_count = 0
        super().__init__('recorder', gui)

    def draw_interface(self):
        self.gui.screen.fill((0, 0, 0))
        self.gui.screen.blit(self.casset[int(self.casset_count)], (0,0))
        self.casset_count = (self.casset_count - 0.1) % 5

class SoundSelectInt(GuiInterface):
    def __init__(self, gui):
        self.casset = makeSprite('Assets/Sprites/Recording_Background_Sprite.png', 5).images
        self.casset_count = 0
        super().__init__('soundselect', gui)

    # draws the interface on the screen
    def draw_interface(self):
        self.gui.screen.fill((0, 0, 0))

        self.draw_text(self.name, self.gui.font, (255, 255, 255), self.gui.screen, 20, 20)
        if self.events.player.recording:
            self.draw_text('recording', self.gui.font, (255, 255, 255), self.gui.screen, 20, 40)
        if self.events.player.playing:
            self.draw_text('playing', self.gui.font, (255, 255, 255), self.gui.screen, 20, 60)

        # TODO: Make api
        channel = self.events.get_current_channel()

        self.draw_text('channel: %s' % self.channel_index[0],
                       self.gui.font, (255, 255, 255), self.gui.screen, 20, 80)
        self.draw_text('bank & program: %s, %s' % (channel.instr[0], channel.instr[1]),
                       self.gui.font, (255, 255, 255), self.gui.screen, 20, 100)
        self.draw_text('instrument: %s' % channel.instr_dict[channel.instr[0], channel.instr[1]],
                       self.gui.font, (255, 255, 255), self.gui.screen, 20, 120)


class FreeplayInt(GuiInterface):
    def __init__(self, gui):
        super().__init__('freeplay', gui)

    # draws the interface on the screen
    def draw_interface(self):
        self.gui.screen.fill((0, 0, 0))
        self.draw_text(self.name, self.gui.font, (255, 255, 255), self.gui.screen, 20, 20)
        if self.events.player.recording:
            self.draw_text('recording', self.gui.font, (255, 255, 255), self.gui.screen, 20, 40)
        if self.events.player.playing:
            self.draw_text('playing', self.gui.font, (255, 255, 255), self.gui.screen, 20, 60)

        channel = self.events.get_current_channel()

        self.draw_text('channel: %s' % self.channel_index[0],
                       self.gui.font, (255, 255, 255), self.gui.screen, 20, 80)
        self.draw_text('instrument: %s' % channel.instr_dict[channel.instr[0], channel.instr[1]],
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
