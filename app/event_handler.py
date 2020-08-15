from synth import Synth
from player import Player
from modes import Freeplay, Test, SoundSelect
from keyboard_driver import Keyboard
import time
import pygame as pg


# Class for connecting synths with the keyboard or handling it with other players
class EventHandler(object):
    def __init__(self, port):
        # initialize channels and the keyboard
        self.channels = []
        # Keep track of channel modes
        self.channel_modes = []

        # Set the current mode to none
        self.current_channel_index = [0]

        # port for connecting to fluidsynth
        self.port = port

        # Start keyboard driver
        self.keyboard = Keyboard(self)

        # set the player/recorder and pass channels
        self.player = Player(self)

        for i in range(16):
            self.add_channel('freeplay',(0,0), 0)

        self.switch_channel(0)

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



    # Add a new channel and declare its playing mode
    def add_channel(self, mode, instr=(0, 0), reverb=0.3, gain=270):
        # Find the channel number
        channel_length = len(self.channels)

        self.current_channel_index[0] = channel_length

        # Make the synth and add it to channels
        if channel_length == 9:
            synth = Synth(event_handler=self, instr=(120, 0), reverb=reverb,
                          gain=gain)
        else:
            synth = Synth(event_handler=self, instr=instr, reverb=reverb,
                      gain=gain)
        self.channels.append(synth)
        self.add_mode(mode)

    # adds mode object to mode list
    def add_mode(self, mode):
        if mode == 'freeplay':
            self.channel_modes.append(Freeplay(self))
        elif mode == 'test':
            self.channel_modes.append(Test(self))
        elif mode == 'soundselect':
            self.channel_modes.append(SoundSelect(self))

    # Switch the mode of the current channel
    def switch_mode(self, mode):
        if mode == 'freeplay':
            self.channel_modes[self.current_channel_index[0]] = Freeplay(self)
        elif mode == 'test':
            self.channel_modes[self.current_channel_index[0]] = Test(self)
        elif mode == 'soundselect':
            self.channel_modes[self.current_channel_index[0]] = SoundSelect(self)

    # Switch the current channel
    def switch_channel(self, channel_ind):
        if channel_ind < 0 or channel_ind > 15:
            return

        # change the channel
        self.current_channel_index[0] = channel_ind

        # if the channel doesn't exist, make new channel
        if channel_ind >= len(self.channels):
            self.add_channel('freeplay')

    # Gets the current mode based on channel index
    def get_current_mode(self):
        return self.channel_modes[self.current_channel_index[0]]

    # Gets the current channel based on channel index
    def get_current_channel(self):
        return self.channels[self.current_channel_index[0]]

    # ------------------
    # Interface for passing to current mode
    # ------------------
    def key_down(self, index):
        self.get_current_mode().key_down(index)

    def key_up(self, index):
        self.get_current_mode().key_up(index)

    def use_knob(self, index, knob_num):
        if knob_num == 0:
            self.get_current_mode().use_knob(index, knob_num)


