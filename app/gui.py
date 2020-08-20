import pygame as pg
from pygame.locals import *
import platform
from pygame_functions import makeSprite, addSpriteImage


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
        self.interface.draw_interface()
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
        self.gui.screen.fill((0, 0, 0))

        self.gui.screen.blit(self.casset_sprite[int(self.casset_count)], (0, 0))
        self.gui.screen.blit(self.play_button[self.play_button_state], (194, 20))
        self.gui.screen.blit(self.stop_button[self.stop_button_state], (286, 20))
        self.gui.screen.blit(self.record_button[self.record_button_state], (96, 20))

        if self.keyboard.is_on('stop'):
            self.stop_button_state = 1
        else:
            self.stop_button_state = 0

        if self.player.recording:
            self.record_button_state = 1
            self.casset_roll_forward()
        elif self.player.playing:
            self.play_button_state = 1
            self.casset_roll_forward()
        else:
            self.play_button_state = 0
            self.record_button_state = 0


        self.draw_text(str(self.player.current_time), self.gui.font, (255, 255, 255), self.gui.screen, 230, 280)



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


