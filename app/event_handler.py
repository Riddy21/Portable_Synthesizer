from synth import Synth
from player import Player
from modes import Freeplay, Test
from keyboard_driver import Keyboard
import time
import pygame as pg


# Class for connecting synths with the keyboard or handling it with other players
class EventHandler(object):
    def __init__(self, port):
        # initialize channels and the keyboard
        self.channels = []

        # Set the current mode to none
        self.current_mode = None
        self.current_channel_index = [0]

        # port for connecting to fluidsynth
        self.port = port

        # Start keyboard driver
        self.keyboard = Keyboard(self)

        # set the player/recorder and pass channels
        self.player = Player(self)

    # ----------------------
    # API public methods
    # ----------------------

    # handle events
    def handle_events(self):
        start = time.time()
        events = pg.event.get()
        for e in events:
            if e.type == pg.KEYDOWN:
                try:
                    note = self.keyboard.get_key_index(e.key)
                except KeyError:
                    pass
                else:
                    self.keyboard.key_down(note)
                    end = time.time()
                    print(end - start)
            elif e.type == pg.KEYUP:
                try:
                    note = self.keyboard.get_key_index(e.key)
                except KeyError:
                    pass
                else:
                    self.keyboard.key_up(note)

        knobs = self.keyboard.get_knobs()
        if knobs[0]:
            self.keyboard.use_knob(0)

    # Add a new channel and declare its playing mode
    def add_channel(self, mode, instr=0, reverb=0.3, gain=270):
        # Find the channel number
        channel_length = len(self.channels)

        self.current_channel_index[0] = channel_length

        # Make the synth and add it to channels
        synth = Synth(mode=mode, event_handler=self, instr=instr, reverb=reverb,
                      gain=gain)
        self.channels.append(synth)

        # set the current playing mode and send the synth to it
        self.switch_mode('freeplay')

    # Switch the mode of the current channel
    def switch_mode(self, mode):
        synth = self.channels[self.current_channel_index[0]]
        if mode == 'freeplay':
            self.current_mode = Freeplay(synth, keyboard=self.keyboard, playback_handler=self)
        elif mode == 'test':
            self.current_mode = Test(synth, keyboard=self.keyboard, playback_handler=self)

    # Switch the current channel
    def switch_channel(self, channel_ind):
        if channel_ind < 0:
            return

        # change the channel
        self.current_channel_index[0] = channel_ind

        # if the channel doesn't exist, make new channel
        if channel_ind >= len(self.channels):
            self.add_channel('freeplay')

        # change the mode
        self.switch_mode(self.channels[channel_ind].mode)

    # ------------------
    # Interface for passing to current mode
    # ------------------
    def key_down(self, index):
        self.current_mode.key_down(index)

    def key_up(self, index):
        self.current_mode.key_up(index)

    def use_knob(self, index, knob_num):
        if knob_num == 0:
            self.current_mode.use_knob(index, knob_num)


