import platform
import pygame as pg
from rotary_encoder_driver import Driver
from threading_decorator import run_in_thread


# Interfacing with the Keyboard API
class Keyboard(object):
    def __init__(self):

        # init key values
        self.key_set = self.make_key_mapping()
        self.on_notes = []

        # init digital knobs
        # change to arrow keys on mac
        self.encoder_counter = [0] * 4
        self.encoder_buffer = [0] * 4
        self.encoder_driver = Driver(self.encoder_buffer, scalar=True, factor=1)
        self.start_encoder_listener()

        # Record button

        # Play button

        # Shift button

        # left right arrow

    # Change the channel we're connected
    def set_player(self, player):
        self.playback_handler = player

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

    # Run encoder listener
    @run_in_thread
    def start_encoder_listener(self):
        if platform.system() == 'Darwin':
            self.encoder_driver.start_mac_tester()
        else:
            self.encoder_driver.start_driver()

    # controls the keyboard to hit a key
    def key_down(self, key_index):
        if key_index not in self.on_notes:
            # add key to on_notes
            self.on_notes.append(key_index)

            # play note
            self.playback_handler.key_down(key_index)

    # controls the keyboard to release a key
    def key_up(self, key_index):
        if key_index in self.on_notes:
            # remove key from on_notes
            self.on_notes.remove(key_index)

            # play note
            self.playback_handler.key_up(key_index)

    # gets the scroll of the digital knob
    def get_knob(self, knob_num):
        # if the digital_buffer changes
        if self.encoder_buffer[knob_num] != self.encoder_counter[knob_num]:
            # send the new value and update
            self.encoder_counter[knob_num] = self.encoder_buffer[knob_num]
            return self.encoder_counter[knob_num]

        # if the digital_buffer is still the same return false
        return False

    # gets the scroll of the digital knob
    def get_knobs(self):
        knobs = [False] * 4
        # Update all 4 knobs
        for knob_num in range(4):
            # if the digital_buffer changes
            if self.encoder_buffer[knob_num] != self.encoder_counter[knob_num]:
                # send the new value and update
                self.encoder_counter[knob_num] = self.encoder_buffer[knob_num]
                knobs[knob_num] = self.encoder_counter[knob_num]

        return knobs

    # makes the playback handler use the know
    def use_knob(self, knob_num):
        self.playback_handler.use_knob(knob_num=knob_num, index=self.encoder_counter[knob_num])
