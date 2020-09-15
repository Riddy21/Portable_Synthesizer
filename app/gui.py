import pygame as pg
from pygame.locals import *
import platform
import time
import datetime
from pygame_functions import makeSprite, addSpriteImage, draw_bordered_rounded_rect

# Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (100,100,100)
RED = (255,109,103)
ORANGE = (255,184,108)
GREEN = (89,246,141)
YELLOW = (243,248,257)
PURPLE = (201,168,250)
PINK = (255,246,208)
CYAN = (153,236,253)

class Gui(object):

    def __init__(self, event_handler):
        # Setup display
        if platform.system() == 'Darwin' or platform.system() == 'Windows':
            self.screen = pg.display.set_mode((480, 320), 32)
        else:
            self.screen = pg.display.set_mode((480, 320), FULLSCREEN | DOUBLEBUF, 32)

        # Fonts
        self.font = pg.font.SysFont('SG02ttf', 25)

        # Get the playback handler to get all the events
        self.events = event_handler

        # dict of loaded interfaces
        self.interface_dict = dict()

        # TODO: Make startup interface
        self.set_interface('test')

    def add_interface(self, mode):
        if mode == 'record':
            self.interface_dict[mode] = RecordInt(self)
        # if mode == 'freeplay':
        #     self.interface_dict[mode] = FreeplayInt(self)
        # elif mode == 'soundselect':
        #     self.interface_dict[mode] = SoundSelectInt(self)
        elif mode == 'test':
            self.interface_dict[mode] = TestInt(self)

        self.interface = self.interface_dict[mode]

    # sets the interface of the OP1 and passes in the pointer to the player
    def set_interface(self, mode):
        try:
            self.interface = self.interface_dict[mode]
        except KeyError:
            self.add_interface(mode)

    # Draws whatever interface is currently on and updates
    def draw_interface(self):
        # switch interfaces if the interface changed
        mode_name = self.events.get_current_mode().name
        if mode_name != self.interface.name:
            self.set_interface(mode_name)

        # draw the interface and update
        self.interface.update_channel()
        self.interface.draw_interface()
        self.interface.draw_overlay()
        pg.display.update()


# -----------------------------
# Interface Modes
# -----------------------------

class GuiInterface(object):
    def __init__(self, name, gui):
        self.name = name
        self.events = gui.events
        self.player = gui.events.player
        self.mode = gui.events.get_current_mode()
        self.channel = gui.events.get_current_channel()
        self.keyboard = gui.events.keyboard
        self.gui = gui
        self.channel_index = self.events.current_channel_index

    # Draws the text on the screen
    @staticmethod
    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def update_channel(self):
        # update the channel
        self.channel = self.events.get_current_channel()

    def draw_overlay(self):
        time_rect = pg.rect.Rect(380, 280, 130, 80)
        draw_bordered_rounded_rect(self.gui.screen, time_rect, (0,0,0), WHITE, 8, 1)
        channel_rect = pg.rect.Rect(-30, 280, 130, 80)
        draw_bordered_rounded_rect(self.gui.screen, channel_rect, (0,0,0), WHITE, 8, 1)
        self.draw_text(
                '%s' % time.strftime('%M:%S', time.gmtime(self.player.current_time)),
                self.gui.font,
                WHITE,
                self.gui.screen, 
                393, 290)
        self.draw_text(
                '%d' % (self.channel_index[0] + 1),
                self.gui.font,
                GREEN,
                self.gui.screen,
                15, 290)

        # TODO: Make pedal icon
        if self.channel.sustenuto == 64:
            self.draw_text('S', self.gui.font, ORANGE, self.gui.screen, 40, 290)
        else:
            self.draw_text('S', self.gui.font, GRAY, self.gui.screen, 40, 290)
        # TODO: Make sustanuto icon
        if self.channel.sustain == 64:
            self.draw_text('P', self.gui.font, PURPLE, self.gui.screen, 65, 290)
        else:
            self.draw_text('P', self.gui.font, GRAY, self.gui.screen, 65, 290)


    # Draw interface abstract method
    def draw_interface(self):
        pass

class RecordInt(GuiInterface):
    def __init__(self, gui):

        # Background sprite
        self.casset_sprite = makeSprite('Assets/Sprites/Record/Recording_Background_Sprite.png', 5).images
        self.casset_count = 0

        # Button sprites
        self.play_button = makeSprite('Assets/Sprites/Record/Casset_Play_Button_Off.png',1)
        addSpriteImage(self.play_button, 'Assets/Sprites/Record/Casset_Play_Button_On.png')
        self.play_button = self.play_button.images
        self.play_button_state = 0

        self.record_button = makeSprite('Assets/Sprites/Record/Casset_Record_Button_Off.png', 1)
        addSpriteImage(self.record_button, 'Assets/Sprites/Record/Casset_Record_Button_On.png')
        self.record_button = self.record_button.images
        self.record_button_state = 0

        self.stop_button = makeSprite('Assets/Sprites/Record/Casset_Stop_Button_Off.png', 1)
        addSpriteImage(self.stop_button, 'Assets/Sprites/Record/Casset_Stop_Button_On.png')
        self.stop_button = self.stop_button.images
        self.stop_button_state = 0

        super().__init__('record', gui)

    def casset_roll_forward(self):

        self.casset_count = (self.casset_count - 0.2) % 5

    def casset_roll_backward(self):
        self.casset_count = (self.casset_count + 0.2) % 5

    def draw_interface(self):
        self.gui.screen.blit(self.casset_sprite[int(self.casset_count)], (0, 20))
        self.gui.screen.blit(self.play_button[self.play_button_state], (194, 30))
        self.gui.screen.blit(self.stop_button[self.stop_button_state], (286, 30))
        self.gui.screen.blit(self.record_button[self.record_button_state], (96, 30))

        if self.keyboard.is_on('stop'):
            self.stop_button_state = 1
        else:
            self.stop_button_state = 0

        if self.player.recording:
            self.record_button_state = 1
            self.casset_roll_forward()
        else:
            self.record_button_state = 0

        if self.player.playing:
            self.play_button_state = 1
            self.casset_roll_forward()
        else:
            self.play_button_state = 0

class SoundSelectInt(GuiInterface):
    def __init__(self, gui):
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


