import platform
import pygame as pg
from rotary_encoder_driver import Driver
from threading_decorator import run_in_thread


# Interfacing with the Keyboard API
class Keyboard(object):
    def __init__(self):

        # init key values
        self.key_dict = self.make_key_mapping()

        self.on_keys = set()

        # init digital knobs
        # change to arrow keys on mac
        self.encoder_counter = [0] * 4
        self.encoder_buffer = [0] * 4
        self.encoder_driver = Driver(self.encoder_buffer, scalar=True, factor=1)
        self.start_encoder_listener()

        # initialize with no play
        self.playback_handler = None

        # For tracking if shift is on faster
        self.shift = False

    # Change the channel were connected
    def set_handler(self, handler):
        self.playback_handler = handler

    # make list for piano keys
    @staticmethod
    def make_key_mapping():
        key_list = [
            pg.K_z,  # C1
            pg.K_s,  # C#1
            pg.K_x,  # D1
            pg.K_d,  # D#1
            pg.K_c,  # E1
            pg.K_v,  # F1
            pg.K_g,  # F#1
            pg.K_b,  # G1
            pg.K_h,  # G#1
            pg.K_n,  # A1
            pg.K_j,  # A#1
            pg.K_m,  # B1
            pg.K_q,  # C2
            pg.K_2,  # C#2
            pg.K_w,  # D2
            pg.K_3,  # D#2
            pg.K_e,  # E2
            pg.K_r,  # F2
            pg.K_5,  # F#2
            pg.K_t,  # G2
            pg.K_6,  # G#2
            pg.K_y,  # A2
            pg.K_7,  # A#2
            pg.K_u,  # B2
            pg.K_LSHIFT,
            pg.K_LEFT,  # left arrow
            pg.K_RIGHT,  # right arrow
            pg.K_RSHIFT,
            pg.K_BACKSPACE,
            pg.K_RETURN,
            pg.K_UP,
            pg.K_DOWN
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
        # If shift is off
        if key_index == 24 and not self.shift:
            self.shift = True

        # Checks the if the key is on and adds key to on keys if not on
        elif key_index not in self.on_keys:
            # add key to on_notes
            self.on_keys.add(key_index)

            # play note
            self.playback_handler.key_down(key_index)

    # controls the keyboard to release a key
    def key_up(self, key_index):
        if key_index == 24 and self.shift:
            self.shift = False

        elif key_index in self.on_keys:
            # remove key from on_notes
            self.on_keys.remove(key_index)

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
