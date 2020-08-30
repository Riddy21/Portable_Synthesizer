from synth import Synth
from player import Player
from modes import *
from keyboard_driver import Keyboard
import time
import pygame as pg
from synth import end


# Class for connecting synths with the keyboard or handling it with other players
class EventHandler(object):
    def __init__(self, port):
        # initialize channels and the keyboard
        self.channels = [None]*16
        # Keep track of channel modes
        self.channel_modes = [None]*16

        # Dictionary of loaded modes so that the mode objects do not need to be created again
        self.channel_mode_buffer = dict()

        # Set the current mode to 0 but keep as list to make sure you can pass by pointer
        self.current_channel_index = [0]

        # port for connecting to fluidsynth
        self.port = port

        # Start keyboard driver
        self.keyboard = Keyboard(self)

        # set the player/recorder and pass channels
        self.player = Player(self)

        self.add_channel('record', 0)

        self.switch_channel(0)

        # Knob queue for holding knob actions
        self.knob_queue = []

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
                    value = self.keyboard.get_key_name(e.key)
                except KeyError:
                    pass
                else:
                    self.keyboard.key_down(value)
                    print(end[0] - start)
            elif e.type == pg.KEYUP:
                try:
                    value = self.keyboard.get_key_name(e.key)
                except KeyError:
                    pass
                else:
                    self.keyboard.key_up(value)
        # collect knob events to knob queue
        self.keyboard.append_to_queue(self.knob_queue)
        # Do one change from the knob queue
        if self.knob_queue:
            knob_event = self.knob_queue.pop(0)
            self.keyboard.use_knob(knob_num=knob_event[0], change=knob_event[1])

    # Add a new channel and declare its playing mode
    def add_channel(self, mode, channel_ind, instr=(0, 0)):

        # Make the synth and add it to channels
        if channel_ind == 9:  # Set to standard piano if number 9 nine, default is drum
            instr = (120, 0)
        synth = Synth(event_handler=self,
                      instr=instr,
                      channel_ind=channel_ind)

        self.channels[channel_ind] = synth
        self.add_mode(mode, channel_ind)
        
        # Update current channel
        self.current_channel_index[0] = channel_ind

    # adds mode object to mode list
    def add_mode(self, mode, channel_ind):
        if mode == 'record':
            mode_obj = Record(self)
        elif mode == 'test':
            mode_obj = Test(self)

        self.channel_modes[channel_ind] = mode_obj
        self.channel_mode_buffer[mode] = mode_obj

    # Switch the mode of the current channel
    def switch_mode(self, mode, channel_ind):
        if mode == 'freeplay':
            try:
                # Try accessing using dictionary
                self.channel_modes[channel_ind] = self.channel_mode_buffer['freeplay']
                
            except KeyError:
                # If not in dictionary add the mode
                self.add_mode('freeplay', channel_ind)
            
        elif mode == 'test':
            try:
                # Try accessing using dictionary
                self.channel_modes[channel_ind] = self.channel_mode_buffer['test']
            except KeyError:
                # If not in dictionary add the mode
                self.add_mode('test', channel_ind)
        elif mode == 'soundselect':
            try:
                # Try accessing using dictionary
                self.channel_modes[channel_ind] = self.channel_mode_buffer['soundselect']
            except KeyError:
                # If not in dictionary add the mode
                self.add_mode('soundselect', channel_ind)
        
        self.channel_modes[channel_ind].update()

    # Switch the current channel
    def switch_channel(self, channel_ind):
        if channel_ind < 0 or channel_ind > 15:
            return

        # if the channel doesn't exist, make new channel
        if not self.channels[channel_ind]:
            self.add_channel(mode='record', channel_ind=channel_ind)


        else:
            # change the channel
            self.current_channel_index[0] = channel_ind

        # Update so channels are synced in modes
        self.channel_modes[channel_ind].update()
    
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

    def use_knob(self, change, knob_num):
        self.get_current_mode().use_knob(change, knob_num)
